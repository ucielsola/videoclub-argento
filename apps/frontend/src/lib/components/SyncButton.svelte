<script lang="ts">
	import { Button, Spinner } from 'flowbite-svelte';
	import { RefreshCw } from 'lucide-svelte';
	import { movies } from '$lib/state';
</script>

<Button
	color="dark"
	onclick={() => movies.syncDatabase()}
	loading={movies.syncing}
	spinnerProps={{ size: '4', color: 'gray' }}
>
	<RefreshCw class="me-2 h-4 w-4" />
	{#if movies.syncing}
		Syncing...
	{:else}
		Sincronizar
	{/if}
</Button>