<script lang="ts">
	import { OnPressFullScreen } from 'components-layout';
	import { OnHotkey } from 'components-shared';

	type Props = {
		onpress: () => void;
	};

	const props: Props = $props();
</script>

<!-- No on-screen label — it kept covering the HUD. Tap/click or Space still continues. -->
<OnHotkey hotkey="Space" onpress={() => props.onpress()} />
<OnPressFullScreen onpress={() => props.onpress()} />
