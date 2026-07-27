<script lang="ts">
	import { OnPressFullScreen } from 'components-layout';

	import { getContext } from '../game/context';

	const context = getContext();

	// Full-screen tap → same bus as TapToSkip / HUD stop (`stopButtonClick`).
	// Space is owned by TapToSkip while the bet is busy — do not bind Space here
	// or one keypress fires the bus twice.
	const skip = () => {
		if (context.stateXstateDerived.isIdle()) return;
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};
</script>

<!-- No on-screen label — it kept covering the HUD. Tap/click continues via stop bus. -->
<OnPressFullScreen onpress={skip} />
