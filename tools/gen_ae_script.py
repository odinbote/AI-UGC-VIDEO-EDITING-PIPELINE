#!/usr/bin/env python3
"""
Writes the After Effects build script for a reel in Abik's manual-edit look.

I cannot run After Effects, so the editable .aep is made by a script Abik runs once
(File > Scripts > Run Script File). The script creates a new project, builds one comp per number card
(and the cover ring when the reel has one), saves "<reel>.aep" next to itself and writes ae_comp_ids.json
with each comp's item id. Premiere's Dynamic Link finds a comp by that id, so tools/build_manual_prproj.py
reads the file and swaps the rendered card clips for the linked comps.

    python3 tools/gen_ae_script.py 13
"""
import os, sys, json, importlib, shutil, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manual_look as ML, manual_reel as MR
from PIL import Image

ROOT = "/Users/abiknewar/Work/Claude Editing 2"
FD = "1001/24000"            # one frame, seconds (23.976 fps comps, like his)


def js(v):
    return json.dumps(v)


def card_js(bi, b, reel_no, footage_dir, comp_no):
    n = b['src'][1] - b['src'][0]
    num_col, ink = MR.CARD_COL[b.get('n') or b.get('col')]
    title = ' '.join(t for t, _, _ in b['lines'])
    name = f"Fanout Reel {reel_no} Linked Comp {comp_no:02d}"          # his naming: "<project> Linked Comp NN"
    cov_name = os.path.basename(b['cover'])
    shutil.copy2(b['cover'], os.path.join(footage_dir, cov_name))
    cw, chh = Image.open(b['cover']).size
    L = [f'  // ---------------- {name}',
         f'  // {title}',
         f'  c = addComp({js(name)}, {n});',
         f'  solid(c, {js([round(x / 255, 4) for x in MR.BG])}, "Background");']
    if b.get('n'):
        size = 2650; cap = 0.705 * size
        L.append(f'  text(c, {js(str(b["n"]))}, {size}, {js([round(x / 255, 4) for x in num_col])}, 0, {round(0.56 * ML.W, 1)}, {round(0.5 * ML.H + cap / 2, 1)}, null, {js(str(b["n"]))});')
    # cover: slides in from the left over 9 frames, easing out, with a small rotation that settles
    scale = round(450 / chh * 100, 3)
    pos, rot = [], []
    for lf in range(0, 9):
        p = 1 - (1 - min(1.0, (lf + 1) / 9)) ** 3
        pos.append([lf, [round((-0.25 + 0.75 * p) * ML.W, 1), round(0.40 * ML.H, 1)]]); rot.append([lf, round(-(1 - p) * 14, 2)])
    L.append(f'  cover(c, {js(cov_name)}, {scale}, {js(pos)}, {js(rot)});')
    y = 0.545
    for text, kind, s0 in b['lines']:
        if kind == 'lead':
            size, track = 62, -20; base = y + 0.705 * size / ML.H; y = base + 0.012
        else:
            size, track = ML.fit_size(text, MR.FONT_BOLD, 230, 0.79 * ML.W, -30), -30; base = y + 0.705 * size / ML.H; y = base + 0.013
        f0 = s0 - b['src'][0]
        L.append(f'  text(c, {js(text)}, {size}, {js([round(x / 255, 4) for x in ink])}, {track}, {ML.W / 2}, {round(base * ML.H, 1)}, {f0}, {js(text)});')
    L.append(f'  ids.push([{js(name)}, c.id, {bi}]);')
    return name, title, n, cov_name, '\n'.join(L)


HEAD = r'''// Build script for the editable After Effects project of %(reel)s (Abik's manual-edit look).
// Run once: File > Scripts > Run Script File... It makes a NEW project, so save your open project first.
(function () {
  var here = new File($.fileName).parent;
  var FD = %(fd)s, W = 1080, H = 1920, FONT = "SFPro-Bold";
  if (app.project && app.project.numItems > 0) {
    if (!confirm("This builds a new After Effects project for %(reel)s.\nSave your current project first.\n\nContinue?")) { return; }
  }
  app.newProject();
  var footage = {}, ids = [], c;

  function addComp(name, frames) {
    var comp = app.project.items.addComp(name, W, H, 1, frames * FD, 1 / FD);
    comp.bgColor = [0.965, 0.965, 0.976];
    return comp;
  }
  function solid(comp, rgb, name) {
    var l = comp.layers.addSolid(rgb, name, W, H, 1, comp.duration);
    return l;
  }
  // centred text with its baseline at (x, y); startFrame = frame it appears on (4-frame fade), null = always on
  function text(comp, str, size, rgb, tracking, x, y, startFrame, name) {
    var l = comp.layers.addText(str);
    var prop = l.property("Source Text"), td = prop.value;
    td.resetCharStyle();
    td.font = FONT; td.fontSize = size; td.applyFill = true; td.fillColor = rgb; td.applyStroke = false; td.tracking = tracking;
    td.justification = ParagraphJustification.CENTER_JUSTIFY;
    prop.setValue(td);
    l.name = name;
    l.property("Position").setValue([x, y]);
    if (startFrame !== null) {
      var op = l.property("Opacity");
      if (startFrame > 0) { op.setValueAtTime((startFrame - 1) * FD, 0); }
      op.setValueAtTime(startFrame * FD, 25);
      op.setValueAtTime((startFrame + 3) * FD, 100);
      // the word arrives through a short lens blur, as in Abik's comps (Camera Lens Blur)
      try {
        var fx = l.property("ADBE Effect Parade").addProperty("ADBE Camera Lens Blur");
        var rad = fx.property(1);
        rad.setValueAtTime(startFrame * FD, 18);
        rad.setValueAtTime((startFrame + 4) * FD, 0);
      } catch (e) {}
    }
    return l;
  }
  function importOnce(file) {
    if (!footage[file]) { footage[file] = app.project.importFile(new ImportOptions(new File(here.fsName + "/(Footage)/" + file))); }
    return footage[file];
  }
  function cover(comp, file, scale, pos, rot) {
    var l = comp.layers.add(importOnce(file)), i;
    l.name = "Cover";
    l.property("Scale").setValue([scale, scale]);
    for (i = 0; i < pos.length; i++) { l.property("Position").setValueAtTime(pos[i][0] * FD, pos[i][1]); }
    for (i = 0; i < rot.length; i++) { l.property("Rotation").setValueAtTime(rot[i][0] * FD, rot[i][1]); }
    return l;
  }

'''

TAIL = r'''
  // ---------------- save, and tell Premiere which comp is which
  var aep = new File(here.fsName + "/%(reel)s.aep");
  app.project.save(aep);
  var out = "[", i;
  for (i = 0; i < ids.length; i++) { out += (i ? "," : "") + '{"name":"' + ids[i][0] + '","id":' + ids[i][1] + ',"beat":' + ids[i][2] + "}"; }
  out += "]";
  var wrote = false;
  try {
    var f = new File(here.fsName + "/ae_comp_ids.json");
    f.encoding = "UTF-8";
    if (f.open("w")) { f.write(out); f.close(); wrote = true; }
  } catch (e) {}
  if (wrote) {
    alert("%(reel)s.aep is saved with " + ids.length + " comp(s).\n\nTell Claude it is done, and the Premiere project gets linked to these comps.");
  } else {
    alert("%(reel)s.aep is saved, but After Effects did not let the script write a file\n(Settings > Scripting & Expressions > Allow Scripts to Write Files).\n\nSend this line to Claude instead:\n\n" + out);
  }
})();
'''


def build(reel_no):
    """Folder laid out like Abik's collected AE folder: "<project> folder/" with the .aep, "(Footage)/" and "<project>Report.txt"."""
    gen = importlib.import_module(f"gen_reel{reel_no}")
    reel = f"Fanout Reel {reel_no}"
    out_dir = os.path.join(ROOT, reel, f"{reel} AE folder"); footage_dir = os.path.join(out_dir, "(Footage)")
    os.makedirs(footage_dir, exist_ok=True)
    parts, comps, footage = [], [], []
    for bi, b in enumerate(gen.BEATS):
        if b['type'] == 'card':
            nm, title, n, cov, code = card_js(bi, b, reel_no, footage_dir, len(comps) + 1)
            comps.append((nm, title, n)); parts.append(code)
            if cov not in footage: footage.append(cov)
    path = os.path.join(out_dir, f"Build {reel} AE.jsx")
    open(path, 'w').write(HEAD % {"reel": reel, "fd": FD} + '\n\n'.join(parts) + '\n' + TAIL % {"reel": reel})
    rep = [f"Project name: \t{reel}.aep", f"Source files collected to: \t{out_dir}", "Source files collected: All", "", "Collected comps:  "]
    rep += [f"\t{nm}   ({title}, {n} frames at 23.976 fps, 1080x1920)" for nm, title, n in comps]
    rep += ["", f"Number of collected files:  {len(footage)}", "", "Collected source files: "] + [f"\t(Footage)/{f}" for f in footage]
    rep += ["", "Rendering plug-ins:", "\tClassic 3D", "", "Effects used:  1", "Effect:  Camera Lens Blur", "", "Layer:  Text Layer", "",
            "External dependencies:  ", "\tFont family: \u201cSF Pro\u201d, Font style: \u201cBold\u201d", "",
            "How this project is made:", f"\tThe .aep is written by After Effects when \"Build {reel} AE.jsx\" is run once",
            "\t(File > Scripts > Run Script File). The script also writes ae_comp_ids.json, which the Premiere project builder", "\tuses to Dynamic Link each comp."]
    open(os.path.join(out_dir, f"{reel}Report.txt"), 'w').write('\n'.join(rep) + '\n')
    return path, [c[0] + '  = ' + c[1] for c in comps]


if __name__ == '__main__':
    p, names = build(int(sys.argv[1]))
    print(p); [print('  comp:', n) for n in names]
