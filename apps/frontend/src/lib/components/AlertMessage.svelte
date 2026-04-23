<script lang="ts">
	import { Alert } from 'flowbite-svelte';
	import { movies } from '$lib/state';
</script>

{#if movies.error}
	<Alert color="red" class="mb-6">
		<span class="font-medium">¡Error!</span> {movies.error}
	</Alert>
{/if}

{#if movies.syncMessage}
	<Alert color="green" class="mb-6">
		<span class="font-medium">¡Éxito!</span> {movies.syncMessage}
	</Alert>
{/if}