<script lang="ts">
	type Props = {
		width: string;
		height: string;
		/** kept for API compat; a non-default value still wins over the theme skin */
		background?: string;
		/** kept for API compat; when passed it overrides the themed border */
		border?: string;
		/** highlight this skin as the active/selected choice (inverted white) */
		selected?: boolean;
	};

	const { width, height, background = 'black', border, selected = false }: Props = $props();
	const customBg = $derived(background && background !== 'black' ? background : '');
</script>

<div
	class="skin"
	class:selected
	style="
	--w: {width};
	--h: {height};
	{customBg ? `--bg: ${customBg};` : ''}
	{border ? `--border: ${border};` : ''}
"
></div>

<style lang="scss">
	// Drama Studios MONO house style (mirrors the pixi ControlInfoBar stepper):
	// a flat dark gunmetal face inside a single hairline border — no gold, no
	// glass sheen, no glow. This skin sits behind BaseButtonContent in every
	// modal button, so theming it here themes the whole HTML UI at once.
	.skin {
		position: relative;
		width: var(--w);
		height: var(--h);
		border-radius: var(--mono-radius, 10px);
		background: var(--bg, var(--mono-surface-2, #1c2732));
		border: var(--border, 1px solid var(--mono-edge, #33414f));
		box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
		transition:
			background 0.15s ease,
			border-color 0.15s ease;
	}

	// selected / active → inverted white fill (primary emphasis). Labels layered
	// on top must switch to --mono-on-fill so they stay legible on white.
	.skin.selected {
		background: var(--mono-fill, #ffffff);
		border-color: var(--mono-fill, #ffffff);
		box-shadow: none;
	}
</style>
