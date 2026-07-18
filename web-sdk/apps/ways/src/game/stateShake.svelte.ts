// Shared board-shake offset. Components that render board-anchored content
// (board container, reels frame, apparition/shatter/liner overlays) add
// stateShake.x/y to their container position so the whole rig kicks as one
// camera move while the room background stays still.
export const stateShake = $state({ x: 0, y: 0 });

let shakeToken = 0;

export const shakeBoard = ({
	intensity = 10,
	duration = 380,
}: { intensity?: number; duration?: number } = {}) => {
	const token = ++shakeToken;
	const start = performance.now();

	const tick = (now: number) => {
		// a newer shake owns the offset now
		if (token !== shakeToken) return;
		const progress = (now - start) / duration;
		if (progress >= 1) {
			stateShake.x = 0;
			stateShake.y = 0;
			return;
		}
		// fresh random direction every frame = jitter, decaying to rest
		const decay = Math.pow(1 - progress, 1.6);
		const angle = Math.random() * Math.PI * 2;
		stateShake.x = Math.cos(angle) * intensity * decay;
		stateShake.y = Math.sin(angle) * intensity * decay * 0.8;
		requestAnimationFrame(tick);
	};

	requestAnimationFrame(tick);
};
