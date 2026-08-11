<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	// Stake Engine mandatory book: COMPONENTS/Symbol exercises the symbol renderer
	// in isolation — one symbol with controls, and the whole cast in a gallery.
	// See https://stakeengine.github.io/math-sdk/fe_docs/explore_sb/
	const { Story } = defineMeta({
		title: 'COMPONENTS/Symbol',
		argTypes: {
			symbol: {
				control: 'select',
				options: ['H1', 'H2', 'H3', 'H4', 'H5', 'L1', 'L2', 'L3', 'L4', 'L5', 'W', 'S'],
			},
			state: {
				control: 'select',
				options: ['static', 'win', 'land', 'postWin', 'postWinStatic'],
			},
		},
	});
</script>

<script lang="ts">
	import { App, Container, Text } from 'pixi-svelte';
	import { CanvasSizeRectangle, MainContainer } from 'components-layout';
	import { StoryLocale } from 'components-storybook';

	import SymbolSprite from '../components/SymbolSprite.svelte';
	import { getContext, setContext } from '../game/context';
	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_SIZE } from '../game/constants';
	import type { SymbolName, SymbolState } from '../game/types';

	setContext();
	const context = getContext();

	// every symbol the player sees on the reels (specials never land there)
	const NAMES: SymbolName[] = ['H1', 'H2', 'H3', 'H4', 'H5', 'L1', 'L2', 'L3', 'L4', 'L5', 'W', 'S'];
	const COLS = 4;
	const CELL = SYMBOL_SIZE * 1.25;
	const LABEL_STYLE = {
		fill: 0xf5e6c8,
		fontFamily: 'Arial',
		fontSize: 22,
		fontWeight: 'bold' as const,
		align: 'center' as const,
		stroke: { color: 0x1a1109, width: 4 },
	};
</script>

<!-- COMPONENTS/Symbol/component: one symbol, pick face + state from Controls. -->
{#snippet componentTemplate(args: { symbol?: SymbolName; state?: SymbolState })}
	{@const name = (args.symbol ?? 'H1') as SymbolName}
	{@const state = (args.state ?? 'static') as SymbolState}
	<StoryLocale lang="en">
		<App>
			{#if context.stateApp.loaded}
				<CanvasSizeRectangle backgroundColor={0x140d08} backgroundAlpha={1} />
				<MainContainer>
					{@const main = context.stateLayoutDerived.mainLayout()}
					<Container x={main.width / 2} y={main.height / 2}>
						<SymbolSprite {state} symbolInfo={getSymbolInfo({ rawSymbol: { name }, state })} />
						<Text
							anchor={0.5}
							y={SYMBOL_SIZE * 0.72}
							text={`${name} · ${state}`}
							style={LABEL_STYLE}
						/>
					</Container>
				</MainContainer>
			{/if}
		</App>
	</StoryLocale>
{/snippet}

<!-- COMPONENTS/Symbol/gallery: every symbol the player sees, in a grid. -->
{#snippet galleryTemplate()}
	{@const rows = Math.ceil(NAMES.length / COLS)}
	<StoryLocale lang="en">
		<App>
			{#if context.stateApp.loaded}
				<CanvasSizeRectangle backgroundColor={0x140d08} backgroundAlpha={1} />
				<MainContainer>
					{@const main = context.stateLayoutDerived.mainLayout()}
					<Container x={main.width / 2} y={main.height / 2}>
						{#each NAMES as name, i (name)}
							{@const col = i % COLS}
							{@const row = Math.floor(i / COLS)}
							<Container
								x={(col - (COLS - 1) / 2) * CELL}
								y={(row - (rows - 1) / 2) * CELL}
							>
								<SymbolSprite symbolInfo={getSymbolInfo({ rawSymbol: { name }, state: 'static' })} />
								<Text anchor={0.5} y={SYMBOL_SIZE * 0.58} text={name} style={LABEL_STYLE} />
							</Container>
						{/each}
					</Container>
				</MainContainer>
			{/if}
		</App>
	</StoryLocale>
{/snippet}

<Story name="component" args={{ symbol: 'H1', state: 'static' }} template={componentTemplate} />
<Story name="gallery" template={galleryTemplate} />
