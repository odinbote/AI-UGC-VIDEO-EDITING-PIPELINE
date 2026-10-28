#!/usr/bin/env python3
"""
Build a new Premiere Pro project (.prproj) by cloning track items from a reference
project (Abik's "AI UGC 1" reel) and re-timing them according to an edit plan.

Usage:
    python3 build_prproj.py plan.json

The plan JSON describes: reference project path, output path, media retargets, and the
list of track items (video / audio / graphics / captions).  See fanout_reel_2_plan.json.
"""
import xml.etree.ElementTree as ET
import gzip, json, sys, os, re, copy, uuid, base64, struct, shutil, time

TICKS = 254016000000          # ticks per second
FPS = 24
FT = TICKS // FPS             # ticks per frame (10584000000)
H3600 = 3600 * TICKS          # Premiere's synthetic-media / keyframe time offset
KF_START = "-91445760000000000"


def f2t(frames):
    return int(round(frames * FT))


def s2t(seconds):
    return int(round(seconds * TICKS))


class Project:
    def __init__(self, path):
        with gzip.open(path, 'rb') as fh:
            data = fh.read()
        self.tree = ET.ElementTree(ET.fromstring(data))
        self.root = self.tree.getroot()
        self.reindex()
        self.next_oid = max(int(k) for k in self.byid) + 1
        self.cloned = []
        # BinaryHash -> data text (Premiere defines each block once, at its first occurrence; later ones are empty refs)
        self.blob_table = {}
        for top in self.root:
            for e in top.iter():
                h = e.attrib.get('BinaryHash')
                if h and e.text and e.text.strip() and h not in self.blob_table:
                    self.blob_table[h] = e.text

    def reindex(self):
        self.byid = {e.attrib['ObjectID']: e for e in self.root if 'ObjectID' in e.attrib}
        self.byuid = {e.attrib['ObjectUID']: e for e in self.root if 'ObjectUID' in e.attrib}

    # ---- lookup helpers -------------------------------------------------
    def ref(self, el):
        if el is None:
            return None
        if 'ObjectRef' in el.attrib:
            return self.byid.get(el.attrib['ObjectRef'])
        if 'ObjectURef' in el.attrib:
            return self.byuid.get(el.attrib['ObjectURef'])
        return None

    def new_id(self):
        oid = str(self.next_oid)
        self.next_oid += 1
        return oid

    def track(self, kind, name):
        """kind: 'video' | 'audio' | 'caption'"""
        if kind == 'caption':
            for e in self.root:
                if e.tag == 'CaptionDataClipTrack' and e.findtext('.//MZ.TrackName') == name:
                    return e
        grp = [e for e in self.root if e.tag == ('VideoTrackGroup' if kind == 'video' else 'AudioTrackGroup')][0]
        for t in grp.find('TrackGroup/Tracks').findall('Track'):
            te = self.ref(t)
            if te is not None and te.findtext('.//MZ.TrackName') == name:
                return te
        raise KeyError(name)

    def track_items(self, te):
        items = te.find('.//ClipItems/TrackItems')
        return [self.ref(x) for x in items.findall('TrackItem')] if items is not None else []

    def item_start_end(self, item):
        ti = item.find('.//TrackItem')
        s = ti.findtext('Start')
        return (int(s) if s else 0, int(ti.findtext('End')))

    def find_item(self, kind, track_name, start_seconds):
        """exemplar lookup by track + start time (seconds, tolerance half frame)"""
        for it in self.track_items(self.track(kind, track_name)):
            s, _ = self.item_start_end(it)
            if abs(s - s2t(start_seconds)) < FT / 2:
                return it
        raise KeyError(f'{track_name} @ {start_seconds}')

    @staticmethod
    def norm(s):
        return (s or '').replace('\u202f', ' ').replace('\u00a0', ' ')

    def media_by_title(self, title):
        for e in self.root:
            if e.tag == 'Media' and self.norm(e.findtext('Title')) == self.norm(title):
                return e
        raise KeyError(title)

    def masterclip_by_name(self, name):
        for e in self.root:
            if e.tag == 'MasterClip' and self.norm(e.findtext('Name')) == self.norm(name):
                return e
        raise KeyError(name)

    def projectitem_by_name(self, name):
        for e in self.root:
            if e.tag == 'ClipProjectItem' and self.norm(e.findtext('.//Name')) == self.norm(name):
                return e
        raise KeyError(name)

    # ---- cloning --------------------------------------------------------
    def closure(self, oid, seen=None, follow_uid_tags=(), useen=None):
        seen = seen if seen is not None else []
        useen = useen if useen is not None else []
        if oid in seen or oid not in self.byid:
            return seen, useen
        seen.append(oid)
        for e in self.byid[oid].iter():
            if 'ObjectRef' in e.attrib:
                self.closure(e.attrib['ObjectRef'], seen, follow_uid_tags, useen)
            elif 'ObjectURef' in e.attrib and follow_uid_tags:
                self.uclosure(e.attrib['ObjectURef'], seen, follow_uid_tags, useen)
        return seen, useen

    def uclosure(self, uid, seen, follow_uid_tags, useen):
        tgt = self.byuid.get(uid)
        if tgt is None or uid in useen or tgt.tag not in follow_uid_tags:
            return
        useen.append(uid)
        for e in tgt.iter():
            if 'ObjectRef' in e.attrib:
                self.closure(e.attrib['ObjectRef'], seen, follow_uid_tags, useen)
            elif 'ObjectURef' in e.attrib:
                self.uclosure(e.attrib['ObjectURef'], seen, follow_uid_tags, useen)

    GUID_TAGS = {'ClipID', 'FileKey'}

    def clone(self, oid, follow_uid_tags=()):
        """Deep-copy the closure of object `oid`; returns (idmap, uidmap)."""
        ids, uids = self.closure(oid, follow_uid_tags=follow_uid_tags)
        idmap = {o: self.new_id() for o in ids}
        uidmap = {u: str(uuid.uuid4()) for u in uids}
        for o in ids:
            self._add_clone(self.byid[o], idmap, uidmap)
        for u in uids:
            self._add_clone(self.byuid[u], idmap, uidmap)
        return idmap, uidmap

    def _add_clone(self, src, idmap, uidmap):
        c = copy.deepcopy(src)
        if 'ObjectID' in c.attrib:
            c.attrib['ObjectID'] = idmap[c.attrib['ObjectID']]
        if 'ObjectUID' in c.attrib:
            c.attrib['ObjectUID'] = uidmap[c.attrib['ObjectUID']]
        for e in c.iter():
            if 'ObjectRef' in e.attrib and e.attrib['ObjectRef'] in idmap:
                e.attrib['ObjectRef'] = idmap[e.attrib['ObjectRef']]
            if 'ObjectURef' in e.attrib and e.attrib['ObjectURef'] in uidmap:
                e.attrib['ObjectURef'] = uidmap[e.attrib['ObjectURef']]
            if e.tag in self.GUID_TAGS and e.text and re.match(r'^[0-9a-f-]{36}$', e.text.strip()):
                e.text = str(uuid.uuid4())
            if e.tag == 'ID' and e.text and re.match(r'^[0-9a-f-]{36}$', e.text.strip()):
                e.text = str(uuid.uuid4())
        c.tail = '\n\t'
        self.cloned.append(c)
        self.root.append(c)
        if 'ObjectID' in c.attrib:
            self.byid[c.attrib['ObjectID']] = c
        if 'ObjectUID' in c.attrib:
            self.byuid[c.attrib['ObjectUID']] = c
        return c

    # ---- item editing ---------------------------------------------------
    @staticmethod
    def set_child(parent, tag, text, before=None):
        el = parent.find(tag)
        if el is None:
            el = ET.Element(tag)
            el.tail = '\n'
            if before is not None and parent.find(before) is not None:
                parent.insert(list(parent).index(parent.find(before)), el)
            else:
                parent.append(el)
        el.text = str(text)
        return el

    def set_item_times(self, item, start_t, end_t, in_t, out_t):
        ti = item.find('.//TrackItem')
        self.set_child(ti, 'Start', start_t, before='End')
        self.set_child(ti, 'End', end_t)
        sub = self.ref(item.find('.//SubClip'))
        clip = self.ref(sub.find('Clip'))
        c = clip.find('.//Clip')
        self.set_child(c, 'InPoint', in_t)
        self.set_child(c, 'OutPoint', out_t)

    def components(self, item):
        comps = self.ref(item.find('.//ComponentOwner/Components'))
        out = []
        if comps is None:
            return out
        for c in comps.iter('Component'):
            ce = self.ref(c)
            if ce is not None:
                out.append(ce)
        return out

    def param(self, item, match_name, param_name):
        for ce in self.components(item):
            if ce.findtext('MatchName') != match_name:
                continue
            params = ce.find('.//Params')
            for pr in params.findall('Param'):
                p = self.ref(pr)
                if p is not None and p.findtext('Name') == param_name:
                    return p
        raise KeyError(f'{match_name}/{param_name}')

    @staticmethod
    def _fmt(v):
        if isinstance(v, (tuple, list)):
            return f'{v[0]}:{v[1]}'
        if isinstance(v, bool):
            return 'true' if v else 'false'
        fv = float(v)
        return (str(int(fv)) + '.') if fv.is_integer() else repr(fv)

    def set_param(self, item, match_name, name, value, keyframes=None):
        """value: scalar or (x,y). keyframes: list of (time_ticks, value); keyframe
        template strings are taken from the exemplar's existing Keyframes if present."""
        p = self.param(item, match_name, name)
        sk = p.find('StartKeyframe')
        parts = sk.text.split(',')
        parts[1] = self._fmt(value)
        sk.text = ','.join(parts)
        cv = p.find('CurrentValue')
        if cv is not None:
            cv.text = self._fmt(value).rstrip('.')
        kf = p.find('Keyframes')
        if keyframes:
            if kf is None:
                kf = ET.SubElement(p, 'Keyframes'); kf.tail = '\n'
                if isinstance(value, (tuple, list)):
                    kf.text = ('914457600000000,0.5:0.5,5,0,0,0.16666666666666666,0,0.0001,5,4,0,0,0,0;'
                               '914743368000000,0.5:0.5,5,0,0,1,0,0.16666666666666666,5,4,0,0,0,0;')
                else:
                    kf.text = ('914457600000000,100.,0,0,0,0.16666666666666666,18,0.16666666666666666;'
                               '914711616000000,100.,5,0,-0.98181818181818148,1,0,0.16666666666666666;')
            tmpl = [k for k in kf.text.strip().split(';') if k]
            out = []
            for i, (t, v) in enumerate(keyframes):
                tp = tmpl[min(i, len(tmpl) - 1)].split(',')
                tp[0] = str(int(t))
                tp[1] = self._fmt(v)
                out.append(','.join(tp))
            kf.text = ';'.join(out) + ';'
            self.set_child(p, 'IsTimeVarying', 'true')
        elif kf is not None:
            p.remove(kf)
            tv = p.find('IsTimeVarying')
            if tv is not None:
                p.remove(tv)

    # ---- captions -------------------------------------------------------
    @staticmethod
    def replace_caption_text(blob_b64, text):
        d = bytearray(base64.b64decode(blob_b64))
        i = len(d) - 4
        while i > 0:
            n = struct.unpack_from('<I', d, i)[0]
            if 1 <= n <= 200 and i + 4 + n <= len(d) and bytes(d[i + 4:i + 4 + n]).isascii():
                break
            i -= 1
        enc = text.encode('utf-8')
        tail = struct.pack('<I', len(enc)) + enc + b'\0'
        tail += b'\0' * ((-len(tail)) % 4)
        new = bytes(d[:i]) + tail
        new = struct.pack('<I', len(new) - 12) + new[4:]
        return base64.b64encode(new).decode()

    @staticmethod
    def rehash(el, mode='size12'):
        """BinaryHash = 24-hex content hash (algorithm unknown) + 8-hex (blob length + 12)."""
        if mode == 'none':
            el.attrib.pop('BinaryHash', None)
            return
        size = len(base64.b64decode(el.text)) + 12
        h = uuid.uuid4().hex[:24] + f'{size:08x}'
        el.attrib['BinaryHash'] = f'{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}'

    # ---- track list management -----------------------------------------
    def clear_track(self, te):
        for path in ('.//ClipItems/TrackItems', './/TransitionItems/TrackItems'):
            items = te.find(path)
            if items is not None:
                for x in list(items.findall('TrackItem')):
                    items.remove(x)

    def add_track_item(self, te, oid, transition=False):
        parent = te.find('.//TransitionItems' if transition else './/ClipItems')
        items = parent.find('TrackItems')
        if items is None:
            items = ET.SubElement(parent, 'TrackItems', Version='1')
            items.tail = '\n'
            parent.insert(0, items)
        n = len(items.findall('TrackItem'))
        el = ET.SubElement(items, 'TrackItem', Index=str(n), ObjectRef=str(oid))
        el.tail = '\n'

    # ---- output -----------------------------------------------------------
    def prune(self):
        """Remove objects unreachable from the project roots (Premiere writes none)."""
        self.reindex()
        seen = set()
        stack = []
        for e in self.root:
            if 'ObjectID' not in e.attrib and 'ObjectUID' not in e.attrib:
                for x in e.iter():
                    if 'ObjectRef' in x.attrib:
                        stack.append(('id', x.attrib['ObjectRef']))
                    if 'ObjectURef' in x.attrib:
                        stack.append(('uid', x.attrib['ObjectURef']))
        while stack:
            key = stack.pop()
            if key in seen:
                continue
            seen.add(key)
            el = self.byid.get(key[1]) if key[0] == 'id' else self.byuid.get(key[1])
            if el is None:
                continue
            for x in el.iter():
                if 'ObjectRef' in x.attrib:
                    stack.append(('id', x.attrib['ObjectRef']))
                if 'ObjectURef' in x.attrib:
                    stack.append(('uid', x.attrib['ObjectURef']))
        removed = 0
        for e in list(self.root):
            if 'ObjectID' in e.attrib and ('id', e.attrib['ObjectID']) not in seen:
                self.root.remove(e); removed += 1
            elif 'ObjectUID' in e.attrib and ('uid', e.attrib['ObjectUID']) not in seen:
                self.root.remove(e); removed += 1
        self.reindex()
        return removed

    # Premiere's own formatting: '<X/>' without a space, newlines inside text as '&#10;', no trailing newline
    @staticmethod
    def _esc_text(t):
        t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if t.strip():
            m = re.search(r'\n\t+$', t)   # formatting before the closing tag stays literal
            if m:
                t = t[:m.start()].replace('\n', '&#10;') + m.group(0)
            else:
                t = t.replace('\n', '&#10;')
        return t

    @staticmethod
    def _esc_attr(t):
        return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    def _serialize(self, el, out):
        out.append('<' + el.tag)
        for k, v in el.attrib.items():
            out.append(f' {k}="{self._esc_attr(v)}"')
        if len(el) == 0 and not el.text:
            out.append('/>')
        else:
            out.append('>')
            if el.text:
                out.append(self._esc_text(el.text))
            for c in el:
                self._serialize(c, out)
            out.append('</' + el.tag + '>')
        if el.tail:
            out.append(el.tail)

    def to_xml(self):
        out = ['<?xml version="1.0" encoding="UTF-8" ?>\n']
        self._serialize(self.root, out)
        return ''.join(out).rstrip('\n\t ') + '\n\n'

    def tidy(self):
        n = 0
        for parent in self.root.iter():
            for ti in list(parent.findall('TrackItems')):
                if len(ti) == 0:
                    parent.remove(ti); n += 1
        return n

    def normalize_blobs(self):
        """First occurrence of each BinaryHash (file order) must carry the data; later ones are empty refs.
        Every hash that appears inside a cloned object gets a fresh value (Premiere rejects known hashes on new objects)."""
        remap = {}
        for top in self.cloned:
            for e in top.iter():
                h = e.attrib.get('BinaryHash')
                if h and h not in remap:
                    n = uuid.uuid4().hex[:24] + h.replace('-', '')[-8:]
                    remap[h] = f'{n[:8]}-{n[8:12]}-{n[12:16]}-{n[16:20]}-{n[20:32]}'
        for top in self.root:
            for e in top.iter():
                h = e.attrib.get('BinaryHash')
                if h in remap:
                    e.attrib['BinaryHash'] = remap[h]
        for old, new in remap.items():
            if old in self.blob_table and new not in self.blob_table:
                self.blob_table[new] = self.blob_table[old]
        self._remapped = len(remap)
        seen = set(); filled = emptied = dangling = 0
        for top in self.root:
            for e in top.iter():
                h = e.attrib.get('BinaryHash')
                if not h:
                    continue
                has = bool(e.text and e.text.strip())
                if h not in seen:
                    seen.add(h)
                    if not has:
                        data = self.blob_table.get(h)
                        if data is None:
                            dangling += 1
                        else:
                            e.text = data; filled += 1
                elif has:
                    if h not in self.blob_table:
                        self.blob_table[h] = e.text
                    e.text = None; emptied += 1
        return filled, emptied, dangling

    def save(self, path):
        print('removed', self.tidy(), 'empty TrackItems;', 'pruned', self.prune(), 'unreachable objects')
        filled, emptied, dangling = self.normalize_blobs()
        print(f'blobs: re-hashed {self._remapped}, re-materialised {filled}, turned into refs {emptied}, dangling {dangling}')
        if dangling:
            raise RuntimeError('dangling BinaryHash references remain')
        xml = self.to_xml()
        with gzip.open(path, 'wb') as fh:
            fh.write(xml.encode('utf-8'))


# ------------------------------------------------------------------------------------
def build(plan):
    P = Project(plan['reference'])
    out_dir = plan['output_dir']
    media_dir = out_dir if plan.get('media_flat') else os.path.join(out_dir, 'Media')
    os.makedirs(media_dir, exist_ok=True)

    # ---------- 1. media: copy files, retarget paths ----------
    copied = {}
    import glob
    media_files = list(plan.get('media_copy', []))
    for d in plan.get('media_copy_dirs', []):
        for f in sorted(glob.glob(os.path.join(d, '*'))):
            if os.path.isfile(f) and not f.endswith('.prproj') and os.path.basename(f) not in plan.get('media_skip', []):
                media_files.append(f)
    for m in media_files:
        dst = os.path.join(media_dir, os.path.basename(m))
        if not os.path.exists(dst):
            shutil.copy2(m, dst)
        copied[os.path.basename(m)] = dst

    def repoint(media_el, filename):
        dst = copied[filename]
        P.set_child(media_el, 'FilePath', dst)
        P.set_child(media_el, 'ActualMediaFilePath', dst)
        P.set_child(media_el, 'Title', filename)

    # repoint every real media file to the delivery folder
    for e in P.root:
        if e.tag == 'Media':
            fp = e.findtext('FilePath') or ''
            base = os.path.basename(fp)
            if fp.startswith('/') and base in copied:
                repoint(e, base)
    copied_norm = {P.norm(k): v for k, v in copied.items()}
    copied.update(copied_norm)

    # retargets: existing media entry -> new file (name + stream fields)
    for rt in plan.get('retarget', []):
        med = P.media_by_title(rt['old_title'])
        old_name = rt['old_title']
        new_name = os.path.basename(rt['new_file'])
        repoint(med, new_name)
        vs = P.ref(med.find('VideoStream'))
        if vs is not None:
            if 'duration_s' in rt:
                P.set_child(vs, 'Duration', s2t(rt['duration_s']))
            if 'frame_rect' in rt:
                P.set_child(vs, 'FrameRect', rt['frame_rect'])
        aus = P.ref(med.find('AudioStream'))
        if aus is not None:
            if 'duration_s' in rt:
                P.set_child(aus, 'Duration', s2t(rt['duration_s']))
            if 'audio_rate' in rt:
                P.set_child(aus, 'FrameRate', TICKS // rt['audio_rate'])
            pk = aus.find('PeakFilePath')
            if pk is not None:
                aus.remove(pk)
        # names in master clip + bin
        try:
            P.set_child(P.masterclip_by_name(old_name), 'Name', new_name)
        except KeyError:
            pass
        try:
            pi = P.projectitem_by_name(old_name)
            P.set_child(pi.find('ProjectItem'), 'Name', new_name)
        except KeyError:
            pass
        # timeline clip names (SubClip) that point at this master clip
        try:
            mcu = P.masterclip_by_name(new_name).attrib['ObjectUID']
            for e in P.root:
                if e.tag == 'SubClip' and e.find('MasterClip') is not None and e.find('MasterClip').attrib.get('ObjectURef') == mcu:
                    P.set_child(e, 'Name', new_name)
        except KeyError:
            pass
        # original duration on every media source pointing at this media
        if 'duration_s' in rt:
            uid = med.attrib['ObjectUID']
            for e in P.root:
                if e.tag in ('VideoMediaSource', 'AudioMediaSource'):
                    m = e.find('.//Media')
                    if m is not None and m.attrib.get('ObjectURef') == uid:
                        P.set_child(e, 'OriginalDuration', s2t(rt['duration_s']))

    # new media cloned from an exemplar (e.g. alpha ProRes from the loader)
    new_media_uids = {}
    for nm in plan.get('new_media', []):
        pi = P.projectitem_by_name(nm['exemplar_title'])
        # clone the project item closure following UID refs (MasterClip, Media)
        ids, uids = [], []
        P.uclosure(pi.attrib['ObjectUID'], ids, ('ClipProjectItem', 'MasterClip', 'Media'), uids)
        idmap = {o: P.new_id() for o in ids}
        uidmap = {u: str(uuid.uuid4()) for u in uids}
        for o in ids:
            P._add_clone(P.byid[o], idmap, uidmap)
        for u in uids:
            P._add_clone(P.byuid[u], idmap, uidmap)
        new_pi = P.byuid[uidmap[pi.attrib['ObjectUID']]]
        new_name = os.path.basename(nm['new_file'])
        P.set_child(new_pi.find('ProjectItem'), 'Name', new_name)
        mc = P.ref(new_pi.find('MasterClip'))
        P.set_child(mc, 'Name', new_name)
        clip = P.ref(mc.find('Clips/Clip'))
        src = P.ref(clip.find('.//Source'))
        med = P.ref(src.find('.//Media'))
        repoint(med, new_name)
        P.set_child(src, 'OriginalDuration', s2t(nm['duration_s']))
        vs = P.ref(med.find('VideoStream'))
        P.set_child(vs, 'Duration', s2t(nm['duration_s']))
        P.set_child(vs, 'FrameRect', nm['frame_rect'])
        P.set_child(vs, 'FrameRate', FT)
        # register in root bin
        rp = [e for e in P.root if e.tag == 'RootProjectItem'][0]
        items = rp.find('.//ProjectItemContainer/Items')
        n = len(items.findall('Item'))
        it = ET.SubElement(items, 'Item', Index=str(n), ObjectURef=new_pi.attrib['ObjectUID'])
        it.tail = '\n'
        new_media_uids[nm['key']] = dict(media=med.attrib['ObjectUID'], masterclip=mc.attrib['ObjectUID'], name=new_name)

    # ---------- 2. exemplars ----------
    EX = {}
    for key, spec in plan['exemplars'].items():
        EX[key] = P.find_item(spec['kind'], spec['track'], spec['start'])

    # ---------- 3. clear every track ----------
    for kind in ('video', 'audio'):
        grp = [e for e in P.root if e.tag == ('VideoTrackGroup' if kind == 'video' else 'AudioTrackGroup')][0]
        for t in grp.find('TrackGroup/Tracks').findall('Track'):
            te = P.ref(t)
            if te is not None:
                P.clear_track(te)
    for e in P.root:
        if e.tag == 'CaptionDataClipTrack':
            P.clear_track(e)

    # ---------- 4. build items ----------
    seq = [e for e in P.root if e.tag == 'Sequence'][0]
    links_el = seq.find('.//Links')
    if links_el is not None:
        for x in list(links_el):
            links_el.remove(x)
    link_groups = {}
    for it in plan['items']:
        kind = it['kind']
        te = P.track(kind if kind != 'graphic' else 'video', it['track'])
        ex = EX[it['exemplar']]
        follow = ('Media', 'MasterClip') if (kind == 'caption' and not plan.get('caption_share_media')) else ()
        idmap, uidmap = P.clone(ex.attrib['ObjectID'], follow_uid_tags=follow)
        new = P.byid[idmap[ex.attrib['ObjectID']]]
        s_f, e_f = it['start_f'], it['end_f']
        dur_t = f2t(e_f - s_f)
        if 'in_s' in it:
            in_t = s2t(it['in_s'])
        elif 'in_f' in it:
            in_t = f2t(it['in_f'])
        else:
            in_t = H3600 + (f2t(s_f) if kind == 'caption' else 0)
        P.set_item_times(new, f2t(s_f), f2t(e_f), in_t, in_t + dur_t)

        if it.get('media_key'):
            nmu = new_media_uids[it['media_key']]
            sub = P.ref(new.find('.//SubClip'))
            sub.find('MasterClip').attrib['ObjectURef'] = nmu['masterclip']
            P.set_child(sub, 'Name', nmu['name'])
            clip = P.ref(sub.find('Clip'))
            src = P.ref(clip.find('.//Source'))
            src.find('.//Media').attrib['ObjectURef'] = nmu['media']
            nm_spec = [n for n in plan['new_media'] if n['key'] == it['media_key']][0]
            P.set_child(src, 'OriginalDuration', s2t(nm_spec['duration_s']))

        if it.get('media_title'):
            mc = P.masterclip_by_name(it['media_title'])
            med = P.media_by_title(it['media_title'])
            sub = P.ref(new.find('.//SubClip'))
            sub.find('MasterClip').attrib['ObjectURef'] = mc.attrib['ObjectUID']
            P.set_child(sub, 'Name', it['media_title'])
            clip = P.ref(sub.find('Clip'))
            src = P.ref(clip.find('.//Source'))
            src.find('.//Media').attrib['ObjectURef'] = med.attrib['ObjectUID']

        # clip frame rect must match the media's native size (e.g. 720x1280 sources)
        if kind == 'video':
            sub = P.ref(new.find('.//SubClip'))
            clip = P.ref(sub.find('Clip'))
            src = P.ref(clip.find('.//Source'))
            med = P.ref(src.find('.//Media'))
            vs = P.ref(med.find('VideoStream')) if med is not None and med.find('VideoStream') is not None else None
            if vs is not None and vs.findtext('FrameRect') and new.find('FrameRect') is not None:
                new.find('FrameRect').text = vs.findtext('FrameRect')

        if kind in ('video', 'graphic'):
            for pname, val in it.get('motion', {}).items():
                kfs = None
                if isinstance(val, dict):
                    kfs = [(in_t + f2t(t), v) for t, v in val['keyframes']]
                    val = val['keyframes'][0][1]
                mn = 'AE.ADBE Graphic Group' if kind == 'graphic' else 'AE.ADBE Motion'
                P.set_param(new, mn, pname, val, kfs)
        if kind == 'audio':
            sub = P.ref(new.find('.//SubClip'))
            aclip = P.ref(sub.find('Clip'))
            if it.get('gain_db'):
                P.set_child(aclip, 'Gain', repr(10 ** (it['gain_db'] / 20.0)))
            # audio transitions cloned with the clip (fade in/out): re-register or drop them
            for tag, head in (('HeadTransition', True), ('TailTransition', False)):
                tr_ref = new.find('.//' + tag)
                if tr_ref is None:
                    continue
                tr = P.ref(tr_ref)
                nfade = it.get('fade_in_f' if head else 'fade_out_f', 0)
                if not nfade or tr is None:
                    new.find('.//ClipTrackItem').remove(tr_ref)
                    continue
                tti = tr.find('.//TrackItem')
                if head:
                    P.set_child(tti, 'Start', f2t(s_f), before='End'); P.set_child(tti, 'End', f2t(s_f + nfade))
                else:
                    P.set_child(tti, 'Start', f2t(e_f - nfade), before='End'); P.set_child(tti, 'End', f2t(e_f))
                P.set_child(tr, 'Alignment', f2t(nfade)) if tr.find('Alignment') is not None else None
                P.add_track_item(te, tr.attrib['ObjectID'], transition=True)
        if kind == 'caption':
            blk = P.ref(new.find('BlockVector/BlockVectorItem'))
            ftd = blk.find('FormattedTextData')
            mode = plan.get('blob_mode', 'size12')
            if mode not in ('keep', 'rehash'):
                ftd.text = P.replace_caption_text(ftd.text, it['text'])
            if 'y' in it and mode not in ('keep', 'rehash'):
                d = bytearray(base64.b64decode(ftd.text))
                cur = struct.unpack_from('<f', d, 232)[0]
                if -0.7 < cur < -0.2:   # standard caption blob family: float @232 maps y=0.385 -> -0.5521, y=0.70 -> -0.2307
                    struct.pack_into('<f', d, 232, (it['y'] - 0.385) / 0.98 - 0.5521)
                    ftd.text = base64.b64encode(bytes(d)).decode()
            if mode != 'keep':
                P.rehash(ftd, mode)
        P.add_track_item(te, new.attrib['ObjectID'])
        if it.get('link'):
            link_groups.setdefault(it['link'], []).append(new.attrib['ObjectID'])

        if kind == 'graphic' and it.get('title'):
            # rewrite the Source Text blob: text is the last length-prefixed string, box auto-fits
            for ce in P.components(new):
                if ce.findtext('MatchName') != 'AE.ADBE Text':
                    continue
                for pr in ce.find('.//Params').findall('Param'):
                    p = P.ref(pr)
                    if p is not None and p.findtext('Name') == 'Source Text':
                        skv = p.find('StartKeyframeValue')
                        mode = plan.get('blob_mode', 'size12')
                        if mode not in ('keep', 'rehash'):
                            skv.text = P.replace_caption_text(skv.text, it['title']['text'])
                        if mode != 'keep':
                            P.rehash(skv, mode)
        if kind == 'graphic':
            # the text-animator "in" transition that was cloned with the clip
            trans = [P.byid[idmap[o]] for o in idmap if P.byid[idmap[o]].tag == 'VideoTransitionTrackItem']
            if trans:
                tr = trans[0]
                tdur = it.get('anim_in_f')
                if tdur is None:
                    tdur = min(18, max(4, round((e_f - s_f) * 0.4)))
                tti = tr.find('.//TrackItem')
                P.set_child(tti, 'Start', f2t(s_f), before='End')
                P.set_child(tti, 'End', f2t(s_f + tdur))
                P.add_track_item(te, tr.attrib['ObjectID'], transition=True)

    # linked video/audio groups
    if links_el is not None:
        for gi, (gname, ids) in enumerate(link_groups.items()):
            lk = ET.Element('Link', ObjectID=P.new_id(), ClassID='149d4ea5-a7d4-4b34-9bb7-16d783904bf2', Version='1')
            tig = ET.SubElement(lk, 'TrackItemGroup', Version='1')
            tis = ET.SubElement(tig, 'TrackItems', Version='1')
            for i, oid in enumerate(ids):
                ET.SubElement(tis, 'TrackItem', Index=str(i), ObjectRef=oid).tail = '\n'
            lk.tail = '\n\t'
            P.root.append(lk)
            P.byid[lk.attrib['ObjectID']] = lk
            ET.SubElement(links_el, 'Link', Index=str(gi), ObjectRef=lk.attrib['ObjectID']).tail = '\n'

    # ---------- 5. sequence housekeeping ----------
    total_t = f2t(plan['total_frames'])
    for tag, val in (('MZ.WorkOutPoint', total_t), ('Monitor.ProgramZoomOut', total_t), ('MZ.EditLine', 0), ('MZ.WorkInPoint', 0)):
        el = seq.find('.//' + tag)
        if el is not None:
            el.text = str(val)
    P.set_child(seq, 'Name', plan['sequence_name'])
    try:
        pi = P.projectitem_by_name(plan['old_sequence_name'])
        P.set_child(pi.find('ProjectItem'), 'Name', plan['sequence_name'])
    except KeyError:
        pass

    out = os.path.join(out_dir, plan['project_name'] + '.prproj')
    P.save(out)
    return out


if __name__ == '__main__':
    plan = json.load(open(sys.argv[1]))
    print(build(plan))
