import { env } from "$env/dynamic/public";

function publicBaseUrl(): string {
	return env.PUBLIC_UCIEL_API ?? "http://localhost:8000";
}

// ?v=1 busts Cloudflare cache (old 10MB responses).
// Remove once cache expires.
const CACHE_BUST = "?v=1";

export function resolvePosterUrl(path: string | null): string | null {
	if (!path) return null;
	if (path.startsWith("http")) return path + CACHE_BUST;
	return `${publicBaseUrl()}${path}${CACHE_BUST}`;
}
