// Build script for the editable After Effects project of Fanout Reel 13 (Abik's manual-edit look).
// Run once: File > Scripts > Run Script File... It makes a NEW project, so save your open project first.
(function () {
  var here = new File($.fileName).parent;
  var FD = 1001/24000, W = 1080, H = 1920, FONT = "SFPro-Bold";
  if (app.project && app.project.numItems > 0) {
    if (!confirm("This builds a new After Effects project for Fanout Reel 13.\nSave your current project first.\n\nContinue?")) { return; }
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

  // ---------------- Fanout Reel 13 Linked Comp 01
  // AI ENGINEERING
  c = addComp("Fanout Reel 13 Linked Comp 01", 27);
  solid(c, [0.9647, 0.9647, 0.9765], "Background");
  cover(c, "Group 1321316775.png", 34.091, [[0, [-28.9, 768.0]], [1, [158.9, 768.0]], [2, [300.0, 768.0]], [3, [401.1, 768.0]], [4, [468.9, 768.0]], [5, [510.0, 768.0]], [6, [531.1, 768.0]], [7, [538.9, 768.0]], [8, [540.0, 768.0]]], [[0, -9.83], [1, -6.59], [2, -4.15], [3, -2.4], [4, -1.23], [5, -0.52], [6, -0.15], [7, -0.02], [8, -0.0]]);
  text(c, "AI", 230, [0.1725, 0.549, 0.5137], -30, 540.0, 1208.6, 2, "AI");
  text(c, "ENGINEERING", 136, [0.1725, 0.549, 0.5137], -30, 540.0, 1329.4, 10, "ENGINEERING");
  ids.push(["Fanout Reel 13 Linked Comp 01", c.id, 5]);

  // ---------------- save, and tell Premiere which comp is which
  var aep = new File(here.fsName + "/Fanout Reel 13.aep");
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
    alert("Fanout Reel 13.aep is saved with " + ids.length + " comp(s).\n\nTell Claude it is done, and the Premiere project gets linked to these comps.");
  } else {
    alert("Fanout Reel 13.aep is saved, but After Effects did not let the script write a file\n(Settings > Scripting & Expressions > Allow Scripts to Write Files).\n\nSend this line to Claude instead:\n\n" + out);
  }
})();
