<script lang="ts">
    import type { Snippet } from "svelte";

    import { movies } from "$lib/state";
    import FilterPills from "./FilterPills.svelte";
    import HeaderSearch from "./HeaderSearch.svelte";
    import SortControls from "./SortControls.svelte";
    import Logo from "./Logo.svelte";
    import ThemeToggle from "./ThemeToggle.svelte";

    interface Props {
        title?: string;
        actionsSlot?: Snippet;
    }

    let { title = "Video Club Argento", actionsSlot }: Props = $props();
</script>

<div class="header-spacer"></div>

<header class="page-header fixed top-0 left-0 right-0 z-50">
    <div class="header-grid bg-grid-pattern"></div>
    <div class="gradient-bar"></div>

    <div class="container mx-auto px-4 relative z-10">
        <div class="header-row">
            <div class="flex items-center gap-5">
                <div class="logo-box">
                    <Logo />
                </div>
                <h1 class="title">{title}</h1>
            </div>
            <div class="flex items-center gap-2">
                <ThemeToggle />
                {#if actionsSlot}
                    {@render actionsSlot()}
                {/if}
            </div>
        </div>

        <div class="search-row">
            <HeaderSearch />
        </div>

        <div class="controls-row">
            <div class="flex-1">
                <span class="text-xs text-gray-500 dark:text-gray-400">
                    Mostrando {movies.filteredList.length} de {movies.list
                        .length} películas
                </span>
            </div>
            <FilterPills />
            <div class="flex-1 flex justify-end">
                <SortControls />
            </div>
        </div>
    </div>
</header>

<style>
    .header-spacer {
        height: 11.5rem;
    }

    @media (min-width: 768px) {
        .header-spacer {
            height: 13rem;
        }
    }

    .page-header {
        background: rgb(255 255 255 / 0.7);
        backdrop-filter: blur(20px) saturate(1.8);
        -webkit-backdrop-filter: blur(20px) saturate(1.8);
    }

    :global(.dark) .page-header {
        background: rgb(17 24 39 / 0.7);
    }

    .header-grid {
        position: absolute;
        inset: 0;
        opacity: 0.07;
        color: rgb(156 163 175);
        pointer-events: none;
        z-index: 0;
    }

    :global(.dark) .header-grid {
        color: rgb(107 114 128);
    }

    .gradient-bar {
        position: relative;
        z-index: 1;
        height: 4px;
        background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
    }

    .header-row {
        padding: 1rem 0 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    @media (min-width: 768px) {
        .header-row {
            padding: 1.25rem 0 0.75rem;
        }
    }

    .search-row {
        display: flex;
        justify-content: center;
        padding-bottom: 0.5rem;
    }

    .controls-row {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-bottom: 0.75rem;
        gap: 0.75rem;
    }

    .logo-box {
        border-radius: 0.75rem;
        padding: 0.75rem;
        background: linear-gradient(to bottom right, #6366f1, #9333ea);
        box-shadow: 0 10px 15px -3px rgb(99 102 241 / 0.2);
    }

    .logo-icon {
        width: 2.25rem;
        height: 2.25rem;
    }

    .title {
        font-weight: 700;
        font-size: 2.25rem;
        line-height: 1.2;
        background: linear-gradient(to right, #4f46e5, #9333ea, #db2777);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    :global(.dark) .title {
        background: linear-gradient(to right, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        background-clip: text;
    }

    @media (min-width: 768px) {
        .title {
            font-size: 3rem;
        }
    }
</style>
