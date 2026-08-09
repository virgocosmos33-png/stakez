import { createAsset } from 'pixi-svelte';

import img from './loadingParticles.webp';
import atlas from './loadingParticles.json';

export default createAsset({ img, atlas, preload: true });
