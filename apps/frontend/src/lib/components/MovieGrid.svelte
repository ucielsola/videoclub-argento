<script lang="ts">
	import type { MovieListItem, SortMode } from '$lib/types';
	import VirtualList from './VirtualList.svelte';
	import MovieCard from './MovieCard.svelte';
	import { Alert, Badge } from 'flowbite-svelte';
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

	let gridOpacity = $state(1);
	let gridTranslateY = $state(0);
	let timeout: ReturnType<typeof setTimeout> | undefined;

	function setSort(mode: SortMode) {
		if (mode === movies.sortBy) return;
		gridOpacity = 0;
		gridTranslateY = 8;
		clearTimeout(timeout);
		timeout = setTimeout(() => {
			movies.sortBy = mode;
			gridOpacity = 1;
			gridTranslateY = 0;
		}, 200);
	}
</script>

<div class="flex items-center gap-3 mb-4">
	<span class="text-sm font-medium text-gray-700 dark:text-gray-300">Ordenar por:</span>
	<Badge
		large
		color={movies.sortBy === 'title' ? 'brand' : 'gray'}
		rounded
		onclick={() => setSort('title')}
		class="cursor-pointer select-none"
	>
		Título
	</Badge>
	<Badge
		large
		color={movies.sortBy === 'year' ? 'brand' : 'gray'}
		rounded
		onclick={() => setSort('year')}
		class="cursor-pointer select-none"
	>
		Año
	</Badge>
</div>

<div
	class="transition-[opacity,transform] duration-200 ease-out"
	style="opacity: {gridOpacity}; transform: translateY({gridTranslateY}px);"
>
	<VirtualList
		bind:this={virtualList}
		items={movies.filteredList}
		{itemHeight}
		{overscan}
		useWindowScroll={true}
	>
		{#snippet row({ item, index }: { item: MovieListItem; index: number })}
			<div class="p-2 h-[280px]">
				<MovieCard movie={item} />
			</div>
		{/snippet}
	</VirtualList>

	{#if movies.filteredList.length === 0 && movies.list.length > 0}
		<div class="mt-8">
			<Alert color="yellow">
				<span class="font-medium">No se encontraron películas.</span>
				<span>Intenta con otro término de búsqueda.</span>
			</Alert>
		</div>
	{/if}
</div>
