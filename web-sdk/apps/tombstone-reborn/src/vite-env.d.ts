/// <reference types="vite/client" />

declare module '*.atlas?raw' {
	const text: string;
	export default text;
}

declare module '@esotericsoftware/spine-pixi-v8';
