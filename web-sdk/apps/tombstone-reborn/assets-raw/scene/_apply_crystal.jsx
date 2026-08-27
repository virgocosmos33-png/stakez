
#target photoshop
app.displayDialogs = DialogModes.NO;
var src = new File("C:/Users/Emex33/Desktop/western_scene2.psd");
if (!src.exists) { throw new Error("missing PSD " + src.fsName); }
var doc = app.open(src);
doc.resizeImage(UnitValue(2684, "px"), UnitValue(1784, "px"), doc.resolution, ResampleMethod.BICUBICSHARPER);
var maps = [{"name": "background", "slug": "background", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/background.png", "x": 0, "y": 0}, {"name": "post_R", "slug": "post_r", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/post_r.png", "x": 2418, "y": 24}, {"name": "post_R", "slug": "post_r_2", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/post_r_2.png", "x": -108, "y": 26}, {"name": "beam", "slug": "beam", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/beam.png", "x": 36, "y": 70}, {"name": "signpost", "slug": "signpost", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/signpost.png", "x": 36, "y": 780}, {"name": "wagon_wheel", "slug": "wagon_wheel", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/wagon_wheel.png", "x": 262, "y": 1294}, {"name": "barrel", "slug": "barrel", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/barrel.png", "x": 2464, "y": 1178}, {"name": "tombstone", "slug": "tombstone", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/tombstone.png", "x": 2082, "y": 1222}, {"name": "right  hanging lamp", "slug": "right_hanging_lamp", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/right_hanging_lamp.png", "x": 2376, "y": 146}, {"name": "left hanging lamp", "slug": "left_hanging_lamp", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/left_hanging_lamp.png", "x": 196, "y": 146}, {"name": "lantern_dim", "slug": "lantern_dim", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/lantern_dim.png", "x": 2566, "y": 918}, {"name": "rock_02", "slug": "rock_02", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/rock_02.png", "x": 1972, "y": 1620}, {"name": "rock", "slug": "rock", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/rock.png", "x": 2024, "y": 1704}, {"name": "rock_03", "slug": "rock_03", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/rock_03.png", "x": 1986, "y": 1652}, {"name": "rocks", "slug": "rocks", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/rocks.png", "x": 764, "y": 1458}, {"name": "shrub", "slug": "shrub", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/shrub.png", "x": 2058, "y": 1540}, {"name": "grass_03", "slug": "grass_03", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/grass_03.png", "x": 1640, "y": 1350}, {"name": "grass_02", "slug": "grass_02", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/grass_02.png", "x": 2630, "y": 1138}, {"name": "rocks_02", "slug": "rocks_02", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/rocks_02.png", "x": 114, "y": 1522}, {"name": "grass", "slug": "grass", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/grass.png", "x": 2250, "y": 1576}, {"name": "cowboy_hat", "slug": "cowboy_hat", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/cowboy_hat.png", "x": 2418, "y": 1668}, {"name": "skull", "slug": "skull", "file": "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/crystal_ready/skull.png", "x": 8, "y": 1348}];

function findLayer(layers, name, skip) {
  var n = 0;
  for (var i = 0; i < layers.length; i++) {
    var L = layers[i];
    if (L.typename === "LayerSet") {
      var hit = findLayer(L.layers, name, skip);
      if (hit) return hit;
    } else if (L.name === name) {
      if (n === skip) return L;
      n++;
    }
  }
  return null;
}

var used = {};
for (var i = 0; i < maps.length; i++) {
  var m = maps[i];
  var skip = used[m.name] || 0;
  used[m.name] = skip + 1;
  var layer = findLayer(doc.layers, m.name, skip);
  if (!layer) {
    $.writeln("missing layer " + m.name + " / " + m.slug);
    continue;
  }
  doc.activeLayer = layer;
  var f = new File(m.file);
  if (!f.exists) { throw new Error("missing PNG " + m.file); }
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
}

var destDesk = new File("C:/Users/Emex33/Desktop/western_scene2.psd");
var destRaw = new File("C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/western_scene2.psd");
doc.saveAs(destDesk, new PhotoshopSaveOptions(), true);
doc.saveAs(destRaw, new PhotoshopSaveOptions(), true);
doc.close(SaveOptions.DONOTSAVECHANGES);
"ok 2684x1784";
