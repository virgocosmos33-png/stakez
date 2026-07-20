<script lang="ts">
	type Props = {
		width: string;
		height: string;
		/** kept for API compat; a non-default value still wins over the theme skin */
		background?: string;
		/** kept for API compat; when passed it overrides the themed border */
		border?: string;
		/** highlight this skin as the active/selected choice (gold glow) */
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
	// Drama Studios house style (mirrors the Pixi hudTheme): dark glass body with
	// a metallic-gold bevel. This skin sits behind BaseButtonContent in every
	// modal button, so theming it here themes the whole HTML UI at once.
	.skin {
		position: relative;
		width: var(--w);
		height: var(--h);
		border-radius: 12px;
		background: var(--bg, linear-gradient(180deg, #3a3a48 0%, #1b1b22 48%, #08080c 100%));
		border: var(--border, 1px solid rgba(201, 154, 63, 0.85));
		box-shadow:
			inset 0 1px 0 rgba(246, 228, 166, 0.35),
			inset 0 -7px 14px rgba(0, 0, 0, 0.55),
			0 2px 6px rgba(0, 0, 0, 0.6);
	}

	// top sheen for the "glass" read
	.skin::after {
		content: '';
		position: absolute;
		inset: 1px 1px 55% 1px;
		border-radius: 11px 11px 40% 40%;
		background: linear-gradient(180deg, rgba(255, 255, 255, 0.14), rgba(255, 255, 255, 0));
		pointer-events: none;
	}

	.skin.selected {
		border-color: #ffc12e;
		background: linear-gradient(180deg, #4c4432 0%, #2b2414 60%, #171205 100%);
		box-shadow:
			inset 0 1px 0 rgba(246, 228, 166, 0.5),
			0 0 0 1px rgba(255, 193, 46, 0.55),
			0 0 14px rgba(255, 193, 46, 0.5);
	}
</style>
