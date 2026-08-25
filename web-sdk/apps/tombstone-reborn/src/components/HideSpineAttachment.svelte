<script lang="ts">
	import { getContextSpine } from 'pixi-svelte';

	const { slotName }: { slotName: string } = $props();
	const spine = getContextSpine();

	$effect(() => {
		const slot = spine.skeleton.findSlot(slotName);
		if (!slot) return;
		slot.setAttachment(null);
		slot.color.a = 0;
	});
</script>
