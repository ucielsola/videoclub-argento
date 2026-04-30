<script lang="ts">
import { onMount } from "svelte";
import Footer from "$lib/components/Footer.svelte";
import MovieGrid from "$lib/components/MovieGrid.svelte";
import PageHeader from "$lib/components/PageHeader.svelte";
import { movies } from "$lib/state";
import type { MovieListItem } from "$lib/types";

interface Props {
	data: { movies: MovieListItem[] };
}
let { data }: Props = $props();

onMount(() => {
	console.log(
		"[+page.svelte] data.movies:",
		data.movies?.length,
		data.movies?.slice(0, 2),
	);
	movies.initialize(data.movies);
	console.log(
		"[+page.svelte] store.list:",
		movies.list.length,
		"filteredList:",
		movies.filteredList.length,
	);
});
</script>

<PageHeader />

<div class="container mx-auto px-4 py-6 pb-20">
	{#if data.movies.length === 0}
		<div class="text-center py-12">
			<p class="text-gray-500 dark:text-gray-400">
				No se encontraron películas.
			</p>
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
