# Frontend Agent Guide

## 🎯 Purpose
A modern SvelteKit web interface for browsing and managing the movie collection.

## 🛠️ Tech Stack
- **Svelte 5**: Uses Runes (`$state`, `$derived`) and Snippets.
- **Tailwind CSS v4**: High-performance styling via the Vite plugin.
- **Flowbite Svelte v2**: UI component library built for Svelte 5.

## 🧩 Key Logic
- `src/routes/+page.ts`: Fetches movie data from the backend during SSR.
- `src/routes/+page.svelte`: Displays the movie grid and handles the "Sync" action.
- `src/app.css`: Central Tailwind v4 configuration.

## 🚀 How to Run
```bash
npm run dev
```
