<script lang="ts">
	import { onMount } from 'svelte';
	import { getContextSpine } from 'pixi-svelte';

	const {
		slotName,
		slotNames,
		hidden = true,
	}: {
		slotName?: string;
		slotNames?: readonly string[];
		hidden?: boolean;
	} = $props();

	const spine = getContextSpine();
	const names = $derived(slotNames ?? (slotName ? [slotName] : []));
	const originals = new Map<string, string | null>();

	const apply = () => {
		for (const name of names) {
			const slot = spine.skeleton.findSlot(name);
			if (!slot) continue;
			if (!originals.has(name)) {
				originals.set(name, slot.data.attachmentName ?? name);
			}
			if (hidden) {
				// Setup-pose mix restores attachments every apply() unless the
				// slot data itself has no attachment to restore.
				slot.data.attachmentName = null;
				slot.setAttachment(null);
				slot.color.a = 0;
				continue;
			}
			const setup = originals.get(name);
			slot.data.attachmentName = setup;
			if (setup) spine.skeleton.setAttachment(slot.data.name, setup);
			slot.color.a = 1;
		}
	};

	$effect(() => {
		apply();
	});

	onMount(() => {
		const prev = spine.beforeUpdateWorldTransforms;
		spine.beforeUpdateWorldTransforms = () => {
			prev?.();
			apply();
		};
		return () => {
			spine.beforeUpdateWorldTransforms = prev;
		};
	});
</script>
