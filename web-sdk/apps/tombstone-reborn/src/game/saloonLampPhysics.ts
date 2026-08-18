/**
 * Hanging lantern as a spherical pendulum. A shot dumps kinetic energy
 * into the globe: fast into the room, plus a quarter-phase left/right so
 * the path is an ellipse that shrinks until it hangs dead. After a shot
 * it does not resume the idle breeze.
 */
export type LampMode = 'idle' | 'hit' | 'hung';

export type LampBody = {
	mode: LampMode;
	theta: number;
	omega: number;
	/** + into the room, − toward the camera. */
	phi: number;
	phiOmega: number;
	/** Visual mesh strength, derived from phi. */
	punch: number;
	idlePhase: number;
	hitAge: number;
};

/** Gentle breeze — same 4s / 4.4° the lamp already had. */
export const IDLE_PERIOD = 4;
export const IDLE_AMP = (4.4 * Math.PI) / 180;
export const IDLE_OMEGA = (Math.PI * 2) / IDLE_PERIOD;

/** Oil lamp on a short chain. T = 2π √(L/g) ≈ 1.85s. */
const PENDULUM_PERIOD = 1.85;
export const PENDULUM_GL = ((Math.PI * 2) / PENDULUM_PERIOD) ** 2;
export const PENDULUM_DAMP = 0.4;

/** Shot: high speed into the plate from rest. */
export const DEPTH_IMPULSE = 0.46 * Math.sqrt(PENDULUM_GL);
/** Quarter-phase L/R seed — with the depth velocity this traces an ellipse. */
export const SIDE_AMP = 0.16;
export const DEPTH_NEAR_K = PENDULUM_GL * 7.2;
export const DEPTH_NEAR_DAMP = 0.55;
export const DEPTH_AIR = 0.18;
export const DEPTH_REF = 0.36;
export const DEPTH_NEAR = 0.42;

const HUNG_THETA = 0.004;
const HUNG_OMEGA = 0.01;
const HUNG_PHI = 0.004;
const HIT_MAX_S = 6.2;

export const STEP_DT = 1 / 120;
export const STEP_MAX = 5;

const clamp01 = (v: number) => Math.max(0, Math.min(1, v));

let sideSign = 1;

export const createLampBody = (): LampBody => ({
	mode: 'idle',
	theta: 0,
	omega: 0,
	phi: 0,
	phiOmega: 0,
	punch: 0,
	idlePhase: 0,
	hitAge: 0,
});

export const resetLampBody = (body: LampBody) => {
	body.mode = 'idle';
	body.theta = 0;
	body.omega = 0;
	body.phi = 0;
	body.phiOmega = 0;
	body.punch = 0;
	body.idlePhase = 0;
	body.hitAge = 0;
};

export const kickLampBody = (body: LampBody) => {
	body.mode = 'hit';
	body.theta = SIDE_AMP * sideSign;
	body.omega = 0;
	body.phi = 0;
	body.phiOmega = DEPTH_IMPULSE;
	body.hitAge = 0;
	sideSign *= -1;
};

const publishPunch = (body: LampBody) => {
	const raw = body.phi / DEPTH_REF;
	const signed = raw > 0 ? raw : raw * DEPTH_NEAR;
	body.punch = Math.max(-0.55, Math.min(1.25, signed));
};

const tailOf = (angle: number, vel: number) => {
	const amp = Math.hypot(angle, vel * 0.3);
	return clamp01((0.22 - amp) / 0.2);
};

const stepAxis = (
	angle: number,
	vel: number,
	dt: number,
	tail: number,
	nearWall: boolean,
) => {
	const gl = PENDULUM_GL * (1 - 0.12 * tail);
	const damp = PENDULUM_DAMP + tail * 1.55;
	let acc = -gl * Math.sin(angle) - damp * vel;
	acc -= DEPTH_AIR * vel * Math.abs(vel);
	if (nearWall && angle < 0) {
		const near = 1 - tail;
		if (near > 0.001) {
			acc += -DEPTH_NEAR_K * near * angle - DEPTH_NEAR_DAMP * near * vel;
		}
	}
	const nextVel = vel + acc * dt;
	return { angle: angle + nextVel * dt, vel: nextVel };
};

const stepIdle = (body: LampBody, dt: number) => {
	body.idlePhase += dt * IDLE_OMEGA;
	body.theta = Math.sin(body.idlePhase) * IDLE_AMP;
	body.omega = Math.cos(body.idlePhase) * IDLE_AMP * IDLE_OMEGA;
	if (body.phi !== 0 || body.phiOmega !== 0) {
		body.phi = 0;
		body.phiOmega = 0;
		body.punch = 0;
	}
};

const stepHit = (body: LampBody, dt: number) => {
	body.hitAge += dt;
	const tail = tailOf(
		Math.hypot(body.theta, body.phi),
		Math.hypot(body.omega, body.phiOmega),
	);
	const swing = stepAxis(body.theta, body.omega, dt, tail, false);
	body.theta = swing.angle;
	body.omega = swing.vel;
	const depth = stepAxis(body.phi, body.phiOmega, dt, tail, true);
	body.phi = depth.angle;
	body.phiOmega = depth.vel;
	publishPunch(body);

	const hung =
		body.hitAge > HIT_MAX_S ||
		(Math.abs(body.theta) < HUNG_THETA &&
			Math.abs(body.omega) < HUNG_OMEGA &&
			Math.abs(body.phi) < HUNG_PHI &&
			Math.abs(body.phiOmega) < HUNG_OMEGA);
	if (!hung) return;

	body.mode = 'hung';
	body.theta = 0;
	body.omega = 0;
	body.phi = 0;
	body.phiOmega = 0;
	body.punch = 0;
};

const stepHung = (body: LampBody) => {
	if (body.theta !== 0) body.theta = 0;
	if (body.omega !== 0) body.omega = 0;
	if (body.phi !== 0) body.phi = 0;
	if (body.phiOmega !== 0) body.phiOmega = 0;
	if (body.punch !== 0) body.punch = 0;
};

export const stepLampBody = (body: LampBody, dt: number) => {
	if (body.mode === 'hit') stepHit(body, dt);
	else if (body.mode === 'hung') stepHung(body);
	else stepIdle(body, dt);
};
