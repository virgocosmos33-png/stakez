/**
 * Cell-pocket blood from https://codepen.io/rafaelcastrocouto/pen/nJyGmv
 *
 * Pen grammar: small red drops, uneven viscous speed (full or /3), trails
 * from a near-zero fade. Transparent field — no black plate.
 *
 * Faces sit on studio black (no knockout). A sprite mask of l1.webp is the
 * whole card, so blood leaked onto the field and past the letter. Clip here
 * with a letter-only alpha (near-black punched out). Pocket clip stays on
 * the parent CellClipMask.
 *
 * BLOOD_DETECTABLE is the try-it punch. Set false to go back to the thin pen.
 * Every stream starts on the letter's real top edge at that column, then falls.
 */
import { Texture } from 'pixi.js';

import type { SymbolName } from './types';

/** Try-it punch. False = thin CodePen size. */
export const BLOOD_DETECTABLE = true;

/** [x, y, r, speed] on the pen's 600×200 canvas. */
const PEN_DROPS: ReadonlyArray<readonly [number, number, number, number]> = [
	[10, 70, 1, 2],
	[35, 32, 1, 1.5],
	[53, 72, 1.5, 1],
	[80, 74, 2, 1.7],
	[100, 68, 1, 1.3],
	[154, 71, 1, 1.9],
	[174, 71, 1, 1.4],
	[222, 76, 1.3, 1.1],
	[263, 72, 1.8, 0.7],
	[280, 75, 1.4, 1.3],
	[325, 72, 1.8, 1.2],
	[380, 75, 1.4, 0.9],
	[395, 88, 0.8, 1.3],
	[418, 70, 1.2, 1.6],
	[466, 67, 0.8, 1.3],
	[487, 71, 1.2, 1.2],
	[512, 74, 1.7, 1.5],
	[542, 74, 1.7, 0.8],
];

const PEN_W = 600;
const PEN_H = 200;
const FADE = 'rgba(0,0,0,0.005)';
const WOBBLE = BLOOD_DETECTABLE ? 2.2 : 3;
const R_MUL = BLOOD_DETECTABLE ? 2.8 : 1;
const BLOOD = BLOOD_DETECTABLE ? 'rgba(196, 12, 12, 1)' : 'red';
const BLACK_SUM = 36;

export const LOW_FACE_KEY: Record<string, string> = {
	L1: 'l1.webp',
	L2: 'l2.webp',
	L3: 'l3.webp',
	L4: 'l4.webp',
	L5: 'l5.webp',
};

export const lowFaceKey = (name: SymbolName) => LOW_FACE_KEY[name];

export type BloodDrop = {
	x: number;
	y0: number;
	y: number;
	r: number;
	speed: number;
};

export type BloodPlate = {
	canvas: HTMLCanvasElement;
	ctx: CanvasRenderingContext2D;
	texture: Texture;
	mask: HTMLCanvasElement;
	drops: BloodDrop[];
	floor: number;
	w: number;
	h: number;
};

const isDrawable = (src: unknown): src is CanvasImageSource =>
	src instanceof HTMLImageElement ||
	src instanceof HTMLCanvasElement ||
	(typeof ImageBitmap !== 'undefined' && src instanceof ImageBitmap);

const isLetterPixel = (r: number, g: number, b: number, a: number) => {
	if (a < 8) return false;
	if (r > 48) return true;
	return r + g + b > BLACK_SUM;
};

/** Studio-black field out. Letter stone / gold / wet red stay. */
export const letterMaskFromTexture = (tex: Texture, w: number, h: number) => {
	const canvas = document.createElement('canvas');
	canvas.width = w;
	canvas.height = h;
	const ctx = canvas.getContext('2d');
	if (!ctx) throw new Error('low-link blood: no mask context');
	const src = tex.source.resource;
	if (!isDrawable(src) || tex.frame.width < 2) return canvas;
	ctx.drawImage(src, tex.frame.x, tex.frame.y, tex.frame.width, tex.frame.height, 0, 0, w, h);
	const img = ctx.getImageData(0, 0, w, h);
	const d = img.data;
	for (let i = 0; i < d.length; i += 4) {
		const keep = isLetterPixel(d[i], d[i + 1], d[i + 2], d[i + 3]);
		d[i] = 255;
		d[i + 1] = 255;
		d[i + 2] = 255;
		d[i + 3] = keep ? 255 : 0;
	}
	ctx.putImageData(img, 0, 0);
	return canvas;
};

const letterBounds = (mask: HTMLCanvasElement) => {
	const ctx = mask.getContext('2d');
	if (!ctx) return { x0: 0, y0: 0, x1: mask.width, y1: mask.height };
	const img = ctx.getImageData(0, 0, mask.width, mask.height);
	const d = img.data;
	let x0 = mask.width;
	let y0 = mask.height;
	let x1 = 0;
	let y1 = 0;
	for (let y = 0; y < mask.height; y += 1) {
		for (let x = 0; x < mask.width; x += 1) {
			if (d[(y * mask.width + x) * 4 + 3] < 8) continue;
			if (x < x0) x0 = x;
			if (y < y0) y0 = y;
			if (x > x1) x1 = x;
			if (y > y1) y1 = y;
		}
	}
	if (x1 <= x0 || y1 <= y0) return { x0: 0, y0: 0, x1: mask.width, y1: mask.height };
	return { x0, y0, x1, y1 };
};

const columnTop = (alpha: Uint8ClampedArray, width: number, height: number, x: number) => {
	const col = Math.round(x);
	if (col < 0 || col >= width) return -1;
	for (let y = 0; y < height; y += 1) {
		if (alpha[(y * width + col) * 4 + 3] > 8) return y;
	}
	return -1;
};

const topEdgeAt = (alpha: Uint8ClampedArray, width: number, height: number, x: number) => {
	for (const dx of [0, 1, -1, 2, -2, 3, -3, 4, -4, 6, -6]) {
		const y = columnTop(alpha, width, height, x + dx);
		if (y >= 0) return { x: x + dx, y };
	}
	return null;
};

export const makeBloodPlate = (w: number, h: number, face: Texture): BloodPlate => {
	const canvas = document.createElement('canvas');
	canvas.width = Math.max(8, Math.round(w));
	canvas.height = Math.max(8, Math.round(h));
	const ctx = canvas.getContext('2d');
	if (!ctx) throw new Error('low-link blood: no 2d context');
	const mask = letterMaskFromTexture(face, canvas.width, canvas.height);
	const box = letterBounds(mask);
	const bw = box.x1 - box.x0;
	const bh = box.y1 - box.y0;
	const maskCtx = mask.getContext('2d');
	if (!maskCtx) throw new Error('low-link blood: no mask pixels');
	const alpha = maskCtx.getImageData(0, 0, mask.width, mask.height).data;
	const drops: BloodDrop[] = [];
	const push = (penX: number, r: number, speed: number) => {
		const edge = topEdgeAt(alpha, mask.width, mask.height, box.x0 + (penX / PEN_W) * bw);
		if (!edge) return;
		const radius = Math.max(1.1, r * (bh / PEN_H) * R_MUL);
		const y0 = edge.y + radius * 0.35;
		drops.push({
			x: edge.x,
			y0,
			y: y0,
			r: radius,
			speed: speed * (bh / PEN_H),
		});
	};
	for (const [x, , r, speed] of PEN_DROPS) push(x, r, speed);
	if (BLOOD_DETECTABLE) {
		for (const [x, , r, speed] of PEN_DROPS) {
			if (x % 80 < 40) push(x + 18, r * 0.85, speed * 0.8);
		}
	}
	return {
		canvas,
		ctx,
		texture: Texture.from(canvas),
		mask,
		drops,
		floor: box.y1 - 2,
		w: canvas.width,
		h: canvas.height,
	};
};

export const tickBloodPlate = (plate: BloodPlate) => {
	const { ctx, w, h, drops, texture, mask } = plate;
	ctx.globalCompositeOperation = 'destination-out';
	ctx.fillStyle = FADE;
	ctx.fillRect(0, 0, w, h);
	ctx.globalCompositeOperation = 'source-over';
	ctx.fillStyle = BLOOD;
	const floor = plate.floor;
	for (const drop of drops) {
		drop.y += Math.random() > 0.5 ? drop.speed : drop.speed / 3;
		if (drop.y > floor) drop.y = drop.y0;
		const dx = Math.sin(drop.y * 0.07 + drop.x * 0.03) * WOBBLE;
		const x = drop.x + 1 + dx;
		ctx.beginPath();
		ctx.arc(x, drop.y, drop.r, 0, Math.PI * 2);
		if (BLOOD_DETECTABLE) ctx.arc(x, drop.y + drop.r * 0.7, drop.r * 0.72, 0, Math.PI * 2);
		ctx.fill();
	}
	ctx.globalCompositeOperation = 'destination-in';
	ctx.drawImage(mask, 0, 0);
	ctx.globalCompositeOperation = 'source-over';
	texture.source.update();
};

export const destroyBloodPlate = (plate: BloodPlate) => {
	plate.texture.destroy(true);
};
