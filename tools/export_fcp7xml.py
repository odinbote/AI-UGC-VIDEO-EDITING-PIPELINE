#!/usr/bin/env python3
"""
Export an edit plan (the JSON used by build_prproj.py) as Final Cut Pro 7 XML (xmeml v5),
importable by Premiere Pro (File > Import), DaVinci Resolve and others.

    python3 export_fcp7xml.py plan.json "out.xml"

What carries over: all cuts, in/out points, scale / position / rotation (with keyframes),
audio clips with gain and fades, the colour matte, titles and captions as text generators.
What does not exist in this format: Premiere's Text Animator in-transitions, the rose keyword
box and green caption pill, Essential Sound tags, the adjustment-layer grade. The .srt written
next to the XML lets you re-import the captions as a caption track.
"""
import json, sys, os, subprocess, re
from urllib.parse import quote
from xml.sax.saxutils import escape

W, H, FPS = 1080, 1920, 24
AUDIO_RATE = 48000

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = 'ffmpeg'


def probe(path):
    """returns (fps or None, duration_s, width, height, has_audio, channels)"""
    out = subprocess.run([FFMPEG, '-i', path], capture_output=True, text=True).stderr
    fps = None; w = h = None; aud = False; ch = 2
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', out)
    dur = (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))) if m else 0.0
    mv = re.search(r'Video: .*?, (\d+)x(\d+).*?([\d.]+) fps', out)
    if mv:
        w, h, fps = int(mv.group(1)), int(mv.group(2)), float(mv.group(3))
    ma = re.search(r'Audio: .*?(mono|stereo|\d+ channels)', out)
    if ma:
        aud = True
        ch = 1 if ma.group(1) == 'mono' else 2
    if path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        fps = None
        if not w:
            from PIL import Image
            w, h = Image.open(path).size
    return fps, dur, w, h, aud, ch


def rate_xml(tb, ntsc=False):
    return f'<rate><timebase>{tb}</timebase><ntsc>{"TRUE" if ntsc else "FALSE"}</ntsc></rate>'


def file_rate(fps):
    if fps is None:
        return FPS, False
    if abs(fps - 23.976) < 0.01:
        return 24, True
    if abs(fps - 29.97) < 0.01:
        return 30, True
    if abs(fps - 59.94) < 0.02:
        return 60, True
    return int(round(fps)), False


class Exporter:
    def __init__(self, plan):
        self.plan = plan
        self.media_dir = plan['output_dir'] if plan.get('media_flat') else os.path.join(plan['output_dir'], 'Media')
        self.files = {}      # basename -> (id, info)
        self.file_emitted = set()
        self.n = 0

    def uid(self, prefix):
        self.n += 1
        return f'{prefix}-{self.n}'

    LOGGING = ('<logginginfo><description></description><scene></scene><shottake></shottake><lognote></lognote><good></good>'
               '<originalvideofilename></originalvideofilename><originalaudiofilename></originalaudiofilename></logginginfo>'
               '<colorinfo><lut></lut><lut1></lut1><asc_sop></asc_sop><asc_sat></asc_sat><lut2></lut2></colorinfo><labels><label2>Iris</label2></labels>')

    def masterclip_id(self, path):
        fid, _ = self.file_info(path)
        return 'masterclip-' + fid.split('-')[1]

    def mpath(self, key):
        for f in sorted(os.listdir(self.media_dir)):
            if key in f:
                return os.path.join(self.media_dir, f)
        raise KeyError(key)

    def file_info(self, path):
        base = os.path.basename(path)
        if base not in self.files:
            fps, dur, w, h, aud, ch = probe(path)
            tb, ntsc = file_rate(fps)
            frames = int(round(dur * (tb / (1.001 if ntsc else 1)))) if fps else 1036800
            self.files[base] = (self.uid('file'), dict(path=path, fps=fps, tb=tb, ntsc=ntsc, frames=frames, w=w, h=h, aud=aud, ch=ch, still=fps is None))
        return self.files[base]

    def file_xml(self, path, want_audio_only=False):
        fid, info = self.file_info(path)
        if fid in self.file_emitted:
            return f'<file id="{fid}"/>'
        self.file_emitted.add(fid)
        url = 'file://localhost' + quote(os.path.abspath(path))
        media = ''
        if info['w']:
            media += (f'<video><samplecharacteristics>{rate_xml(info["tb"], info["ntsc"])}'
                      f'<width>{info["w"]}</width><height>{info["h"]}</height>'
                      f'<anamorphic>FALSE</anamorphic><pixelaspectratio>square</pixelaspectratio>'
                      f'<fielddominance>none</fielddominance></samplecharacteristics></video>')
        if info['aud']:
            media += (f'<audio><samplecharacteristics><depth>16</depth><samplerate>{AUDIO_RATE}</samplerate>'
                      f'</samplecharacteristics><channelcount>{info["ch"]}</channelcount></audio>')
        return (f'<file id="{fid}"><name>{escape(os.path.basename(path))}</name><pathurl>{url}</pathurl>'
                f'{rate_xml(info["tb"], info["ntsc"])}<duration>{info["frames"]}</duration>'
                f'<timecode>{rate_xml(info["tb"], info["ntsc"])}<string>00:00:00:00</string><frame>0</frame>'
                f'<displayformat>{"DF" if info["ntsc"] else "NDF"}</displayformat></timecode><media>{media}</media></file>')

    # ---- parameters ---------------------------------------------------------
    @staticmethod
    def kf_param(pid, name, value, kfs, vmin, vmax, in_f, fmt=lambda v: f'{v}'):
        s = f'<parameter><parameterid>{pid}</parameterid><name>{name}</name><valuemin>{vmin}</valuemin><valuemax>{vmax}</valuemax>'
        if kfs:
            s += f'<value>{fmt(kfs[0][1])}</value>'
            for t, v in kfs:
                s += f'<keyframe><when>{in_f + t}</when><value>{fmt(v)}</value></keyframe>'
        else:
            s += f'<value>{fmt(value)}</value>'
        return s + '</parameter>'

    @staticmethod
    def center(v):
        return f'<horiz>{v[0] - 0.5:.6f}</horiz><vert>{v[1] - 0.5:.6f}</vert>'

    def motion_filter(self, motion, in_f):
        sc = motion.get('Scale', 100); pos = motion.get('Position', [0.5, 0.5]); rot = motion.get('Rotation', 0)
        def split(v):
            return (v['keyframes'], v['keyframes'][0][1]) if isinstance(v, dict) else (None, v)
        sck, scv = split(sc); pk, pv = split(pos); rk, rv = split(rot)
        p = self.kf_param('scale', 'Scale', scv, sck, 0, 1000, in_f)
        p += self.kf_param('rotation', 'Rotation', rv, rk, -8640, 8640, in_f)
        p += self.kf_param('center', 'Center', pv, pk, '', '', in_f, fmt=lambda v: self.center(v)).replace('<valuemin></valuemin><valuemax></valuemax>', '')
        p += '<parameter><parameterid>centerOffset</parameterid><name>Anchor Point</name><value><horiz>0</horiz><vert>0</vert></value></parameter>'
        return (f'<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory>'
                f'<effecttype>motion</effecttype><mediatype>video</mediatype>{p}</effect></filter>')

    @staticmethod
    def opacity_filter(v=100):
        return ('<filter><effect><name>Opacity</name><effectid>opacity</effectid><effectcategory>motion</effectcategory>'
                '<effecttype>motion</effecttype><mediatype>video</mediatype><parameter><parameterid>opacity</parameterid>'
                f'<name>opacity</name><valuemin>0</valuemin><valuemax>100</valuemax><value>{v}</value></parameter></effect></filter>')

    @staticmethod
    def level_filter(gain_db, dur_f, fade_in_f=0, fade_out_f=0, in_f=0):
        g = 10 ** (gain_db / 20.0)
        s = ('<filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>audiolevels</effectcategory>'
             '<effecttype>audiolevels</effecttype><mediatype>audio</mediatype><parameter><parameterid>level</parameterid>'
             f'<name>Level</name><valuemin>0</valuemin><valuemax>3.98109</valuemax><value>{g:.6f}</value>')
        if fade_in_f or fade_out_f:
            if fade_in_f:
                s += f'<keyframe><when>{in_f}</when><value>0</value></keyframe><keyframe><when>{in_f + fade_in_f}</when><value>{g:.6f}</value></keyframe>'
            else:
                s += f'<keyframe><when>{in_f}</when><value>{g:.6f}</value></keyframe>'
            if fade_out_f:
                s += f'<keyframe><when>{in_f + dur_f - fade_out_f}</when><value>{g:.6f}</value></keyframe><keyframe><when>{in_f + dur_f}</when><value>0</value></keyframe>'
        return s + '</parameter></effect></filter>'

    # ---- items ----------------------------------------------------------------
    def video_clip(self, it, path, name=None):
        fid, info = self.file_info(path)
        s_f, e_f = it['start_f'], it['end_f']
        tb_scale = (info['tb'] / (1.001 if info['ntsc'] else 1)) / FPS
        if info['still']:
            in_f = 0; out_f = e_f - s_f
        elif 'in_s' in it:
            in_f = int(round(it['in_s'] * info['tb'] / (1.001 if info['ntsc'] else 1))); out_f = in_f + int(round((e_f - s_f) * tb_scale))
        else:
            in_f = int(round(it.get('in_f', s_f) * tb_scale)); out_f = in_f + int(round((e_f - s_f) * tb_scale))
        cid = self.uid('clipitem')
        filters = self.motion_filter(it.get('motion', {}), in_f) + self.opacity_filter()
        tbf = info['tb'] / (1.001 if info['ntsc'] else 1)
        ticks_in = int(round(in_f / tbf * 254016000000)); ticks_out = int(round(out_f / tbf * 254016000000))
        alpha = 'straight' if path.lower().endswith('.mov') and ('alpha' in path.lower() or 'loader' in path.lower()) else 'none'
        return cid, (f'<clipitem id="{cid}"><masterclipid>{self.masterclip_id(path)}</masterclipid><name>{escape(name or os.path.basename(path))}</name><enabled>TRUE</enabled>'
                     f'<duration>{info["frames"]}</duration>{rate_xml(info["tb"], info["ntsc"])}'
                     f'<start>{s_f}</start><end>{e_f}</end><in>{in_f}</in><out>{out_f}</out>'
                     f'<pproTicksIn>{ticks_in}</pproTicksIn><pproTicksOut>{ticks_out}</pproTicksOut>'
                     f'<alphatype>{alpha}</alphatype><pixelaspectratio>square</pixelaspectratio><anamorphic>FALSE</anamorphic>'
                     f'{self.file_xml(path)}<sourcetrack><mediatype>video</mediatype><trackindex>1</trackindex></sourcetrack>'
                     f'{filters}LINKS{self.LOGGING}</clipitem>')

    def audio_clip(self, it, path, channel=1):
        fid, info = self.file_info(path)
        s_f, e_f = it['start_f'], it['end_f']
        in_f = int(round(it['in_s'] * FPS)) if 'in_s' in it else it.get('in_f', s_f)
        out_f = in_f + (e_f - s_f)
        cid = self.uid('clipitem')
        lvl = self.level_filter(it.get('gain_db', 0), e_f - s_f, it.get('fade_in_f', 0), it.get('fade_out_f', 0), in_f)
        ticks_in = int(round(in_f / FPS * 254016000000)); ticks_out = int(round(out_f / FPS * 254016000000))
        return cid, (f'<clipitem id="{cid}" premiereChannelType="{"stereo" if info["ch"] == 2 else "mono"}"><masterclipid>{self.masterclip_id(path)}</masterclipid>'
                     f'<name>{escape(os.path.basename(path))}</name><enabled>TRUE</enabled>'
                     f'<duration>{int(round(info["frames"] * FPS / info["tb"])) if not info["still"] else info["frames"]}</duration>{rate_xml(FPS)}'
                     f'<start>{s_f}</start><end>{e_f}</end><in>{in_f}</in><out>{out_f}</out>'
                     f'<pproTicksIn>{ticks_in}</pproTicksIn><pproTicksOut>{ticks_out}</pproTicksOut>'
                     f'{self.file_xml(path)}<sourcetrack><mediatype>audio</mediatype><trackindex>{channel}</trackindex></sourcetrack>'
                     f'{lvl}LINKS{self.LOGGING}</clipitem>')

    def matte_item(self, it, rgb=(245, 245, 245)):
        s_f, e_f = it['start_f'], it['end_f']
        cid = self.uid('clipitem')
        return (f'<generatoritem id="{cid}"><name>Color Matte</name><enabled>TRUE</enabled><duration>1036800</duration>{rate_xml(FPS)}'
                f'<start>{s_f}</start><end>{e_f}</end><in>0</in><out>{e_f - s_f}</out>'
                f'<effect><name>Color</name><effectid>Color</effectid><effectcategory>Matte</effectcategory><effecttype>generator</effecttype>'
                f'<mediatype>video</mediatype><parameter><parameterid>fillcolor</parameterid><name>Color</name>'
                f'<value><alpha>255</alpha><red>{rgb[0]}</red><green>{rgb[1]}</green><blue>{rgb[2]}</blue></value></parameter></effect>'
                f'{self.opacity_filter()}</generatoritem>')

    def text_item(self, it, text, font, style, size, pos, color=(255, 255, 255), name='Title'):
        s_f, e_f = it['start_f'], it['end_f']
        cid = self.uid('clipitem')
        return (f'<generatoritem id="{cid}"><name>{escape(name)}</name><enabled>TRUE</enabled><duration>1036800</duration>{rate_xml(FPS)}'
                f'<start>{s_f}</start><end>{e_f}</end><in>0</in><out>{e_f - s_f}</out>'
                f'<effect><name>Text</name><effectid>Text</effectid><effectcategory>Text</effectcategory><effecttype>generator</effecttype><mediatype>video</mediatype>'
                f'<parameter><parameterid>str</parameterid><name>Text</name><value>{escape(text)}</value></parameter>'
                f'<parameter><parameterid>fontname</parameterid><name>Font</name><value>{escape(font)}</value></parameter>'
                f'<parameter><parameterid>fontsize</parameterid><name>Size</name><valuemin>0</valuemin><valuemax>1000</valuemax><value>{size}</value></parameter>'
                f'<parameter><parameterid>fontstyle</parameterid><name>Style</name><valuemin>1</valuemin><valuemax>4</valuemax><value>{style}</value></parameter>'
                f'<parameter><parameterid>fontalign</parameterid><name>Alignment</name><valuemin>1</valuemin><valuemax>3</valuemax><value>2</value></parameter>'
                f'<parameter><parameterid>fontcolor</parameterid><name>Font Color</name><value><alpha>255</alpha><red>{color[0]}</red><green>{color[1]}</green><blue>{color[2]}</blue></value></parameter>'
                f'<parameter><parameterid>origin</parameterid><name>Origin</name><value>{self.center(pos)}</value></parameter>'
                f'</effect>{self.motion_filter({}, 0)}{self.opacity_filter()}</generatoritem>')

    # ---- sequence -------------------------------------------------------------
    def export(self):
        plan = self.plan
        items = plan['items']
        total = plan['total_frames']
        pm = plan.get('media', {})
        aroll = self.mpath(pm.get('aroll', 'aroll'))
        cutout = self.mpath(pm.get('cutout', 'cutout'))
        vtracks_order = ['Aroll', 'Color mate Background', 'Screen Recording 1', 'Screen Recording 2', 'Broll 1', 'Broll 2',
                         'Aroll Cutout', 'Aroll Full Screen', 'Logos', 'Text Graphics 1', 'Text Graphics 2', 'Text Graphics 3',
                         'Captions', 'Outro Animation']
        atracks_logical = ['Aroll Sound', 'SFX 1', 'SFX 2', 'SFX 3', 'SFX 4', 'SFX 5', 'Background music']
        atracks_order = [f'{t} ch{c}' for t in atracks_logical for c in (1, 2)]
        vtracks = {t: [] for t in vtracks_order}
        atracks = {t: [] for t in atracks_order}
        links = {}   # link group -> [(cid, 'video'/'audio', trackindex, clipindex)]
        clipx = {}

        def title_spec(t):
            style = t['style']
            if style == 'serif':
                return 'Instrument Serif', 3, t['size']
            return 'SF Pro Display', 2, t['size']

        for it in items:
            kind = it['kind']
            if kind == 'video':
                tr = it['track']
                if tr == 'Color mate Background':
                    vtracks[tr].append((None, self.matte_item(it))); continue
                if it.get('file'):
                    path = self.mpath(it['file'])
                elif it.get('still'):
                    path = self.mpath(it['still'])
                elif tr == 'Aroll Cutout':
                    path = cutout
                elif tr in ('Aroll', 'Aroll Full Screen'):
                    path = aroll
                elif tr.startswith('Broll'):
                    path = self.mpath('Silicon Valley' if it['exemplar'] == 'broll1' else 'SOCIAL NETWORK')
                elif tr == 'Outro Animation':
                    path = self.mpath('fanout-loader')
                else:
                    continue
                cid, x = self.video_clip(it, path)
                vtracks[tr].append((cid, x))
                if it.get('link'):
                    links.setdefault(it['link'], []).append((cid, 'video', vtracks_order.index(tr) + 1, len(vtracks[tr])))
            elif kind == 'graphic':
                t = it['title']; font, style, size = title_spec(t)
                pos = it['motion']['Position']; screen = (pos[0], pos[1] + 0.096)
                vtracks[it['track']].append((None, self.text_item(it, t['text'], font, style, size, screen, name=t['text'])))
            elif kind == 'caption':
                y = it.get('y', {'cap_layout': 0.385, 'cap_youll': 0.61, 'cap_understand': 0.61, 'cap_low': 0.70}.get(it['exemplar'], 0.5))
                vtracks['Captions'].append((None, self.text_item(it, it['text'], 'Instrument Serif', 3, 70, (0.5, y), name=it['text'])))
            elif kind == 'audio':
                tr = it['track']
                if tr == 'Aroll Sound':
                    path = aroll
                elif it['exemplar'] == 'music':
                    path = self.mpath('Electronica')
                else:
                    path = self.mpath(it.get('file') or {'sfx_click': 'Mechanical, Click, Buttons', 'sfx_ui_a': 'User Interface, Click', 'sfx_ui_b': 'User Interface, Click',
                                                           'sfx_whoosh': 'Swooshes, Whoosh', 'sfx_woosh2': 'Transition_Woosh', 'sfx_button': 'Miniature Button', 'sfx_ting': 'Pings, Tings'}[it['exemplar']])
                _, info = self.file_info(path)
                group = it.get('link') or f'au-{self.n}'
                for ch in (1, 2) if info['ch'] == 2 else (1,):
                    cid, x = self.audio_clip(it, path, ch)
                    tname = f'{tr} ch{ch}'
                    atracks[tname].append((cid, x))
                    links.setdefault(group, []).append((cid, 'audio', atracks_order.index(tname) + 1, len(atracks[tname])))

        def link_xml(group, own):
            out = ''
            for cid, mt, ti, ci in group:
                out += f'<link><linkclipref>{cid}</linkclipref><mediatype>{mt}</mediatype><trackindex>{ti}</trackindex><clipindex>{ci}</clipindex></link>'
            return out
        linkmap = {cid: g for g in links.values() if len(g) > 1 for (cid, *_rest) in g}

        def render_tracks(tracks, order, audio=False):
            out = ''
            for i, name in enumerate(order):
                out += '<track>' if not audio else f'<track currentExplodedTrackIndex="{i % 2}" totalExplodedTrackCount="2" premiereTrackType="Stereo">'
                for cid, x in tracks[name]:
                    out += x.replace('LINKS', link_xml(linkmap[cid], cid) if cid in linkmap else '')
                out += '<enabled>TRUE</enabled><locked>FALSE</locked>'
                if audio:
                    out += f'<outputchannelindex>{i % 2 + 1}</outputchannelindex>'
                out += '</track>'
            return out

        seq_name = plan.get('sequence_name', plan['project_name'])
        import uuid as _uuid
        xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4">'
               f'<sequence id="{self.uid("sequence")}"><uuid>{_uuid.uuid4()}</uuid><updatebehavior>add</updatebehavior><name>{escape(seq_name)}</name>'
               f'<duration>{total}</duration>{rate_xml(FPS)}'
               f'<timecode>{rate_xml(FPS)}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>'
               '<in>-1</in><out>-1</out>'
               '<media><video><format><samplecharacteristics>' + rate_xml(FPS) +
               f'<width>{W}</width><height>{H}</height><anamorphic>FALSE</anamorphic><pixelaspectratio>square</pixelaspectratio>'
               '<fielddominance>none</fielddominance><colordepth>24</colordepth></samplecharacteristics></format>'
               + render_tracks(vtracks, vtracks_order) + '</video>'
               f'<audio><format><samplecharacteristics><depth>16</depth><samplerate>{AUDIO_RATE}</samplerate></samplecharacteristics></format>'
               '<outputs><group><index>1</index><numchannels>2</numchannels><downmix>0</downmix><channel><index>1</index></channel><channel><index>2</index></channel></group></outputs>'
               + render_tracks(atracks, atracks_order, audio=True) + '</audio></media>'
               '<labels><label2>Forest</label2></labels><logginginfo><description></description><scene></scene><shottake></shottake><lognote></lognote><good></good>'
               '<originalvideofilename></originalvideofilename><originalaudiofilename></originalaudiofilename></logginginfo></sequence></xmeml>')
        return xml

    def srt(self):
        def tc(f):
            s = f / FPS; h = int(s // 3600); m = int(s % 3600 // 60); sec = s % 60
            return f'{h:02d}:{m:02d}:{int(sec):02d},{int(round((sec - int(sec)) * 1000)):03d}'
        out = []; n = 0
        for it in self.plan['items']:
            if it['kind'] == 'caption':
                n += 1
                out.append(f'{n}\n{tc(it["start_f"])} --> {tc(it["end_f"])}\n{it["text"]}\n')
        return '\n'.join(out)


if __name__ == '__main__':
    plan = json.load(open(sys.argv[1]))
    ex = Exporter(plan)
    xml = ex.export()
    open(sys.argv[2], 'w', encoding='utf-8').write(xml)
    srt_path = os.path.splitext(sys.argv[2])[0] + ' captions.srt'
    open(srt_path, 'w', encoding='utf-8').write(ex.srt())
    print('wrote', sys.argv[2], len(xml), 'bytes;', srt_path)
