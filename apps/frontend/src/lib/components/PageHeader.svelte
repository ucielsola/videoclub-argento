<script lang="ts">
import type { Snippet } from "svelte";
import { movies } from "$lib/state";
import CategoryChips from "./CategoryChips.svelte";
import FilterPills from "./FilterPills.svelte";
import HeaderSearch from "./HeaderSearch.svelte";
import Logo from "./Logo.svelte";
import SortControls from "./SortControls.svelte";
import ThemeToggle from "./ThemeToggle.svelte";
import WatchlistTabs from "./WatchlistTabs.svelte";

interface Props {
	title?: string;
	actionsSlot?: Snippet;
}

let { title = "Video Club Argento", actionsSlot }: Props = $props();

let hasActiveFilters = $derived(
	movies.searchQuery !== "" ||
		movies.activeFilter !== "all" ||
		movies.sortBy !== "year" ||
		movies.sortDirection !== "desc" ||
		movies.watchlistFilter !== null ||
		movies.categoryFilter !== null,
);
</script>

<div class="h-56 md:h-52"></div>

<header
    class="fixed top-0 left-0 right-0 z-50 bg-white/70 dark:bg-gray-900/70 backdrop-blur-[20px] backdrop-saturate-[1.8]"
>
    <div
        class="absolute inset-0 opacity-[0.07] text-gray-400 dark:text-gray-500 pointer-events-none z-0 bg-grid-pattern"
    ></div>

    <div
        class="relative z-10 h-1 bg-linear-to-r from-indigo-500 via-purple-500 to-pink-500"
    ></div>

    <div class="container mx-auto px-4 relative z-10">
        <div
            class="flex items-center justify-between pt-4 pb-2 md:pt-5 md:pb-3"
        >
            <div class="flex items-center gap-5">
                <div
                    class="rounded-xl p-3 bg-linear-to-br from-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/20"
                >
                    <Logo />
                </div>
                <h1
                    class="font-bold text-4xl md:text-5xl leading-tight bg-linear-to-r from-indigo-600 via-purple-600 to-pink-600 dark:from-indigo-400 dark:via-purple-400 dark:to-pink-400 bg-clip-text text-transparent"
                >
                    {title}
                </h1>
            </div>
            <div class="flex items-center gap-2">
                <WatchlistTabs />
                <ThemeToggle />
                {#if actionsSlot}
                    {@render actionsSlot()}
                {/if}
            </div>
        </div>

        <div class="flex justify-center pb-2">
            <HeaderSearch />
        </div>

        <div class="pb-2">
            <CategoryChips />
        </div>

        <div
            class="flex flex-col md:flex-row items-center justify-between gap-3 pb-4 md:pb-3"
        >
            <div class="order-2 md:order-1 md:flex-1 text-center md:text-left">
                <span class="text-xs text-gray-500 dark:text-gray-400">
                    Mostrando <b
                        class="font-medium text-gray-700 dark:text-gray-200"
                        >{movies.filteredList.length}</b
                    >
                    de {movies.list.length} películas
                </span>
            </div>

			<div
				class="order-1 md:order-2 w-full md:w-auto flex md:flex-2 justify-between md:justify-center items-center gap-2 md:gap-3"
			>
				<div
					class="overflow-x-auto whitespace-nowrap [-webkit-overflow-scrolling:touch] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
				>
					<FilterPills />
				</div>

				<div class="shrink-0 md:flex-1 flex items-center gap-2 justify-end">
					{#if hasActiveFilters}
						<button
							onclick={() => movies.resetFilters()}
							class="text-xs px-3 py-1 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
						>
							Quitar todos los filtros
						</button>
					{/if}
					<SortControls />
				</div>
			</div>
        </div>
    </div>
</header>
