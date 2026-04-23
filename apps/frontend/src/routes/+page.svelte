<script lang="ts">
import { Spinner } from "flowbite-svelte";
import { onMount } from "svelte";
import AlertMessage from "$lib/components/AlertMessage.svelte";
import FilterButtons from "$lib/components/FilterButtons.svelte";
import Footer from "$lib/components/Footer.svelte";
import MovieGrid from "$lib/components/MovieGrid.svelte";
import PageHeader from "$lib/components/PageHeader.svelte";
import SearchBar from "$lib/components/SearchBar.svelte";
import SyncButton from "$lib/components/SyncButton.svelte";
import { movies } from "$lib/state";

onMount(() => {
	movies.loadMovies();
});
</script>

<PageHeader>
	{#snippet children()}
		<SearchBar />
		<FilterButtons />
	{/snippet}

	{#snippet actionsSlot()}
		<SyncButton />
	{/snippet}
</PageHeader>

<div class="container mx-auto px-4 py-6 pb-20">
	<AlertMessage />

	{#if movies.loading}
		<div class="flex justify-center items-center h-64">
			<Spinner size="12" />
		</div>
	{:else if movies.list.length === 0}
		<div class="text-center py-12">
			<p class="text-gray-500 dark:text-gray-400">No se encontraron películas. Haz clic en "Sincronizar" para cargarlas.</p>
		</div>
	{:else}
		<MovieGrid />
	{/if}
</div>

<Footer>
	{#snippet children()}
		<p>Video Club Argento &copy; {new Date().getFullYear()}</p>
	{/snippet}
</Footer>
