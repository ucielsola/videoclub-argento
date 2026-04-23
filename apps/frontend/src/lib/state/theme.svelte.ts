type Theme = 'light' | 'dark';

const STORAGE_KEY = 'theme';

function getInitialTheme(): Theme {
	if (typeof window === 'undefined') return 'light';
	const stored = localStorage.getItem(STORAGE_KEY);
	if (stored === 'light' || stored === 'dark') return stored;
	return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme(theme: Theme) {
	const root = document.documentElement;
	if (theme === 'dark') {
		root.classList.add('dark');
	} else {
		root.classList.remove('dark');
	}
}

class ThemeStore {
	#theme = $state<Theme>('light');
	#initialized = $state(false);

	constructor() {
		if (typeof window !== 'undefined') {
			this.#theme = getInitialTheme();
			applyTheme(this.#theme);
			this.#initialized = true;

			window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
				if (!localStorage.getItem(STORAGE_KEY)) {
					this.#theme = e.matches ? 'dark' : 'light';
					applyTheme(this.#theme);
				}
			});
		}
	}

	get theme(): Theme {
		return this.#theme;
	}

	get initialized(): boolean {
		return this.#initialized;
	}

	get isDark(): boolean {
		return this.#theme === 'dark';
	}

	toggle() {
		this.#theme = this.#theme === 'dark' ? 'light' : 'dark';
		localStorage.setItem(STORAGE_KEY, this.#theme);
		applyTheme(this.#theme);
	}

	set(theme: Theme) {
		this.#theme = theme;
		localStorage.setItem(STORAGE_KEY, this.#theme);
		applyTheme(this.#theme);
	}
}

export const theme = new ThemeStore();
