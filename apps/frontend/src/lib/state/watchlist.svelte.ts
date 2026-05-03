type WatchStatus = "quiero-ver" | "ya-la-vi" | null;

const STORAGE_KEY = "videoclub-watchlist";

function getInitialWatchlist(): Record<string, WatchStatus> {
	if (typeof window === "undefined") return {};
	try {
		const stored = localStorage.getItem(STORAGE_KEY);
		return stored ? JSON.parse(stored) : {};
	} catch {
		return {};
	}
}

class WatchlistStore {
	#watchlist = $state<Record<string, WatchStatus>>(getInitialWatchlist());

	getStatus(slug: string): WatchStatus {
		return this.#watchlist[slug] ?? null;
	}

	toggleQuieroVer(slug: string) {
		const current = this.#watchlist[slug];
		this.#watchlist[slug] = current === "quiero-ver" ? null : "quiero-ver";
		this.#persist();
	}

	toggleYaLaVi(slug: string) {
		const current = this.#watchlist[slug];
		this.#watchlist[slug] = current === "ya-la-vi" ? null : "ya-la-vi";
		this.#persist();
	}

	get quieroVerList(): string[] {
		return Object.entries(this.#watchlist)
			.filter(([, status]) => status === "quiero-ver")
			.map(([slug]) => slug);
	}

	get yaLaViList(): string[] {
		return Object.entries(this.#watchlist)
			.filter(([, status]) => status === "ya-la-vi")
			.map(([slug]) => slug);
	}

	#persist() {
		if (typeof window !== "undefined") {
			localStorage.setItem(STORAGE_KEY, JSON.stringify(this.#watchlist));
		}
	}
}

export const watchlist = new WatchlistStore();
