<script>
import "../app.css";
import Footer from "$lib/components/Footer.svelte";
import ScrollToTop from "$lib/components/ScrollToTop.svelte";
import URLSync from "$lib/components/URLSync.svelte";

let { children } = $props();
</script>

<div class="bg-white dark:bg-gray-900 relative min-h-dvh">
    <div
        class="fixed inset-0 bg-grid-pattern text-gray-400 dark:text-gray-500 pointer-events-none opacity-[0.07]"
    ></div>
    <URLSync />
    {@render children()}
    <ScrollToTop />
    <Footer />
</div>
