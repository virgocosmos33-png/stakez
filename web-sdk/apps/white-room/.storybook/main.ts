// https://github.com/storybookjs/storybook/issues/29567
import type { StorybookConfig } from '@storybook/sveltekit';
import { searchForWorkspaceRoot } from 'vite';
import { main } from 'config-storybook';

// Extend the shared config with a Vite fs.allow for the monorepo root so
// @fs-served package assets (e.g. the cinzel / cormorant webfonts under
// packages/components-ui-html/src/fonts) load in Storybook instead of 403ing.
const config: StorybookConfig = {
	...main,
	viteFinal: async (cfg) => {
		const root = searchForWorkspaceRoot(process.cwd());
		cfg.server = cfg.server ?? {};
		cfg.server.fs = cfg.server.fs ?? {};
		cfg.server.fs.allow = [...(cfg.server.fs.allow ?? []), root];
		return cfg;
	},
};

export default config;
