<script lang="ts">
	/**
	 * Hanging lantern as a vertex grid. A shot kills the globe and the
	 * mesh keeps punching in Z.
	 */
	import { Mesh, MeshGeometry, Texture } from 'pixi.js';
	import { getContextApp, getContextParent } from 'pixi-svelte';
	import type { LoadedSprite } from 'pixi-svelte';

	import { SALOON_LAMPS } from '../game/saloonLamps';
	import { applyLampPunch, buildLampMeshGrid } from '../game/saloonLampPunch';

	type Props = {
		punch: number;
		lit: boolean;
		tint: number;
	};

	const props: Props = $props();
	const L = SALOON_LAMPS.L;
	const app = getContextApp();
	const parent = getContextParent();
	const grid = buildLampMeshGrid(L.width, L.height);
	const geometry = new MeshGeometry({
		positions: new Float32Array(grid.rest),
		uvs: grid.uvs,
		indices: grid.indices,
	});
	const mesh = new Mesh({
		texture: Texture.EMPTY,
		geometry,
	});
	mesh.x = -L.anchorX * L.width;
	mesh.y = -L.anchorY * L.height;
	mesh.eventMode = 'none';
	parent.addToParent(mesh);

	$effect(() => {
		const lit = (app.stateApp.loadedAssets?.['saloonLampL'] || Texture.EMPTY) as LoadedSprite;
		const dead = (app.stateApp.loadedAssets?.['saloonLampLSmashed'] ||
			Texture.EMPTY) as LoadedSprite;
		const next = props.lit ? lit : dead;
		if (mesh.texture !== next) mesh.texture = next;
		mesh.tint = props.lit ? props.tint : 0xffffff;
		applyLampPunch(mesh, grid.rest, props.punch, L.width, L.height);
	});
</script>
