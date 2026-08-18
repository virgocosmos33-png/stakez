import {
	createLampBody,
	kickLampBody,
	resetLampBody,
	stepLampBody,
	type LampMode,
} from './saloonLampPhysics';

const body = createLampBody();

/** Published pose. Physics runs on a private body and copies once a frame. */
export const saloonLamp = $state({
	mode: 'idle' as LampMode,
	theta: 0,
	punch: 0,
	lit: true,
});

const publishLamp = () => {
	saloonLamp.mode = body.mode;
	saloonLamp.theta = body.theta;
	saloonLamp.punch = body.punch;
};

export const strikeLamp = () => {
	kickLampBody(body);
	saloonLamp.lit = false;
	publishLamp();
};

export const resetLamp = () => {
	resetLampBody(body);
	saloonLamp.lit = true;
	publishLamp();
};

export const stepLamp = (dt: number) => {
	stepLampBody(body, dt);
};

export const flushLamp = () => {
	publishLamp();
};
