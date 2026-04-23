<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title?: string;
		children: Snippet;
		actionsSlot?: Snippet;
	}

	let { title = 'Video Club Argento', children, actionsSlot }: Props = $props();

	let scrolled = $state(false);

	$effect(() => {
		const onScroll = () => {
			scrolled = window.scrollY > 50;
		};
		onScroll();
		window.addEventListener('scroll', onScroll, { passive: true });
		return () => window.removeEventListener('scroll', onScroll);
	});
</script>

<div
	class="sticky top-0 relative transition-all duration-300 {scrolled
		? 'z-50 shadow-lg shadow-black/5 bg-gray-50/80 dark:bg-gray-800/80 backdrop-blur-lg'
		: ''}"
>
	<div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 transition-all duration-300 {scrolled ? 'h-0.5 opacity-60' : ''}"></div>

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
			{#if actionsSlot}
				{@render actionsSlot()}
			{/if}
		</div>

		<div class="max-w-2xl mx-auto">
			{@render children()}
		</div>
	</div>
</div>
