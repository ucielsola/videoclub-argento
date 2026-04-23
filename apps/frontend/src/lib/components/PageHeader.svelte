<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title?: string;
		children: Snippet;
		actionsSlot?: Snippet;
	}

	let { title = 'Video Club Argento', children, actionsSlot }: Props = $props();
</script>

<div class="relative overflow-hidden">
	<div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" />

	<div class="container mx-auto px-4 py-14 md:py-20 relative">
		<div class="flex flex-col sm:flex-row justify-between items-center mb-8">
			<div class="flex items-center gap-5">
				<div class="bg-gradient-to-br from-indigo-500 to-purple-600 p-3 rounded-xl shadow-lg shadow-indigo-500/20">
					<svg class="w-9 h-9 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 4h16a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1z" />
					</svg>
				</div>
				<h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 dark:from-indigo-400 dark:via-purple-400 dark:to-pink-400 bg-clip-text text-transparent">
					{title}
				</h1>
			</div>
			{#if actionsSlot}
				{@render actionsSlot()}
			{/if}
		</div>

		<div class="max-w-2xl mx-auto">
			{@render children()}
		</div>
	</div>
</div>