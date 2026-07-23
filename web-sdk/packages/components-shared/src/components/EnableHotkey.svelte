<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	import { getContextEventEmitter } from 'utils-event-emitter';

	import type { EmitterEventHotKey } from '../types';

	const context = getContextEventEmitter<EmitterEventHotKey>();
	const PREVENT_DEFAULT_KEYS = ['Space', 'ArrowUp', 'ArrowDown'];
	const EXCLUDED_TAGS = ['input', 'textarea', 'select'];

	const getValidElement = (e: KeyboardEvent) =>
		!EXCLUDED_TAGS.includes(e?.target?.tagName?.toLowerCase());

	// every key currently held down - lets us synthesize releases when the
	// browser never delivers the real keyup (window blur, focus in an input)
	const heldKeys = new Set<string>();

	function handleKeydown(e: KeyboardEvent) {
		if (getValidElement(e)) {
			const isSpace = e.key === ' ';
			const key = isSpace ? 'Space' : e.key;
			if (PREVENT_DEFAULT_KEYS.includes(key)) e.preventDefault();
			// OS key-repeat must not re-fire presses (holding Space would
			// otherwise spam spin/skip on every repeat tick) - hold detection
			// only needs the FIRST keydown + the keyup. preventDefault above
			// still runs so a held Space never scrolls the page.
			if (e.repeat) return;
			if (key) {
				heldKeys.add(key);
				context.eventEmitter.broadcast({ type: 'hotKey', key, action: 'keyDown' });
			}
		}
	}

	function handleKeyup(e: KeyboardEvent) {
		// keyUp is NEVER filtered by target: releasing a held key over an input
		// must still end the hold, or space-hold betting gets stuck ON forever
		const isSpace = e.key === ' ';
		const key = isSpace ? 'Space' : e.key;
		if (getValidElement(e) && PREVENT_DEFAULT_KEYS.includes(key)) e.preventDefault();
		if (key) {
			heldKeys.delete(key);
			context.eventEmitter.broadcast({ type: 'hotKey', key, action: 'keyUp' });
		}
	}

	function releaseAllKeys() {
		// window lost focus: real keyups will never arrive - synthesize them so
		// no hold (space-hold betting, turbo latch) survives an alt-tab
		heldKeys.forEach((key) => {
			context.eventEmitter.broadcast({ type: 'hotKey', key, action: 'keyUp' });
		});
		heldKeys.clear();
	}

	onMount(() => {
		window.addEventListener('keydown', handleKeydown);
		window.addEventListener('keyup', handleKeyup);
		window.addEventListener('blur', releaseAllKeys);
		document.addEventListener('visibilitychange', releaseAllKeys);
	});

	onDestroy(() => {
		window.removeEventListener('keydown', handleKeydown);
		window.removeEventListener('keyup', handleKeyup);
		window.removeEventListener('blur', releaseAllKeys);
		document.removeEventListener('visibilitychange', releaseAllKeys);
	});
</script>
