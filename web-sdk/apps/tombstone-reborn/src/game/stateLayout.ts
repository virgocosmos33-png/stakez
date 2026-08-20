import { createLayout } from 'utils-layout';

const layout = createLayout({
	backgroundRatio: {
		normal: 2039 / 1000,
		portrait: 1242 / 2208,
	},
	mainSizesMap: {
		desktop: { width: 1422, height: 800 },
		tablet: { width: 1422, height: 800 },
		landscape: { width: 1600, height: 900 },
		portrait: { width: 960, height: 1422 },
	},
});

const DESKTOP_STANDARD = { width: 1920, height: 1080 };

const layoutType = () => {
	const type = layout.stateLayoutDerived.layoutType();
	// Almost-square / iPad used the stacked tablet chrome and hung WAYS /
	// MULTI / WIN under the board. Same HUD and hang as desktop.
	return type === 'tablet' ? 'desktop' : type;
};

const mainLayoutStandard = () => {
	if (layout.stateLayoutDerived.layoutType() !== 'tablet') {
		return layout.stateLayoutDerived.mainLayoutStandard();
	}
	const canvas = layout.stateLayoutDerived.canvasSizes();
	const scale = Math.min(
		canvas.width / DESKTOP_STANDARD.width,
		canvas.height / DESKTOP_STANDARD.height,
	);
	return {
		x: canvas.width / 2,
		y: canvas.height / 2,
		scale,
		width: DESKTOP_STANDARD.width,
		height: DESKTOP_STANDARD.height,
		anchor: 0.5,
	};
};

export const stateLayout = layout.stateLayout;
export const stateLayoutDerived = {
	...layout.stateLayoutDerived,
	layoutType,
	mainLayoutStandard,
};
