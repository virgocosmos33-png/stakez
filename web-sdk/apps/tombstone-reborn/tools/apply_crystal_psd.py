"""Write Crystal 2x layers into western_scene2.psd via Photoshop COM."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from restore_crystal_layers import READY, SCALE, SRC
from export_western_scene2 import PSD_NAME, RAW

DESK = Path.home() / "Desktop" / PSD_NAME
CANVAS_W = 1342 * SCALE
CANVAS_H = 892 * SCALE


def js_escape(path: Path) -> str:
	return str(path.resolve()).replace("\\", "/")


def build_jsx() -> str:
	manifest = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))
	entries = []
	for item in manifest:
		png = READY / f"{item['slug']}.png"
		if not png.is_file():
			continue
		x0, y0, _, _ = item["bbox"]
		entries.append(
			{
				"name": item["name"],
				"slug": item["slug"],
				"file": js_escape(png),
				"x": int(round(x0 * SCALE)),
				"y": int(round(y0 * SCALE)),
			}
		)
	src = DESK if DESK.is_file() else (RAW / PSD_NAME)
	payload = json.dumps(entries)
	return f"""
#target photoshop
app.displayDialogs = DialogModes.NO;
var src = new File("{js_escape(src)}");
if (!src.exists) {{ throw new Error("missing PSD " + src.fsName); }}
var doc = app.open(src);
doc.resizeImage(UnitValue({CANVAS_W}, "px"), UnitValue({CANVAS_H}, "px"), doc.resolution, ResampleMethod.BICUBICSHARPER);
var maps = {payload};

function findLayer(layers, name, skip) {{
  var n = 0;
  for (var i = 0; i < layers.length; i++) {{
    var L = layers[i];
    if (L.typename === "LayerSet") {{
      var hit = findLayer(L.layers, name, skip);
      if (hit) return hit;
    }} else if (L.name === name) {{
      if (n === skip) return L;
      n++;
    }}
  }}
  return null;
}}

var used = {{}};
for (var i = 0; i < maps.length; i++) {{
  var m = maps[i];
  var skip = used[m.name] || 0;
  used[m.name] = skip + 1;
  var layer = findLayer(doc.layers, m.name, skip);
  if (!layer) {{
    $.writeln("missing layer " + m.name + " / " + m.slug);
    continue;
  }}
  doc.activeLayer = layer;
  var f = new File(m.file);
  if (!f.exists) {{ throw new Error("missing PNG " + m.file); }}
  var placed = new File(m.file);
  app.open(placed);
  app.activeDocument.selection.selectAll();
  app.activeDocument.selection.copy();
  app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
  doc.selection.selectAll();
  doc.paste();
  var pasted = doc.activeLayer;
  pasted.translate(m.x - pasted.bounds[0].as("px"), m.y - pasted.bounds[1].as("px"));
  pasted.merge();
  $.writeln("replaced " + m.slug);
}}

var destDesk = new File("{js_escape(DESK)}");
var destRaw = new File("{js_escape(RAW / PSD_NAME)}");
doc.saveAs(destDesk, new PhotoshopSaveOptions(), true);
doc.saveAs(destRaw, new PhotoshopSaveOptions(), true);
doc.close(SaveOptions.DONOTSAVECHANGES);
"ok {CANVAS_W}x{CANVAS_H}";
"""


def main() -> None:
	READY.mkdir(parents=True, exist_ok=True)
	jsx_path = RAW / "_apply_crystal.jsx"
	jsx_path.write_text(build_jsx(), encoding="utf-8")
	try:
		import win32com.client
	except ImportError as exc:
		raise SystemExit(f"win32com missing: {exc}") from exc
	ps = win32com.client.Dispatch("Photoshop.Application")
	ps.DoJavaScript(jsx_path.read_text(encoding="utf-8"))
	print(f"wrote {DESK} and {RAW / PSD_NAME} at {CANVAS_W}x{CANVAS_H}")


if __name__ == "__main__":
	main()
