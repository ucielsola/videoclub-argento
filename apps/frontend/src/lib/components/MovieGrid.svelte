<script lang="ts">
	import type { MovieListItem } from '$lib/types';
	import VirtualList from './VirtualList.svelte';
	import MovieCard from './MovieCard.svelte';
	import { Alert } from 'flowbite-svelte';
	import { movies } from '$lib/state';

	let virtualList: ReturnType<typeof VirtualList> | undefined = $state();

	export function scrollToIndex(index: number, behavior?: ScrollBehavior) {
		virtualList?.scrollToIndex(index, behavior);
	}

	interface Props {
		itemHeight?: number;
		overscan?: number;
	}

	let { itemHeight = 280, overscan = 3 }: Props = $props();
</script>

<div class="flex-1 min-h-0">
	<VirtualList
		bind:this={virtualList}
		items={movies.filteredList}
		{itemHeight}
		{overscan}
	>
		{#snippet row({ item, index }: { item: MovieListItem; index: number })}
			<div class="p-2 h-[280px]">
				<MovieCard movie={item} />
			</div>
		{/snippet}
	</VirtualList>
</div>

{#if movies.filteredList.length === 0 && movies.list.length > 0}
	<div class="mt-8">
		<Alert color="yellow">
			<span class="font-medium">No se encontraron películas.</span>
			<span>Intenta con otro término de búsqueda.</span>
		</Alert>
	</div>
{/if}