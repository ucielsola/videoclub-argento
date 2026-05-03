<script lang="ts">
import { onMount } from "svelte";
import Footer from "$lib/components/Footer.svelte";
import MovieGrid from "$lib/components/MovieGrid.svelte";
import PageHeader from "$lib/components/PageHeader.svelte";
import { categories, movies } from "$lib/state";
import type { Category, MovieListItem } from "$lib/types";

interface Props {
	data: { movies: MovieListItem[]; categories: Category[] };
}
let { data }: Props = $props();

onMount(() => {
	movies.initialize(data.movies);
	categories.initialize(data.categories);
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
