# Stories Reference Database

This repository hosts a modular fantasy RPG reference database designed for worldbuilding, gameplay planning, and future tooling such as search or indexing. Content lives in the [`reference/`](reference) directory and is organized by theme with stable IDs for cross-linking.

## Structure
- `reference/README.md` — Top-level index of the database files and guidance on cross-references.
- `reference/templates.md` — ID conventions and table templates for adding new data.
- Domain files: `fauna.md`, `flora.md`, `materials.md`, `equipment.md`, `crafting_recipes.md`, `technology.md`, `structures.md`, `spells.md`, `profiles.md`, `inventories.md`.

## Contribution workflow
1. Choose the appropriate domain file in `reference/` and follow the template headers.
2. Assign the next sequential ID with the correct prefix (e.g., `FAU-004`).
3. Cross-reference related entries (loot, ingredients, unlocks, owners, etc.).
4. Update related files if dependencies change (e.g., new material used in a recipe or spell focus).
5. Keep this README in sync when the file structure expands.

## Indexing/search readiness
- Tables use consistent columns for easier parsing by scripts.
- Stable IDs connect loot, materials, recipes, techs, structures, spells, and inventories.
- Each file is small and focused to keep searches fast while allowing future expansion.
