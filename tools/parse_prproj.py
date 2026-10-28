import xml.etree.ElementTree as ET, sys, json, re, base64
TICKS=254016000000
path=sys.argv[1]
r=ET.parse(path).getroot()
byid={}; byuid={}
for e in r:
    if 'ObjectID' in e.attrib: byid[e.attrib['ObjectID']]=e
    if 'ObjectUID' in e.attrib: byuid[e.attrib['ObjectUID']]=e
def ref(el):
    if el is None: return None
    if 'ObjectRef' in el.attrib: return byid.get(el.attrib['ObjectRef'])
    if 'ObjectURef' in el.attrib: return byuid.get(el.attrib['ObjectURef'])
    return None
def txt(el,tag,default=None):
    x=el.find(tag); return x.text if x is not None and x.text is not None else default
def find_desc(el,tag):
    return el.find('.//'+tag)
seq=[e for e in r if e.tag=='Sequence'][0]
seq_name=txt(seq,'Name')
fr_ticks=None
def fmt(t):
    s=t/TICKS; return f"{s:7.3f}s (f{round(s*fps):4d})"
# locate track groups
tgs=seq.find('TrackGroups')
groups=[]
for tg in tgs.findall('TrackGroup'):
    sec=ref(tg.find('Second')); groups.append(sec)
vg=[g for g in groups if g.tag=='VideoTrackGroup'][0]
ag=[g for g in groups if g.tag=='AudioTrackGroup'][0]
fps=TICKS/int(txt(vg.find('TrackGroup'),'FrameRate'))
print(f"SEQUENCE: {seq_name}  fps={fps:g}  frame={vg.findtext('FrameRect')}")

def parse_kf_scalar(s):
    out=[]
    for part in filter(None,s.strip().split(';')):
        f=part.split(',')
        t=int(f[0])-3600*TICKS
        out.append((t,f[1],f[2]))
    return out
def param_summary(p):
    name=txt(p,'Name'); sk=txt(p,'StartKeyframe'); kfs=txt(p,'Keyframes')
    val=None
    if sk:
        parts=sk.split(',')
        val=parts[1] if len(parts)>1 else sk
    tv=txt(p,'IsTimeVarying')=='true'
    s=f"{name}={val}"
    if kfs:
        s+=" KF["+ " | ".join(f"{fmt(t)}→{v} interp{i}" for t,v,i in parse_kf_scalar(kfs))+"]"
    # arb data
    arb=p.find('ArbData') 
    return s, name, val, kfs, p
def components(owner):
    comps=ref(owner.find('Components')) if owner is not None else None
    out=[]
    if comps is None: return out
    for c in comps.iter('Component'):
        ce=ref(c)
        if ce is None: continue
        out.append(ce)
    return out
def dump_component(ce,indent='      '):
    dn=find_desc(ce,'DisplayName'); mn=txt(ce,'MatchName')
    dn=dn.text if dn is not None else ce.tag
    lines=[f"{indent}[{dn}] ({mn})"]
    params=ce.find('.//Params')
    if params is None: return lines
    for pr in params.findall('Param'):
        p=ref(pr)
        if p is None: continue
        s,name,val,kfs,_=param_summary(p)
        # skip boring params
        if name in ('_ Sequence Width','_ Sequence Height','_ Sequence Pixel Ratio','_ Overlay Mode','_ Overlay Info','_ Overlay Enabled','_ Applied Version','Error occurred','Visual Curve Editor','Curve Graph','Parent Width','Parent Height','Parent Rotation'): continue
        if kfs or val not in (None,'0','0.','1','1.','false','true') or name in ('Preset','Type','Source Text','Scale','Position','Opacity','Start','End','Blend Mode'):
            lines.append(f"{indent}   {s}")
    return lines

def dump_track_item(ti,kind):
    cti=ti.find('ClipTrackItem'); tr=cti.find('TrackItem')
    start=int(txt(tr,'Start','0')); end=int(txt(tr,'End'))
    sub=ref(cti.find('SubClip'))
    name=txt(sub,'Name') if sub is not None else '?'
    clip=ref(sub.find('Clip')) if sub is not None else None
    inp=outp=None; src_dur=None
    if clip is not None:
        c=clip.find('Clip')
        inp=txt(c,'InPoint'); outp=txt(c,'OutPoint')
        src=ref(c.find('Source'))
        if src is not None:
            src_dur=txt(src,'OriginalDuration')
    speed=''
    dur=end-start
    if inp and outp:
        sd=int(outp)-int(inp)
        if abs(sd-dur)>TICKS/fps/2: speed=f" SPEED {sd/dur*100:.0f}%"
    line=f"  {fmt(start)} → {fmt(end)}  dur {(end-start)/TICKS:6.3f}s  '{name}'"
    if inp and outp: line+=f"  src {int(inp)/TICKS:.3f}–{int(outp)/TICKS:.3f}{speed}"
    lines=[line]
    for ce in components(cti.find('ComponentOwner')):
        lines+=dump_component(ce)
    # also master-clip (source) effects
    return lines

for label,g in (('VIDEO',vg),('AUDIO',ag)):
    print(f"\n==================== {label} TRACKS ====================")
    tracks=g.find('TrackGroup/Tracks').findall('Track')
    for t in tracks:
        te=ref(t)
        if te is None: continue
        tname=te.findtext('.//MZ.TrackName') or ''
        items=te.find('.//ClipItems/TrackItems')
        n=len(items.findall('TrackItem')) if items is not None else 0
        locked=te.findtext('.//MZ.TrackLocked')
        print(f"\n--- {label[0]}{int(t.attrib['Index'])+1}  '{tname}'  ({n} clips)")
        if items is None: continue
        tis=[ref(x) for x in items.findall('TrackItem')]
        tis=[x for x in tis if x is not None]
        tis.sort(key=lambda ti:int(txt(ti.find('ClipTrackItem/TrackItem'),'Start','0')))
        for ti in tis:
            for l in dump_track_item(ti,label): print(l)

# ---- caption track ----
import base64, struct
def _strings(b):
    out=[]; i=0
    while i < len(b)-4:
        n=struct.unpack_from('<I',b,i)[0]
        if 1<=n<=300 and i+4+n<len(b) and b[i+4+n]==0:
            try:
                t=b[i+4:i+4+n].decode('utf-8')
                if all(32<=ord(c)<0x3000 or c=='\n' for c in t): out.append(t); i+=4+n; continue
            except Exception: pass
        i+=1
    return out
for ctr in [e for e in r if e.tag=='CaptionDataClipTrack']:
    print(f"\n==================== CAPTIONS '{ctr.findtext('.//MZ.TrackName')}' ====================")
    for x in ctr.find('.//ClipItems/TrackItems').findall('TrackItem'):
        ti=ref(x); cti=ti.find('.//ClipTrackItem'); st=int(txt(cti.find('TrackItem'),'Start','0')); en=int(txt(cti.find('TrackItem'),'End'))
        words=[]
        for b in ti.find('BlockVector').findall('BlockVectorItem'):
            be=ref(b); ft=be.findtext('FormattedTextData')
            if ft: words+=_strings(base64.b64decode(ft))
        print(f"  {fmt(st)} → {fmt(en)}  dur {(en-st)/TICKS:6.3f}s  {words}")
