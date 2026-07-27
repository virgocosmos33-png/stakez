<script lang="ts" module>
	export type EmitterEventWildReel =
		| { type: 'wildReelSlideShow'; reels: number[] }
		| { type: 'wildReelSlideHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, MAX_ROWS, NUM_ROWS, pickWildReelArt, type WildReelArt } from '../game/constants';

	const context = getContext();

	// each triggered reel remembers WHICH random premium wild portrait it drew, so
	// the art stays fixed for the whole slide (no per-frame flicker). Wild reels
	// now fire ONE PER CELL (activation order), so each entry keeps its OWN slide
	// tween — a later wild reel slides in while the earlier columns stay at rest.
	let reels = $state<{ reel: number; art: WildReelArt; slide: Tween<number> }[]>([]);

	// One column overlay per triggered middle reel. The art spans EXACTLY that
	// reel's visible rows (diamond board: reels are centred on the board mid-line),
	// so it covers the reel that went wild — not a phantom extra row.
	const columns = $derived.by(() => {
		if (!reels.length)
			return [] as {
				reel: number;
				art: WildReelArt;
				cx: number;
				cy: number;
				w: number;
				h: number;
				artW: number;
				artH: number;
			}[];
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		const w = SYMBOL_SIZE;
		// every reel is vertically centred on the board mid-line
		const cy = originY + MAX_ROWS * 0.5 * SYMBOL_SIZE;
		return reels.map(({ reel, art, slide }) => {
			const rows = NUM_ROWS[reel] ?? MAX_ROWS;
			const h = rows * SYMBOL_SIZE;
			// cover-fit the portrait art into the reel column (crop overflow, never letterbox)
			const scale = Math.max(w / art.width, h / art.height);
			return {
				reel,
				art,
				slide,
				cx: originX + (reel + 0.5) * SYMBOL_SIZE,
				cy,
				w,
				h,
				artW: art.width * scale,
				artH: art.height * scale,
			};
		});
	});

	context.eventEmitter.subscribeOnMount({
		// a bottom-slot WILD turned this middle reel into a Wild Reel: the wild
		// column drops in from the top of the reel window with a weighty nudge.
		// ACCUMULATES: earlier wild columns stay at rest while the new one slides.
		wildReelSlideShow: async (e) => {
			const existing = new Set(reels.map((r) => r.reel));
			const added = e.reels
				.filter((reel) => !existing.has(reel))
				.map((reel) => ({ reel, art: pickWildReelArt(), slide: new Tween(0) }));
			if (!added.length) return;
			reels = [...reels, ...added];
			await Promise.all(
				added.map((r) => r.slide.set(1, { duration: 560, easing: backOut })),
			);
		},
		wildReelSlideHide: () => {
			reels = [];
		},
	});
</script>

{#if reels.length}
	<MainContainer>
		{#each columns as c (c.reel)}
			<!-- masked to the reel window: the wild column slides DOWN into the reel
				(clipped like a reel drop), landing on top of the board symbols. -->
			<Container x={c.cx} y={c.cy}>
				<Rectangle isMask anchor={0.5} width={c.w} height={c.h} backgroundColor={0xffffff} />
				<Sprite
					key={c.art.key}
					x={0}
					y={-c.h * (1 - c.slide.current)}
					anchor={0.5}
					width={c.artW}
					height={c.artH}
				/>
			</Container>
		{/each}
	</MainContainer>
{/if}
