<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Rectangle, Text } from 'pixi-svelte';
	import { stateUrlDerived } from 'state-shared';
	import { socialText } from 'utils-shared/socialText';
	import { SPECIALS, INFO_SECTIONS } from 'components-ui-html';

	// Base-game info ticker for the centre HUD well (the slot the FREE SPINS
	// counter occupies during the bonus). Scrolls the SAME scatter / wild /
	// buy-bonus / ways / feature copy shown in the pay-table menu, seamlessly
	// looped and clipped to the well by a Pixi mask so it never spills into the
	// WAYS / WIN compartments beside it. Only mounted in the base game.
	//
	// The full message is far too long to live in a single PIXI.Text (its texture
	// would exceed the GPU max width and render blank), so it is packed into
	// word-bounded chunks, each a separate Text laid end-to-end, then the whole
	// run is duplicated for the seam-free wrap.
	type Props = {
		/** centre of the well (world/design space, matches FrameMorphHud slots) */
		x: number;
		y: number;
		/** clip window = the well's inner width/height */
		width: number;
		height: number;
		fontSize: number;
	};
	const { x, y, width, height, fontSize }: Props = $props();

	// stake.us jurisdiction language: rewrite prohibited gambling terms, exactly
	// like the pay-table modal does
	const st = (text: string) => socialText(text, stateUrlDerived.social());

	// Compose ticker items straight from the shared info source of truth.
	// Specials first (WILD / SCATTER / HAUNTED MIRROR / MADAM'S EYE), then the
	// most player-relevant rule sections (ways, free spins, feature spins, buys).
	const SECTION_TITLES = [
		'WAYS PAYS',
		'FREE SPINS',
		'EXTRA BET & FEATURE SPINS',
		'BONUS BUYS',
		'MAX WIN',
	];

	const sectionToText = (title: string) => {
		const section = INFO_SECTIONS.find((s) => s.title === title);
		if (!section) return '';
		const parts: string[] = [];
		if (section.body) parts.push(section.body);
		if (section.rows?.length)
			parts.push(section.rows.map((r) => `${r.label} — ${r.value}`).join('   '));
		if (section.bullets?.length) parts.push(section.bullets.join('   '));
		return `${section.title}: ${parts.join('   ')}`;
	};

	// diamond flourish between items — padded with non-breaking spaces so the gap
	// survives the word-splitting below (which splits on plain spaces only)
	const SEP = '\u00a0\u00a0\u00a0\u25c6\u00a0\u00a0\u00a0';
	const message = $derived(
		[
			...SPECIALS.map((s) => `${s.name.toUpperCase()} — ${s.desc}`),
			...SECTION_TITLES.map(sectionToText).filter(Boolean),
		]
			.map(st)
			.join(SEP) + SEP,
	);

	const textStyle = $derived({
		fontFamily: '"Segoe UI", Arial, Helvetica, sans-serif',
		fontWeight: '700',
		fontSize,
		fill: 0xf0e6d0,
		letterSpacing: 0.3,
		stroke: { color: 0x2a1608, width: 2 },
	} as const);

	// keep every chunk's texture comfortably under the GPU limit
	const maxChars = $derived(Math.max(24, Math.floor(1400 / (fontSize * 0.62))));
	const chunks = $derived.by(() => {
		const words = message.split(' ');
		const out: string[] = [];
		let cur = '';
		for (const w of words) {
			const next = cur ? `${cur} ${w}` : w;
			if (next.length > maxChars && cur) {
				out.push(cur);
				cur = w;
			} else {
				cur = next;
			}
		}
		if (cur) out.push(cur);
		return out;
	});

	// measured chunk widths → cumulative x positions and the total run width
	let widths = $state<number[]>([]);
	const setWidth = (i: number, w: number) => {
		if (widths[i] === w) return;
		const next = widths.slice();
		next[i] = w;
		widths = next;
	};
	const layout = $derived.by(() => {
		const pos: number[] = [];
		let acc = 0;
		for (let i = 0; i < chunks.length; i++) {
			pos.push(acc);
			acc += widths[i] ?? 0;
		}
		return { pos, total: acc };
	});

	// scroll offset, animated leftward and wrapped at the run width so the second
	// copy lands exactly where the first began (invisible seam)
	let offset = $state(0);
	const SPEED = 46; // px / second

	onMount(() => {
		let raf = 0;
		let last = performance.now();
		const tick = (now: number) => {
			const dt = (now - last) / 1000;
			last = now;
			const total = layout.total;
			if (total > 0) {
				offset -= SPEED * dt;
				if (offset <= -total) offset += total;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	// text starts at the LEFT edge of the well and scrolls left
	const trackX = $derived(-width / 2 + offset);
</script>

<Container {x} {y}>
	<!-- clip window: exactly the well's inner box, so the scroll never bleeds
		into the WAYS / WIN compartments -->
	<Rectangle isMask anchor={0.5} {width} {height} backgroundColor={0xffffff} />

	<!-- moving track: chunked message laid end-to-end, then duplicated so the
		loop is seamless -->
	<Container x={trackX} y={0}>
		{#each chunks as chunk, i (i)}
			<Text
				anchor={{ x: 0, y: 0.5 }}
				x={layout.pos[i]}
				text={chunk}
				style={textStyle}
				onresize={(sizes) => setWidth(i, sizes.width)}
			/>
		{/each}
		{#if layout.total > 0}
			{#each chunks as chunk, i (i)}
				<Text
					anchor={{ x: 0, y: 0.5 }}
					x={layout.total + layout.pos[i]}
					text={chunk}
					style={textStyle}
				/>
			{/each}
		{/if}
	</Container>
</Container>
