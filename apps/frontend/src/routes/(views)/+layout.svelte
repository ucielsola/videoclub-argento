<script lang="ts">
import Footer from "$lib/components/Footer.svelte";
import Logo from "$lib/components/Logo.svelte";
import ThemeToggle from "$lib/components/ThemeToggle.svelte";

let { children } = $props();
</script>

<div class="fixed top-0 left-0 right-0 z-50 bg-white/70 dark:bg-gray-900/70 backdrop-blur-[20px] backdrop-saturate-[1.8]">
	<div class="relative z-10 h-1 bg-linear-to-r from-indigo-500 via-purple-500 to-pink-500"></div>

	<div class="container mx-auto px-4 relative z-10">
		<div class="flex items-center justify-between py-2">
			<a href="/" class="flex items-center gap-3">
				<div
					class="rounded-md p-1.5 bg-linear-to-br from-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/20"
				>
					<Logo />
				</div>
				<h1
					class="font-bold text-lg bg-linear-to-r from-indigo-600 via-purple-600 to-pink-600 dark:from-indigo-400 dark:via-purple-400 dark:to-pink-400 bg-clip-text text-transparent"
				>
					Video Club Argento
				</h1>
			</a>
			<ThemeToggle />
		</div>
	</div>
</div>

<div class="pt-24 pb-20">{@render children()}</div>

<Footer>
	<p>Built with ❤️ for Argentine cinema</p>
</Footer>
