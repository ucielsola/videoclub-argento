<script lang="ts">
import { onMount } from "svelte";
import Footer from "$lib/components/Footer.svelte";
import MovieGrid from "$lib/components/MovieGrid.svelte";
import PageHeader from "$lib/components/PageHeader.svelte";
import { movies, watchlist } from "$lib/state";
import type { MovieListItem } from "$lib/types";

interface Props {
	data: { movies: MovieListItem[] };
}

let { data }: Props = $props();

onMount(() => {
	movies.initialize(data.movies);
});

let activeTab = $state<"quiero" | "visto">("quiero");

const filteredMovies = $derived(
	movies.list.filter((m) => {
		const slugs =
			activeTab === "quiero" ? watchlist.quieroVerList : watchlist.yaLaViList;
		return slugs.includes(m.slug);
	}),
);
</script>

<PageHeader
	title="Mis Listas"
	actionsSlot={() => {
		return (
			<div class="flex gap-2">
				<button
					onclick={() => (activeTab = "quiero")}
					class="px-3 py-1.5 text-xs rounded-full transition-colors {activeTab === 'quiero' ? 'bg-blue-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'}"
				>
					Quiero ver ({watchlist.quieroVerList.length})
				</button>
				<button
					onclick={() => (activeTab = "visto")}
					class="px-3 py-1.5 text-xs rounded-full transition-colors {activeTab === 'visto' ? 'bg-green-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'}"
				>
					Ya la vi ({watchlist.yaLaViList.length})
				</button>
			</div>
		);
	}}
/>

<div class="container mx-auto px-4 py-6 pb-20">
	{#if filteredMovies.length === 0}
		<div class="text-center py-12">
			<p class="text-gray-500 dark:text-gray-400">
				{activeTab === "quiero"
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
