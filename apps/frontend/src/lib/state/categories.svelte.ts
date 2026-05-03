import type { Category } from "$lib/types";

class CategoriesStore {
	#list = $state<Category[]>([]);
	#activeCategory = $state<string | null>(null);

	get list(): Category[] {
		return this.#list;
	}
	get activeCategory(): string | null {
		return this.#activeCategory;
	}

	initialize(list: Category[]): void {
		this.#list = list;
	}

	setActiveCategory(name: string | null): void {
		this.#activeCategory = name;
	}
}

export const categories = new CategoriesStore();
