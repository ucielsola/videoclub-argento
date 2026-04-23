<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		children: Snippet;
	}

	let { children }: Props = $props();
</script>

<footer class="bg-gray-100 dark:bg-gray-800 py-6 mt-8">
	<div class="container mx-auto px-4 text-center text-gray-500 dark:text-gray-400">
		{@render children()}
	</div>
</footer>