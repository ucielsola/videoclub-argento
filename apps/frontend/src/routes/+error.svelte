<script lang="ts">
import { page } from "$app/state";

let status = $derived(page.status);
let message = $derived(page.error?.message ?? "Error desconocido");
</script>

<svelte:head>
	<title>{status} - Video Club Argento</title>
</svelte:head>

<div class="flex flex-col items-center justify-center min-h-[60vh] gap-4">
	<h1 class="text-6xl font-bold text-gray-300 dark:text-gray-600">{status}</h1>
	<p class="text-lg text-gray-600 dark:text-gray-400">{message}</p>
	<a href="/" class="text-indigo-500 hover:underline">Volver al inicio</a>
</div>
