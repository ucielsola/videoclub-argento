<script lang="ts">
import { movies } from "$lib/state";
import type { MovieListItem } from "$lib/types";
import MovieCard from "./MovieCard.svelte";
import VirtualList from "./VirtualList.svelte";

let virtualList: ReturnType<typeof VirtualList> | undefined = $state();

export function scrollToIndex(index: number, behavior?: ScrollBehavior) {
	virtualList?.scrollToIndex(index, behavior);
}

interface Props {
	itemHeight?: number;
	overscan?: number;
	list?: MovieListItem[];
}

let { itemHeight = 460, overscan = 12, list }: Props = $props();

let filteredList = $derived(list ?? movies.filteredList);
</script>

<VirtualList
    bind:this={virtualList}
    items={filteredList}
    {itemHeight}
    {overscan}
    useWindowScroll={true}
>
    {#snippet row({ item, index }: { item: MovieListItem; index: number })}
        <div class="p-2 h-70">
            <MovieCard movie={item} />
        </div>
    {/snippet}
</VirtualList>

{#if filteredList.length === 0 && movies.list.length > 0}
    <div class="mt-8 flex flex-col items-center gap-2 text-gray-500 dark:text-gray-400">
        <span class="text-lg">No se encontraron películas</span>
        <span class="text-sm">Intenta con otro término de búsqueda</span>
        <button
            onclick={() => movies.resetFilters()}
            class="mt-2 text-sm px-4 py-1.5 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
        >
            Quitar todos los filtros
        </button>
    </div>
{/if}
