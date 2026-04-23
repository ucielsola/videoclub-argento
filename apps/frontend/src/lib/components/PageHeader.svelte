<script lang="ts">
import type { Snippet } from "svelte";
import { theme } from "$lib/state";

interface Props {
	title?: string;
	children: Snippet;
	actionsSlot?: Snippet;
}

let { title = "Video Club Argento", children, actionsSlot }: Props = $props();

let scrolled = $state(false);
let rafId = 0;

function handleScroll() {
	cancelAnimationFrame(rafId);
	rafId = requestAnimationFrame(() => {
		const y = window.scrollY;
		if (!scrolled && y > 20) scrolled = true;
		else if (scrolled && y < 5) scrolled = false;
	});
}
</script>

<svelte:window onscroll={handleScroll}></svelte:window>

<div
	class="sticky top-0 transition-all duration-300 {scrolled
		? 'z-50 shadow-lg shadow-black/5 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg'
		: ''}"
>
	<div class="absolute top-0 left-0 right-0 h-1 bg-linear-to-r from-indigo-500 via-purple-500 to-pink-500 transition-all duration-300 {scrolled ? 'h-0.5 opacity-60' : ''}"></div>

	<div
		class="container mx-auto px-4 relative transition-all duration-300 ease-in-out {scrolled
			? 'py-3 md:py-4'
			: 'py-14 md:py-20'}"
	>
		<div
			class="flex flex-col sm:flex-row justify-between items-center transition-all duration-300 ease-in-out {scrolled
				? 'mb-3'
				: 'mb-8'}"
		>
			<div class="flex items-center gap-5">
				<div
					class="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl shadow-lg shadow-indigo-500/20 transition-all duration-300 ease-in-out {scrolled
						? 'p-2'
						: 'p-3'}"
				>
					<svg
						class="text-white transition-all duration-300 ease-in-out {scrolled
							? 'w-6 h-6'
							: 'w-9 h-9'}"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 4h16a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1z"
						/>
					</svg>
				</div>
				<h1
					class="font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 dark:from-indigo-400 dark:via-purple-400 dark:to-pink-400 bg-clip-text text-transparent leading-[1.3] transition-all duration-300 ease-in-out {scrolled
						? 'text-2xl md:text-3xl'
						: 'text-4xl md:text-5xl'}"
				>
					{title}
				</h1>
			</div>
		<div class="flex items-center gap-2">
				<button
					onclick={() => theme.toggle()}
					class="rounded-full p-2 transition-colors hover:bg-gray-200 dark:hover:bg-gray-700"
					aria-label={theme.isDark ? 'Switch to light mode' : 'Switch to dark mode'}
				>
					{#if theme.isDark}
						<svg class="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
						</svg>
					{:else}
						<svg class="h-5 w-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
							<path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
						</svg>
					{/if}
				</button>
				{#if actionsSlot}
					{@render actionsSlot()}
				{/if}
			</div>
		</div>

		<div class="max-w-2xl mx-auto">
			{@render children()}
		</div>
	</div>
</div>
