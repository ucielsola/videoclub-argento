<script lang="ts">
interface Props {
	text: string;
	children: import("svelte").Snippet;
}

let { text, children }: Props = $props();

let visible = $state(false);
let el: HTMLDivElement | undefined = $state();
</script>

<span class="relative inline-flex">
    <span
        class="inline-flex"
        onmouseenter={() => (visible = true)}
        onmouseleave={() => (visible = false)}
        onfocus={() => (visible = true)}
        onblur={() => (visible = false)}
    >
        {@render children()}
    </span>
    {#if visible}
        <div
            bind:this={el}
            role="tooltip"
            class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2.5 py-1 text-xs font-medium text-white bg-gray-900 dark:bg-gray-700 rounded-md whitespace-nowrap pointer-events-none animate-fade-in z-50"
        >
            {text}
            <div
                class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-900 dark:border-t-gray-700"
            ></div>
        </div>
    {/if}
</span>
