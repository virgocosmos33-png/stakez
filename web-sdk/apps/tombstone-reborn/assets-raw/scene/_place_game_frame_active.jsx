#target photoshop
app.displayDialogs = DialogModes.NO;
app.preferences.rulerUnits = Units.PIXELS;

var LOG = new File("C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/_game_frame_place_log.txt");
var SPR = "C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets/sprites/";
var OUT_1X = new File("C:/Users/Emex33/Desktop/western_scene2.1x.psd");
var OUT_1X_RAW = new File("C:/Users/Emex33/Documents/tombstone reborn/web-sdk/apps/tombstone-reborn/assets-raw/scene/western_scene2.1x.psd");

function log(msg) {
    LOG.open("a");
    LOG.writeln(msg);
    LOG.close();
}

function px(u) {
    try { return u.as("px"); } catch (e) { return Number(u); }
}

function findSet(container, name) {
    var i;
    for (i = 0; i < container.layerSets.length; i++) {
        if (container.layerSets[i].name === name) return container.layerSets[i];
    }
    return null;
}

function deleteGameFrame(doc) {
    var g = findSet(doc, "GAME FRAME");
    if (g) {
        g.remove();
        log("removed existing GAME FRAME");
    }
}

function addPngLayer(doc, group, pngPath, layerName, left, top, tw, th) {
    tw = Math.max(1, Math.round(tw));
    th = Math.max(1, Math.round(th));
    left = Math.round(left);
    top = Math.round(top);
    var src = app.open(new File(pngPath));
    app.preferences.rulerUnits = Units.PIXELS;
    src.resizeImage(new UnitValue(tw, "px"), new UnitValue(th, "px"), src.resolution, ResampleMethod.BICUBIC);
    src.layers[0].duplicate(doc, ElementPlacement.PLACEATBEGINNING);
    src.close(SaveOptions.DONOTSAVECHANGES);
    app.activeDocument = doc;
    var lyr = doc.activeLayer;
    lyr.name = layerName;
    lyr.move(group, ElementPlacement.INSIDE);
    var b = lyr.bounds;
    lyr.translate(left - px(b[0]), top - px(b[1]));
    log("placed " + layerName + " @ " + left + "," + top + " " + tw + "x" + th);
    return lyr;
}

if (LOG.exists) LOG.remove();
LOG.open("w");
LOG.writeln("start");
LOG.close();

if (app.documents.length < 1) {
    log("ERROR no open document");
    throw new Error("no open document");
}

var doc = app.activeDocument;
app.activeDocument = doc;
var w = px(doc.width);
var h = px(doc.height);
var full = "";
try { full = String(doc.fullName.fsName); } catch (e) { full = "(unsaved)"; }
log("doc=" + doc.name);
log("path=" + full);
log("canvas=" + w + "x" + h);

var s = w / 2684.0;
log("scale=" + s);

deleteGameFrame(doc);

var gf = doc.layerSets.add();
gf.name = "GAME FRAME";
try {
    if (doc.layers.length > 1) {
        gf.move(doc.layers[0], ElementPlacement.PLACEBEFORE);
    }
} catch (eMove) {
    log("move-top warn " + eMove);
}

var chains = gf.layerSets.add();
chains.name = "CHAINS";
var board = gf.layerSets.add();
board.name = "BOARD";
var ways = gf.layerSets.add();
ways.name = "WAYS";
var multi = gf.layerSets.add();
multi.name = "MULTI";
var win = gf.layerSets.add();
win.name = "WIN";
log("groups created");

function seat(L, T, R, B) {
    return { l: L * s, t: T * s, w: (R - L) * s, h: (B - T) * s };
}

var bf = seat(673, 147, 2010, 1312);
var waysBox = seat(1343, 75, 1713, 306);
var waysPal = seat(1340, 117, 1717, 163);
var multiBox = seat(1654, 75, 2024, 306);
var multiPal = seat(1650, 117, 2027, 163);
var winBox = seat(1343, 1045, 1713, 1276);
var winPal = seat(1340, 1087, 1717, 1133);

addPngLayer(doc, board, SPR + "board/board_frame.png", "board_frame", bf.l, bf.t, bf.w, bf.h);
addPngLayer(doc, ways, SPR + "tombstone/wood_readout_ways.png", "ways_box", waysBox.l, waysBox.t, waysBox.w, waysBox.h);
addPngLayer(doc, ways, SPR + "tombstone/wood_pallet_ways.png", "ways_pallet", waysPal.l, waysPal.t, waysPal.w, waysPal.h);
addPngLayer(doc, multi, SPR + "tombstone/wood_readout_multi.png", "multi_box", multiBox.l, multiBox.t, multiBox.w, multiBox.h);
addPngLayer(doc, multi, SPR + "tombstone/wood_pallet_multi.png", "multi_pallet", multiPal.l, multiPal.t, multiPal.w, multiPal.h);
addPngLayer(doc, win, SPR + "tombstone/wood_readout_win.png", "win_box", winBox.l, winBox.t, winBox.w, winBox.h);
addPngLayer(doc, win, SPR + "tombstone/wood_pallet_win.png", "win_pallet", winPal.l, winPal.t, winPal.w, winPal.h);

var ch = SPR + "tombstone/hud_chain.png";
var c;
c = seat(1436, 70, 1457, 129);
addPngLayer(doc, chains, ch, "chain_ways_l", c.l, c.t, c.w, c.h);
c = seat(1599, 70, 1620, 129);
addPngLayer(doc, chains, ch, "chain_ways_r", c.l, c.t, c.w, c.h);
c = seat(1747, 70, 1768, 129);
addPngLayer(doc, chains, ch, "chain_multi_l", c.l, c.t, c.w, c.h);
c = seat(1910, 70, 1931, 129);
addPngLayer(doc, chains, ch, "chain_multi_r", c.l, c.t, c.w, c.h);
c = seat(1436, 992, 1457, 1092);
addPngLayer(doc, chains, ch, "chain_win_l", c.l, c.t, c.w, c.h);
c = seat(1599, 992, 1620, 1092);
addPngLayer(doc, chains, ch, "chain_win_r", c.l, c.t, c.w, c.h);
c = seat(837, 148, 854, 421);
addPngLayer(doc, chains, ch, "chain_board_far_left", c.l, c.t, c.w, c.h);
c = seat(1347, 148, 1364, 314);
addPngLayer(doc, chains, ch, "chain_board_step", c.l, c.t, c.w, c.h);
c = seat(1829, 148, 1846, 634);
addPngLayer(doc, chains, ch, "chain_board_far_right", c.l, c.t, c.w, c.h);

try {
    gf.move(doc.layers[0], ElementPlacement.PLACEBEFORE);
} catch (eTop) {
    log("re-top warn " + eTop);
}

var opt = new PhotoshopSaveOptions();
opt.layers = true;
opt.embedColorProfile = true;
opt.annotations = false;
opt.alphaChannels = true;

var crystalPath = "C:\\Users\\Emex33\\Desktop\\western_scene2.psd";
var rawCrystal = "C:\\Users\\Emex33\\Documents\\tombstone reborn\\web-sdk\\apps\\tombstone-reborn\\assets-raw\\scene\\western_scene2.psd";
var is1x = w < 2000;
var saved = "";

if (is1x) {
    doc.saveAs(OUT_1X, opt, false, Extension.LOWERCASE);
    saved = String(OUT_1X.fsName);
    log("saved-as-1x " + saved);
    try {
        doc.saveAs(OUT_1X_RAW, opt, true, Extension.LOWERCASE);
        log("copied-1x-raw " + String(OUT_1X_RAW.fsName));
    } catch (eRaw) {
        log("raw-1x-copy-fail " + eRaw);
    }
} else {
    var low = full.toLowerCase();
    if (low === crystalPath.toLowerCase() || low === rawCrystal.toLowerCase() || low.indexOf("western_scene2.psd") >= 0) {
        doc.save();
        saved = full;
        log("saved-crystal-in-place " + saved);
    } else {
        doc.save();
        saved = full;
        log("saved-active " + saved);
    }
}

var names = [];
function walk(container, depth) {
    var i, lyr, pad;
    pad = "";
    for (i = 0; i < depth; i++) pad += "  ";
    for (i = 0; i < container.layers.length; i++) {
        lyr = container.layers[i];
        names.push(pad + lyr.name);
        if (lyr.typename === "LayerSet") walk(lyr, depth + 1);
    }
}
walk(doc, 0);
log("layers-top-first:");
for (var n = 0; n < names.length && n < 40; n++) log("  " + names[n]);
log("DONE canvas=" + w + "x" + h + " path=" + (function () { try { return String(doc.fullName.fsName); } catch (e2) { return saved; } })());
"ok " + w + "x" + h + " " + (function () { try { return String(doc.fullName.fsName); } catch (e3) { return saved; } })();
