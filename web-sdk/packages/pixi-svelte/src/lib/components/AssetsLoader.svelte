<script lang="ts">
	import type { Snippet } from 'svelte';
	import * as PIXI from 'pixi.js';

	import { getContextApp } from '../context.svelte';
	import { getProcessed } from '../assetLoad';
	import type { LoadedAssets, RawAsset } from '../types';

	type Props = { children: Snippet };

	const props: Props = $props();
	const context = getContextApp();

	let preLoaded = $state(false);
	let preloadStarted = $state(false);
	let postStarted = $state(false);
	let lazyStarted = $state(false);

	const VIDEO_LOAD_MS = 8_000;
	const ASSET_LOAD_MS = 20_000;

	const assetNameList = $derived(
		context.stateApp.assets
			? Object.keys(context.stateApp.assets).filter((key) => {
					const asset = context.stateApp.assets?.[key];
					return Boolean(asset?.preload) === false && asset?.lazy !== true;
				})
			: [],
	);

	const preAssetNameList = $derived(
		context.stateApp.assets
			? Object.keys(context.stateApp.assets).filter((key) => {
					const asset = context.stateApp.assets?.[key];
					return asset?.preload === true && asset?.lazy !== true;
				})
			: [],
	);

	const lazyAssetNameList = $derived(
		context.stateApp.assets
			? Object.keys(context.stateApp.assets).filter(
					(key) => context.stateApp.assets?.[key].lazy === true,
				)
			: [],
	);

	let counter = 0;

	const onProgress = (value: number) => {
		if (preLoaded && value === 1) {
			counter = counter + 1;
			const ratio = counter / assetNameList.length;
			context.stateApp.loadingProgress = ratio * 100;
		}
	};

	const srcIdOf = (key: string) => {
		const { type, src } = context.stateApp.assets![key];
		return type === 'spine'
			? Object.values(src)
					.filter((item) => typeof item === 'string')
					.join('|')
			: String(src);
	};

	const loadOne = async (key: string) => {
		const { type, src } = context.stateApp.assets![key];
		const loadSrc =
			type === 'spine' ? Object.values(src).filter((item) => typeof item === 'string') : src;
		const loadPromise = PIXI.Assets.load<RawAsset>(loadSrc, onProgress);
		const srcUrl = typeof src === 'string' ? src : '';
		const isVideo = /\.(webm|mp4|mov)(\?|#|$)/i.test(srcUrl);
		const timeoutMs = isVideo ? VIDEO_LOAD_MS : ASSET_LOAD_MS;
		return Promise.race([
			loadPromise,
			new Promise<never>((_, reject) => {
				setTimeout(() => {
					reject(new Error(`Asset "${key}" timed out after ${timeoutMs}ms`));
				}, timeoutMs);
			}),
		]);
	};

	const loadAssets = async (nameList: string[]) => {
		const srcToKeys = new Map<string, string[]>();
		for (const key of nameList) {
			const id = srcIdOf(key);
			const list = srcToKeys.get(id);
			if (list) list.push(key);
			else srcToKeys.set(id, [key]);
		}

		const loadedAssetsArray = await Promise.all(
			[...srcToKeys.values()].map(async (keys) => {
				const lead = keys[0];
				try {
					const rawAsset = await loadOne(lead);
					return keys.reduce((acc, key) => {
						const { type, src } = context.stateApp.assets![key];
						return { ...acc, ...getProcessed({ key, rawAsset, type, src }) };
					}, {} as LoadedAssets);
				} catch (error) {
					console.error(error);
				}
			}),
		);

		return loadedAssetsArray.reduce(
			(acc, cur) => ({
				...acc,
				...cur,
			}),
			{} as LoadedAssets,
		);
	};

	$effect(() => {
		if (preloadStarted) return;
		preloadStarted = true;
		(async () => {
			if (preAssetNameList.length > 0) {
				const preLoadedAssets = await loadAssets(preAssetNameList);
				if (preLoadedAssets) context.stateApp.loadedAssets = preLoadedAssets;
			}
			preLoaded = true;
		})();
	});

	$effect(() => {
		if (postStarted || !preLoaded || context.stateApp.loaded) return;
		postStarted = true;
		(async () => {
			if (assetNameList.length > 0) {
				const postLoadedAssets = await loadAssets(assetNameList);
				if (postLoadedAssets)
					context.stateApp.loadedAssets = {
						...context.stateApp.loadedAssets,
						...postLoadedAssets,
					};
			}
			context.stateApp.loaded = true;
		})();
	});

	$effect(() => {
		if (context.stateApp.loaded && !lazyStarted) {
			lazyStarted = true;
			if (lazyAssetNameList.length > 0) {
				loadAssets(lazyAssetNameList).then((lazyAssets) => {
					if (lazyAssets) {
						context.stateApp.loadedAssets = {
							...context.stateApp.loadedAssets,
							...lazyAssets,
						};
					}
				});
			}
		}
	});
</script>

{#if preLoaded}
	{@render props.children()}
{/if}
