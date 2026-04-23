<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		children: Snippet;
	}

	let { children }: Props = $props();
</script>

<footer class="fixed bottom-0 left-0 right-0 z-40 bg-gray-100/80 dark:bg-gray-800/80 backdrop-blur-lg border-t border-gray-200 dark:border-gray-700">
	<div class="container mx-auto px-4 py-4 text-center text-gray-500 dark:text-gray-400 text-sm">
		{@render children()}
	</div>
</footer>
