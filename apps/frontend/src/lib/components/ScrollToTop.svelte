<script lang="ts">
import { ArrowUp } from "lucide-svelte";

let visible = $state(false);

function onScroll() {
	visible = window.scrollY > 400;
}

function scrollToTop() {
	window.scrollTo({ top: 0, behavior: "smooth" });
}
</script>

<svelte:window onscroll={onScroll} />

{#if visible}
	<button
		type="button"
		onclick={scrollToTop}
		class="fixed bottom-6 right-6 z-50 rounded-full bg-gray-800 p-3 text-white shadow-lg transition-opacity hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 dark:bg-gray-200 dark:text-gray-800 dark:hover:bg-gray-300"
		aria-label="Scroll to top"
	>
		<ArrowUp class="h-5 w-5" />
	</button>
{/if}
