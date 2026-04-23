import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import Inspector from "vite-plugin-inspector";

const inspectorEnabled = !!process.env.VITE_INSPECTOR;

export default defineConfig({
	plugins: [sveltekit(), tailwindcss(), inspectorEnabled && Inspector()],
});
