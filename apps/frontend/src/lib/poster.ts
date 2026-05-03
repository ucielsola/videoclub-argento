import { env } from "$env/dynamic/public";

function publicBaseUrl(): string {
	return env.PUBLIC_UCIEL_API ?? "http://localhost:8000";
}

export function resolvePosterUrl(path: string | null): string | null {
	if (!path) return null;
	if (path.startsWith("http")) return path;
	return `${publicBaseUrl()}${path}`;
}
