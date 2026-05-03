<script lang="ts">
import { onMount } from "svelte";
import Footer from "$lib/components/Footer.svelte";
import MovieGrid from "$lib/components/MovieGrid.svelte";
import PageHeader from "$lib/components/PageHeader.svelte";
import { movies, watchlist } from "$lib/state";
import type { MovieListItem } from "$lib/types";

interface Props {
	data: { movies: MovieListItem[] };
	type: "quiero" | "visto";
}

let { data, type }: Props = $props();

onMount(() => {
	movies.initialize(data.movies);
});

const filteredMovies = $derived(
	movies.list.filter((m) => {
		const slugs =
			type === "quiero" ? watchlist.quieroVerList : watchlist.yaLaViList;
		return slugs.includes(m.slug);
	}),
);
</script>

<PageHeader />

<div class="container mx-auto px-4 py-6 pb-20">
	{#if filteredMovies.length === 0}
		<div class="text-center py-12">
			<p class="text-gray-500 dark:text-gray-400">
				{type === "quiero"
					? "No tenés películas en 'Quiero ver'"
					: "No tenés películas en 'Ya la vi'"}
			</p>
		</div>
	{:else}
		<MovieGrid list={filteredMovies} />
	{/if}
</div>

<Footer>
	{#snippet children()}
		<p>Video Club Argento &copy; {new Date().getFullYear()}</p>
	{/snippet}
</Footer>
