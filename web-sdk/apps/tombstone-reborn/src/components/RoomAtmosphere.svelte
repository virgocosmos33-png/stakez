<script lang="ts">
	/**
	 * Super-bonus room weather. HTML embers only — smoke is the dual-decoder
	 * webm in Background (SeamlessVideoLoop), behind the board.
	 */
	import { getContext } from '../game/context';

	const context = getContext();
	const live = $derived(
		context.stateGame.atmosphere === 'super' && !context.stateLayout.showLoadingScreen,
	);

	type EmberKind = 'rise' | 'spiral' | 'tumble' | 'helix';

	type Ember = {
		id: number;
		kind: EmberKind;
		left: number;
		bottom: number;
		w: number;
		h: number;
		dur: number;
		delay: number;
		drift: number;
		amp: number;
		hot: boolean;
		ease: string;
	};

	const KINDS: EmberKind[] = ['rise', 'spiral', 'tumble', 'helix'];

	const embers: Ember[] = Array.from({ length: 64 }, (_, id) => {
		const kind = KINDS[id % 4];
		const roll = (id * 47 + 13) % 100;
		const big = roll > 88;
		const tiny = roll < 18;
		const base = tiny ? 1.2 + (id % 4) * 0.2 : big ? 3.6 + (id % 5) * 0.28 : 1.8 + (id % 8) * 0.22;
		const streak = kind === 'tumble' && id % 3 === 0;
		const along = (id * 19.3 + (id % 7) * 5.1) % 100;
		// Fat coals stay in the side thirds — never the middle of the board.
		const left = big ? (id % 2 === 0 ? 4 + (id % 11) : 85 + (id % 11)) : along;
		return {
			id,
			kind,
			left,
			bottom: ((id * 13) % 38) + (id % 5 === 0 ? 2 : 8),
			w: streak ? base * 0.45 : base,
			h: streak ? base * 1.7 : base,
			dur: kind === 'helix' ? 7 + (id % 6) * 1.1 : 3.2 + (id % 10) * 0.85 + (big ? 2 : 0),
			delay: -((id * 0.41) % 10),
			drift: ((id % 9) - 4) * (12 + (id % 5) * 6),
			amp: 18 + (id % 8) * 8,
			hot: big || id % 7 === 0,
			ease: id % 3 === 0 ? 'ease-out' : id % 3 === 1 ? 'linear' : 'ease-in-out',
		};
	});
</script>

<div class="room-atmo" class:on={live} aria-hidden="true">
	<div class="embers">
		{#each embers as e (e.id)}
			<span
				class="ember {e.kind}"
				class:hot={e.hot}
				style="
					left: {e.left}%;
					bottom: {e.bottom}%;
					width: {e.w}px;
					height: {e.h}px;
					animation-duration: {e.dur}s;
					animation-delay: {e.delay}s;
					animation-timing-function: {e.ease};
					--drift: {e.drift}px;
					--amp: {e.amp}px;
				"
			></span>
		{/each}
	</div>
</div>

<style>
	.room-atmo {
		position: fixed;
		inset: 0;
		z-index: 4;
		pointer-events: none;
		overflow: hidden;
		opacity: 0;
		transition: opacity 0.9s ease;
	}

	.room-atmo.on {
		opacity: 1;
	}

	.embers {
		position: absolute;
		inset: 0;
		mix-blend-mode: plus-lighter;
	}

	.ember {
		position: absolute;
		border-radius: 50%;
		background: radial-gradient(
			circle at 38% 32%,
			#fff8d2 0%,
			#ffb347 26%,
			#ff4e10 56%,
			#7a1000 80%,
			transparent 100%
		);
		box-shadow:
			0 0 3px 1px rgba(255, 140, 40, 0.7),
			0 0 6px 2px rgba(255, 50, 0, 0.22);
		animation-iteration-count: infinite;
		will-change: transform, opacity;
	}

	.ember.hot {
		box-shadow:
			0 0 4px 1px rgba(255, 200, 80, 0.8),
			0 0 8px 2px rgba(255, 70, 10, 0.28);
	}

	.ember.rise {
		animation-name: ember-rise;
	}

	.ember.spiral {
		animation-name: ember-spiral;
	}

	.ember.tumble {
		animation-name: ember-tumble;
		border-radius: 40%;
	}

	.ember.helix {
		animation-name: ember-helix;
	}

	@keyframes ember-rise {
		0% {
			transform: translate3d(0, 6px, 0) scale(0.5);
			opacity: 0;
		}
		10% {
			opacity: 1;
		}
		100% {
			transform: translate3d(var(--drift), -68vh, 0) scale(0.2);
			opacity: 0;
		}
	}

	@keyframes ember-spiral {
		0% {
			transform: translate3d(0, 4px, 0) rotate(0deg) scale(0.45);
			opacity: 0;
		}
		8% {
			opacity: 1;
		}
		25% {
			transform: translate3d(var(--amp), -17vh, 0) rotate(90deg) scale(0.72);
		}
		50% {
			transform: translate3d(calc(var(--amp) * -1), -34vh, 0) rotate(180deg) scale(0.7);
		}
		75% {
			transform: translate3d(var(--amp), -51vh, 0) rotate(270deg) scale(0.4);
		}
		100% {
			transform: translate3d(0, -68vh, 0) rotate(360deg) scale(0.15);
			opacity: 0;
		}
	}

	@keyframes ember-tumble {
		0% {
			transform: translate3d(0, 8px, 0) rotate(0deg) scale(0.6);
			opacity: 0;
		}
		12% {
			opacity: 1;
		}
		100% {
			transform: translate3d(var(--drift), -70vh, 0) rotate(540deg) scale(0.18);
			opacity: 0;
		}
	}

	@keyframes ember-helix {
		0% {
			transform: translate3d(0, 0, 0) rotate(0deg) scale(0.4);
			opacity: 0;
		}
		10% {
			opacity: 1;
		}
		20% {
			transform: translate3d(var(--amp), -12vh, 0) rotate(40deg) scale(1);
		}
		40% {
			transform: translate3d(calc(var(--amp) * -0.85), -26vh, 0) rotate(-30deg) scale(0.85);
		}
		60% {
			transform: translate3d(calc(var(--amp) * 0.7), -40vh, 0) rotate(55deg) scale(0.55);
		}
		80% {
			transform: translate3d(calc(var(--amp) * -0.4), -54vh, 0) rotate(-20deg) scale(0.35);
		}
		100% {
			transform: translate3d(0, -68vh, 0) rotate(10deg) scale(0.12);
			opacity: 0;
		}
	}
</style>
