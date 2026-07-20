<script lang="ts">
	import { SvelteDate } from 'svelte/reactivity';

	import { Text, REM } from 'pixi-svelte';
	import { HUD_THEME } from '../hudTheme';

	type Props = {
		name: string;
	};

	const props: Props = $props();
	const reactiveDate = new SvelteDate();
	const clock = $derived(
		reactiveDate.toLocaleTimeString('en-US', {
			hour: 'numeric',
			minute: 'numeric',
			hour12: false,
		}),
	);
	const textProps = {
		style: {
			fontFamily: HUD_THEME.fontDisplay,
			fontSize: REM * 1.05,
			fontWeight: '700',
			lineHeight: REM * 1.4,
			fill: HUD_THEME.textPrimary,
			letterSpacing: 1,
		},
	} as const;

	let clockSizes = $state({ width: 0, height: 0 });

	$effect(() => {
		const interval = setInterval(() => {
			reactiveDate.setTime(Date.now());
		}, 1000);

		return () => {
			clearInterval(interval);
		};
	});
</script>

<Text text={clock} onresize={(value) => (clockSizes = value)} {...textProps} />
<Text text={props.name} x={clockSizes.width + 5} {...textProps} />
