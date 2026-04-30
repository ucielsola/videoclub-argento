<script lang="ts">
import { Alert } from "flowbite-svelte";
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
}

let { itemHeight = 280, overscan = 24 }: Props = $props();

let filteredList = $derived(movies.filteredList);
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
    <div class="mt-8">
        <Alert color="yellow">
            <span class="font-medium">No se encontraron películas.</span>
            <span>Intenta con otro término de búsqueda.</span>
        </Alert>
    </div>
{/if}
