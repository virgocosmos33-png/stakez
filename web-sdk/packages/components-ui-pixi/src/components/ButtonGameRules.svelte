<script lang="ts">
	import type { ButtonProps } from 'components-pixi';
	import { stateModal } from 'state-shared';

	import UiButton from './UiButton.svelte';
	import { getContext } from '../context';
	import { UI_BASE_SIZE } from '../constants';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const context = getContext();
	const sizes = { width: UI_BASE_SIZE, height: UI_BASE_SIZE };

	const onpress = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		// the full-page pay table menu carries the complete game rules;
		// the bare gameRules modal is an unfinished placeholder
		stateModal.modal = { name: 'payTable' };
	};
</script>

<UiButton {...props} {sizes} {onpress} icon="info" variant="light" />
