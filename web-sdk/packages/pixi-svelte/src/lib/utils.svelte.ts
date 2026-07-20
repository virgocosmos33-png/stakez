import type { PixiPoint, Sizes } from './types';

export const REM = 16;
export const MIN_CLICKABLE_SIZE = 3 * REM; // 44 x 44 is minimum clickable size

export const getPointValues = ({
	point,
	defaultValue,
}: {
	point: PixiPoint;
	defaultValue: number;
}) => {
	const finalDefaultValue = defaultValue === undefined ? 0 : defaultValue;
	if (typeof point === 'number') return [point, point];
	return [point?.x || finalDefaultValue, point?.y || finalDefaultValue];
};

export const anchorToPivot = ({ anchor, sizes }: { anchor: PixiPoint; sizes: Sizes }) => {
	const { width, height } = sizes;
	const [anchorX, anchorY] = getPointValues({ point: anchor, defaultValue: 0 });
	return { x: width * anchorX, y: height * anchorY };
};

/**
 * Detects if WebGL is enabled.
 * Inspired from http://www.browserleaks.com/webgl#howto-detect-webgl
 *
 * @return { number } -1 for not Supported,
 *										0 for disabled
 *										1 for enabled
 */
export function detectWebGL() {
	// Check for the WebGL rendering context
	if (window && !!window.WebGLRenderingContext) {
		let canvas = document.createElement('canvas'),
			names = ['webgl', 'experimental-webgl', 'moz-webgl', 'webkit-3d'],
			context = false;

		for (const i in names) {
			try {
				// @ts-ignore
				context = canvas.getContext(names[i]);
				// @ts-ignore
				if (context && typeof context.getParameter === 'function') {
					// WebGL is enabled.
					return 1;
				}
			} catch (e) {}
		}

		// WebGL is supported, but disabled.
		return 0;
	}

	// WebGL not supported.
	return -1;
}

// Stake Engine XSS policy: the game build must be fully static and cannot
// reach external sources (the previous Typekit/webfontloader fetch violated
// this). The Drama Studios house faces (Cinzel / Cormorant Garamond) are
// bundled locally via @font-face in components-ui-html/global.scss; here we
// just force the browser to fetch them before the Pixi canvas rasterizes any
// text, otherwise the first frames fall back to a system font.
export const preloadFont = async () => {
	if (typeof document === 'undefined' || !document.fonts?.load) return;
	const faces = [
		'400 16px Cinzel',
		'700 16px Cinzel',
		'900 16px Cinzel',
		'700 16px "Cinzel Decorative"',
		'400 16px "Cormorant Garamond"',
		'600 16px "Cormorant Garamond"',
	];
	// NEVER let font loading gate app startup: race against a short timeout so a
	// slow/blocked woff2 can't leave the canvas on a permanent loading screen.
	// (font-display:block already handles the visual swap once faces arrive.)
	const load = Promise.all(faces.map((face) => document.fonts.load(face))).catch(() => {});
	const timeout = new Promise((resolve) => setTimeout(resolve, 1500));
	await Promise.race([load, timeout]);
};

export function propsSyncEffect<TProps extends object, TTarget>({
	props,
	target,
	ignore,
}: {
	props: TProps;
	target?: TTarget | (() => TTarget);
	ignore?: (keyof TProps)[];
}) {
	$effect(() => {
		// The whole thing is wrapped inside an $effect
		// and because of ”props[key]“，it will react with every single props updated.
		let targetInstance = target instanceof Function ? target() : target;
		if (targetInstance) {
			(Object.keys(props) as (keyof TProps)[])
				.filter((key) => (ignore ? !ignore.includes(key) : true))
				.forEach((key) => {
					if (props[key] !== undefined) {
						// @ts-ignore
						targetInstance[key] = props[key];
					}
				});
		}
	});
}
