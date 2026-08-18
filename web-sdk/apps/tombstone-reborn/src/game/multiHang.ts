/**
 * MULTI box hang. Seated in base at x1. Shared so the three HudReadout
 * layers (chains / plate / boxes) stay in lockstep.
 */
import { Tween } from 'svelte/motion';

/** 0 = parked at the hinge (hidden), 1 = seated. */
export const multiHang = new Tween(0, { duration: 0 });

let live = false;

export const syncMultiHang = (next: boolean) => {
	if (next === live) return;
	live = next;
	multiHang.set(next ? 1 : 0, { duration: 0 });
};

export const multiHangPose = (t: number) => {
	const u = Math.min(1, Math.max(0, t));
	return {
		swing: Math.sin(u * Math.PI * 5.2 + 0.55) * (1 - u) * 0.36,
		sway: Math.sin(u * Math.PI * 3.4 + 0.2) * (1 - u) * 12,
	};
};
