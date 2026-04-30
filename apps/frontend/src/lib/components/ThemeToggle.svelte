<script lang="ts">
    import { Moon, Sun } from "lucide-svelte";

    import { theme } from "$lib/state";
</script>

<button
    onclick={() => theme.toggle()}
    class="rounded-full p-2 transition-colors hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer"
    aria-label={theme.isDark ? "Switch to light mode" : "Switch to dark mode"}
>
    {#if theme.isDark}
        <Sun class="h-5 w-5 text-yellow-400"></Sun>
    {:else}
        <Moon class="h-5 w-5 text-gray-600"></Moon>
    {/if}
</button>
