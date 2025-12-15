# Fantasy RPG Reference Database

This directory contains a modular, cross-referenced knowledge base for a fantasy RPG world. Each file focuses on one domain while sharing common identifiers to maintain consistency and support future indexing/searching.

## File map
- [templates.md](templates.md) — Shared ID scheme and data entry templates.
- [economy.md](economy.md) — Coinage, pricing bands, wages, and regional supply/demand flags.
- [biomes.md](biomes.md) — Biomes, habitats, and landmass types with linked flora/fauna/material IDs.
- [fauna.md](fauna.md) — Bestiary entries with spawn, abilities, and loot.
- [flora.md](flora.md) — Plants, fungi, and harvest details.
- [materials.md](materials.md) — Mined/harvested resources and refined materials.
- [equipment.md](equipment.md) — Weapons, armor, accessories, consumables.
- [crafting_recipes.md](crafting_recipes.md) — Recipes linking ingredients, tools, and structures.
- [technology.md](technology.md) — Technology tree with unlocks and prerequisites.
- [structures.md](structures.md) — Buildings, furniture, and tools tied to technologies. Now includes `Stats` and `Upgrade path` columns for balancing and modules.
- [spells.md](spells.md) — Spell list with elements and schools.
- [profiles.md](profiles.md) — Player and settlement profiles.
- [inventories.md](inventories.md) — Current inventories referencing profiles and items.
- [systems_calendar.md](systems_calendar.md) — Calendar and spoilage rules (13 months, 28 days each; 1-day cycles).
- [systems_districts.md](systems_districts.md) — District adjacency logic and bonuses.
- [systems_events.md](systems_events.md) — Event triggers, effects, and mitigations.
- [systems_difficulty.md](systems_difficulty.md) — Difficulty presets and global rule toggles.

## Table conventions
- Structures, equipment, spells, and materials now include a `Required tech (TEC)` or `Unlocked by (TEC)` column to standardize tech gating. Use comma-separated TEC IDs or `None` for ungated entries.
- Technology unlock lists should mirror these columns when a tech directly enables a recipe, structure, or item.
- Keep existing column ordering; add new data by filling cells rather than rearranging headers.

### Upgrades/Modules
- Renovations and modules are encoded as `Type: Upgrade/Module` rows in `structures.md` and are linked to base structures through the `Upgrade path` column.
- The `Stats` field uses compact key/value pairs (`bo`, `l`, `em`, `r`, `qt`, `cap`, `up`, optional `pop` and `tags`) with semicolon separation. Modules use `+` values to indicate deltas. Residential entries use `pop` instead of `bo`.

### Districts
- `systems_districts.md` defines district tags, radii, bonuses, and adjacency notes with parseable columns.

### Events
- `systems_events.md` lists cycle-based events with triggers, effects, and mitigations for simulation tuning.

### Difficulty
- `systems_difficulty.md` captures presets and global rules such as diminishing returns and storage caps.

### Calendar and pacing
- The system uses 13 months of 28 days (364-day year) with a 1-day cycle. Spoilage defaults are recorded in `systems_calendar.md` for perishables and grain.

### Exports & Validation
- Regenerate JSON exports from markdown tables:
  - `python tools/build_exports.py`
- Validate cross-references, cycles, and schema compliance:
  - `python tools/validate_reference_db.py`

## Indexing/search guidance
- Unique IDs (e.g., `FAU-001`, `EQP-003`) are stable across files for cross-linking.
- Tables use consistent column headers to simplify parsing.
- Use the templates to add new entries and keep references synchronized across files.
- When adding new IDs, also update related recipes, technologies, and inventories to preserve traceability.

## Adding or updating technologies
- Insert new technology rows at the end of `reference/technology.md`, following the existing tier notation (`Tier 1`, `Tier 2`, etc.).
- Align unlocks with other tables: if a tech unlocks a recipe, structure, or item, ensure the corresponding table’s `Unlocked by (TEC)`/`Required tech (TEC)` cell lists that TEC.
- Avoid cycles by keeping prerequisite chains acyclic and using existing TEC IDs where possible.

## Validation and graph export
- Validate cross-references and ID formats:
  - `python tools/validate_reference_db.py`
- Regenerate the deterministic tech graph export for tooling/UI:
  - `python tools/build_tech_graph.py`
