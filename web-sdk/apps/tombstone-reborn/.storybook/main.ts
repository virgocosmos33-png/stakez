// https://github.com/storybookjs/storybook/issues/29567
import type { StorybookConfig } from '@storybook/sveltekit';
import { searchForWorkspaceRoot } from 'vite';
import { main } from 'config-storybook';

// Extend the shared config with a Vite fs.allow for the monorepo root so
// @fs-served package assets (e.g. the cinzel / cormorant webfonts under
// packages/components-ui-html/src/fonts) load in Storybook instead of 403ing.
const config: StorybookConfig = {
	...main,
	// App static/ (hanging_lamps atlas + PNG siblings), not the config-package path.
	staticDirs: ['../static'],
	viteFinal: async (cfg) => {
		const root = searchForWorkspaceRoot(process.cwd());
		cfg.server = cfg.server ?? {};
		cfg.server.fs = cfg.server.fs ?? {};
		cfg.server.fs.allow = [...(cfg.server.fs.allow ?? []), root];
		// Two dev servers sharing node_modules/.vite thrash each other's
		// dep-optimizer output, which serves stale package builds. Set
		// STORYBOOK_VITE_CACHE_DIR to give a second instance its own cache.
		if (process.env.STORYBOOK_VITE_CACHE_DIR) cfg.cacheDir = process.env.STORYBOOK_VITE_CACHE_DIR;
		return cfg;
	},
};

export default config;
