import { WESTERN_SCENE_SEATS } from './westernSceneSeats.generated';

/** Duck-type the ready TR2 western skeleton. Never use instanceof —
 *  app vs pixi-svelte can load two copies of spine-pixi-v8. */
export const isWesternSceneSkeleton = (data: unknown) => {
	const skeleton = data as { bones?: unknown; animations?: unknown } | undefined;
	return Array.isArray(skeleton?.bones) && Array.isArray(skeleton?.animations);
};

/**
 * Scene wood that HudReadout / BoardPlate already paint. Chains stay on the
 * ready skeleton — those slots are not in this list.
 */
export const WESTERN_PLAQUE_SLOTS = [
	'MAIN_FRAME',
	'Layer_4',
	'Layer_5',
	'Layer_4_copy',
	'Layer_6',
	'Layer_4_copy_2',
	'Layer_7',
	'Layer_4_copy_2_02',
	'Layer_9',
] as const;

/** Street hanging lamps. HangingLamps paints those. Sitting barrel lantern
 *  stays on this skeleton so the porch lamp is lit in base, not bonus-only. */
export const WESTERN_LAMP_SLOTS = [
	'left_hanging_lamp',
	'right_hanging_lamp',
	'left_hanging_lamp_light',
	'right_hanging_lamp_light',
] as const;

/** FREE SPINS hangers. Hidden in base so empty chains do not hang with no plaque. */
export const WESTERN_FREE_SPINS_CHAIN_SLOTS = [
	'Layer_8_copy_7_02',
	'Layer_8_copy_8_02',
	'Layer_8_copy_12',
	'chain_bolt_copy_20',
	'chain_bolt_copy_21',
	'chain_bolt_copy_24',
	'chain_bolt_copy_25',
] as const;

/** Beware / Dead Men / Tell No Tales — gone in the ready git scene. */
export const WESTERN_SIGN_SLOTS = [
	'signpost',
	'sign_beware_1',
	'sign_beware_2',
	'sign_dead_men',
	'sign_tell_no_tales',
	'sign_highlight',
] as const;

/** Old flatten plate only. red_filter stays on the skeleton — scene-viewer
 *  sets that slot's alpha (Base 45% / Bonus 80%). Do not hide it. */
export const WESTERN_STREET_SLOTS = ['background'] as const;

/**
 * PSD "clouds marquee" on bone `bg`. Idle is rotate-only, so CloudsMarquee
 * slides the existing slots. homeX comes from the live western_scene skin.
 */
export const WESTERN_CLOUD_MARQUEE = {
	slots: ['background_clouds', 'background_clouds_2'] as const,
	homeX: WESTERN_SCENE_SEATS.cloudHomeX,
	artW: 4189,
	/** 1× px / second, right → left */
	speed: 42,
} as const;

/**
 * FX panel from the ready Spine scene lamp_state.json — not a local guess.
 * smoke true, fire true, density 48, speed 1.
 * backgroundSPINE/spine-scene/lamp_state.json
 * assets/spines/western_scene/lamp_state.json
 */
export const WESTERN_SCENE_FX = {
	viewW: 1342,
	viewH: 892,
	smoke: true,
	fire: true,
	density: 48,
	speed: 1,
} as const;

/** red_filter.json — PNG is full strength. Spine slot blend is multiply. */
export const WESTERN_RED_FILTER = {
	blend: 'multiply',
	baseOpacity: 0.45,
	bonusOpacity: 0.8,
} as const;

/** Viewer barrel lamp Glow slider 0.40x. On in bonus only. */
export const WESTERN_BARREL_LUMEN = 0.4;

/** lantern_dim_light seat in SCENE_ART. From the live western_scene skeleton. */
export const WESTERN_BARREL_GLOW = WESTERN_SCENE_SEATS.barrelGlow;

/** `idle` rotate keys from TR2-Spine-Background-scene/spine-scene/skeleton.json. */
type IdleRotateKey = {
	time: number;
	value: number;
	curve?: number;
	c2?: number;
	c3?: number;
	c4?: number;
};

const IDLE_LAMP_ROTATE: Record<'L' | 'R', readonly IdleRotateKey[]> = {
	L: [
		{ time: 0, value: -8, curve: 0.42, c2: 0, c3: 1, c4: 1 },
		{ time: 1.3147, value: 0, curve: 0, c2: 0, c3: 0.58, c4: 1 },
		{ time: 2.6294, value: 8, curve: 0.42, c2: 0, c3: 1, c4: 1 },
		{ time: 3.9441, value: 0, curve: 0, c2: 0, c3: 0.58, c4: 1 },
		{ time: 5.2588, value: -8 },
	],
	R: [
		{ time: 0, value: 6.5, curve: 0.42, c2: 0, c3: 1, c4: 1 },
		{ time: 1.3017, value: 0, curve: 0, c2: 0, c3: 0.58, c4: 1 },
		{ time: 2.6033, value: -6.5, curve: 0.42, c2: 0, c3: 1, c4: 1 },
		{ time: 3.905, value: 0, curve: 0, c2: 0, c3: 0.58, c4: 1 },
		{ time: 5.2067, value: 6.5 },
	],
};

export const WESTERN_IDLE_DURATION = 5.2588;

type IdleColorKey = {
	time: number;
	color: string;
	curve?: number;
	c2?: number;
	c3?: number;
	c4?: number;
};

/** `idle` slot color on left/right_hanging_lamp_light. */
const IDLE_LAMP_LIGHT: Record<'L' | 'R', readonly IdleColorKey[]> = {
	L: [
		{ time: 0, color: 'ffffffb8', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 0.3068, color: 'fffffff2', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 0.6793, color: 'ffffff99', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 1.1504, color: 'ffffffe0', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 1.5338, color: 'ffffffff', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 1.9501, color: 'ffffffa3', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 2.4651, color: 'ffffffe6', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 2.9362, color: 'ffffff8c', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 3.3963, color: 'ffffffdb', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 3.8893, color: 'fffffffa', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 4.3823, color: 'ffffffb2', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 4.8425, color: 'ffffffcc', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 5.2588, color: 'ffffffb8' },
	],
	R: [
		{ time: 0, color: 'ffffffd9', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 0.4163, color: 'ffffffff', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 0.7888, color: 'ffffff94', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 1.2051, color: 'fffffff0', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 1.6215, color: 'ffffffb2', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 2.1364, color: 'ffffffff', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 2.4979, color: 'ffffff8c', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 2.9581, color: 'ffffffeb', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 3.4511, color: 'ffffffad', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 3.966, color: 'fffffffa', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 4.4919, color: 'ffffff9e', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 4.9082, color: 'ffffffe6', curve: 0.33, c2: 0, c3: 0.67, c4: 1 },
		{ time: 5.2588, color: 'ffffffd9' },
	],
};

const parseSpineColor = (hex: string) => {
	const h = hex.replace('#', '');
	if (h.length === 8) {
		return {
			r: parseInt(h.slice(0, 2), 16) / 255,
			g: parseInt(h.slice(2, 4), 16) / 255,
			b: parseInt(h.slice(4, 6), 16) / 255,
			a: parseInt(h.slice(6, 8), 16) / 255,
		};
	}
	return {
		r: parseInt(h.slice(0, 2), 16) / 255,
		g: parseInt(h.slice(2, 4), 16) / 255,
		b: parseInt(h.slice(4, 6), 16) / 255,
		a: 1,
	};
};

const mixColor = (
	a: ReturnType<typeof parseSpineColor>,
	b: ReturnType<typeof parseSpineColor>,
	p: number,
) => ({
	r: a.r + (b.r - a.r) * p,
	g: a.g + (b.g - a.g) * p,
	b: a.b + (b.b - a.b) * p,
	a: a.a + (b.a - a.a) * p,
});

const bezierY = (x: number, cx1: number, cy1: number, cx2: number, cy2: number) => {
	let t = x;
	for (let i = 0; i < 8; i += 1) {
		const u = 1 - t;
		const xt = 3 * u * u * t * cx1 + 3 * u * t * t * cx2 + t * t * t;
		const dx = xt - x;
		if (Math.abs(dx) < 1e-5) break;
		const d = 3 * u * u * cx1 + 6 * u * t * (cx2 - cx1) + 3 * t * t * (1 - cx2);
		if (Math.abs(d) < 1e-6) break;
		t = Math.max(0, Math.min(1, t - dx / d));
	}
	const u = 1 - t;
	return 3 * u * u * t * cy1 + 3 * u * t * t * cy2 + t * t * t;
};

/** Radians. Same pendulum as the ready scene `idle` clip. */
export const westernIdleLampRotation = (side: 'L' | 'R', seconds: number) => {
	const keys = IDLE_LAMP_ROTATE[side];
	const period = keys[keys.length - 1]?.time || WESTERN_IDLE_DURATION;
	const t = ((seconds % period) + period) % period;
	if (t <= keys[0].time) return (keys[0].value * Math.PI) / 180;
	const last = keys[keys.length - 1];
	if (t >= last.time) return (last.value * Math.PI) / 180;
	let i = 1;
	while (i < keys.length && keys[i].time < t) i += 1;
	const a = keys[i - 1];
	const b = keys[i];
	const span = b.time - a.time;
	if (span <= 0) return (b.value * Math.PI) / 180;
	let p = (t - a.time) / span;
	if (typeof a.curve === 'number') p = bezierY(p, a.curve, a.c2 ?? 0, a.c3 ?? 1, a.c4 ?? 1);
	return (((a.value + (b.value - a.value) * p) * Math.PI) / 180);
};

/** Additive oil flicker from the ready scene `idle` light slots. */
export const westernIdleLampLight = (side: 'L' | 'R', seconds: number) => {
	const keys = IDLE_LAMP_LIGHT[side];
	const period = keys[keys.length - 1]?.time || WESTERN_IDLE_DURATION;
	const t = ((seconds % period) + period) % period;
	const at = (key: IdleColorKey) => parseSpineColor(key.color);
	if (t <= keys[0].time) return at(keys[0]);
	const last = keys[keys.length - 1];
	if (t >= last.time) return at(last);
	let i = 1;
	while (i < keys.length && keys[i].time < t) i += 1;
	const a = keys[i - 1];
	const b = keys[i];
	const span = b.time - a.time;
	if (span <= 0) return at(b);
	let p = (t - a.time) / span;
	if (typeof a.curve === 'number') p = bezierY(p, a.curve, a.c2 ?? 0, a.c3 ?? 1, a.c4 ?? 1);
	return mixColor(at(a), at(b), p);
};
