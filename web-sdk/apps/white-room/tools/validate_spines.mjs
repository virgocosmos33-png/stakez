// Validate the generated Madam Mirror symbol spines against the real Spine
// runtime classes (@esotericsoftware/spine-core 4.2.74) the frontend uses.
// Parses the shared atlas + every skeleton JSON exactly like assetLoad.ts does
// (SkeletonJson + AtlasAttachmentLoader + TextureAtlas, parser.scale = 2).
import { readFileSync, readdirSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const CORE = path.resolve(
	'../../..',
	'node_modules/.pnpm/@esotericsoftware+spine-core@4.2.74/node_modules/@esotericsoftware/spine-core/dist/index.js',
);
const spine = await import(pathToFileURL(CORE).href);
const { TextureAtlas, AtlasAttachmentLoader, SkeletonJson } = spine;

const DIR = path.resolve('../static/assets/spines/mm_symbols');
const atlasText = readFileSync(path.join(DIR, 'mm_symbols.atlas'), 'utf8');

// stub a texture on every page/region so attachment loading has dimensions
const atlas = new TextureAtlas(atlasText);
const fakeTexture = {
	setFilters() {},
	setWraps() {},
	dispose() {},
	getImage: () => ({ width: 1210, height: 1210 }),
};
atlas.pages.forEach((page) => {
	page.width = page.width || 1210;
	page.height = page.height || 1210;
	page.setTexture?.(fakeTexture);
	page.texture = page.texture || fakeTexture;
});
atlas.regions.forEach((r) => {
	r.texture = r.texture || fakeTexture;
	if (r.page) r.page.texture = r.page.texture || fakeTexture;
});

console.log(`atlas regions: ${atlas.regions.map((r) => r.name).join(', ')}`);

const files = readdirSync(DIR).filter((f) => f.endsWith('.json'));
let ok = 0;
let failed = 0;
for (const file of files) {
	try {
		const loader = new AtlasAttachmentLoader(atlas);
		const parser = new SkeletonJson(loader);
		parser.scale = 2;
		const data = parser.readSkeletonData(JSON.parse(readFileSync(path.join(DIR, file), 'utf8')));
		const anims = data.animations.map((a) => `${a.name}(${a.duration.toFixed(2)}s)`).join(', ');
		console.log(`OK  ${file.padEnd(9)} w=${data.width} h=${data.height} anims: ${anims}`);
		ok++;
	} catch (error) {
		console.error(`FAIL ${file}: ${error.message}`);
		failed++;
	}
}
console.log(`\n${ok} ok, ${failed} failed`);
process.exit(failed ? 1 : 0);
