<script lang="ts">
	import { type Snippet } from 'svelte';
	import { GlobalStyle } from 'components-ui-html';
	import { Authenticate, LoaderBase, LoadI18n } from 'components-shared';
	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';

	import messagesMap from '../i18n/messagesMap';

	type Props = { children: Snippet };

	const props: Props = $props();

	const loaderUrl = new URL('../../loader.gif', import.meta.url).href;

	setContext();
</script>

<GlobalStyle>
	<Authenticate>
		<LoadI18n {messagesMap}>
			<Game />
		</LoadI18n>
	</Authenticate>
</GlobalStyle>

<!-- Stake Engine loader removed per Stake review — straight to the studio loader.
	Drama Studios logo loader on black (static/loader.gif) -->
<LoaderBase maxWidth={360} backgroundColor={'#000000'} timeout={2000} src={loaderUrl} />

{@render props.children()}