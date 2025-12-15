# Tag taxonomy

A lightweight tag layer lets you filter TEC/STR/CRF/EQP/SPL/MAT/JOB entries by themes rather than only by IDs. Tags are short, lowercase slugs; apply two to four per entry to capture the main fantasy/industrial vibes without overfitting.

## Core tag families
- **metallurgy** — smelting, forging, alloys, anvils, metalworking tools.
- **ceramics** — clay, kilns, pottery, bricks, glazing, refractory goods.
- **textiles** — fibers, spinning, weaving, dyeing, tailoring equipment.
- **leather** — hides, tanning, curing, leatherworking benches.
- **agriculture** — crops, irrigation, plowing, harvest/storage of foodstuffs.
- **logistics** — transport, storage, pack animals, carts, warehousing, supply chains.
- **arcana** — magical theory, runes, enchanting, mana conduits, spellcraft scaffolding.
- **siege** — fortifications, siege engines, battlements, breaching/defense tools.
- **governance** — civic administration, taxation, law, diplomacy, bureaucracy.

Use additional contextual tags sparingly (e.g., `navigation`, `medicine`, `guilds`, `festival`) when a concept is central to the entry.

## Tagging guidelines by record type

### Technology (TEC)
- Capture the discipline driving the unlock (e.g., `metallurgy`, `arcana`).
- Add operational focus if it changes logistics or administration (e.g., `logistics`, `governance`).
- Avoid tagging every downstream application; stick to what the research *teaches*.

### Structures (STR)
- Tag by primary function and material workflow (`ceramics` for kilns, `metallurgy` for forges).
- Include `logistics` for storage/transport hubs and `siege` for defensive works.
- If the building channels magical effects, append `arcana`.

### Crafting recipes (CRF)
- Match tags to the dominant production method (`textiles` for cloth bolts, `leather` for cured hide).
- Add resource-intensive supports like `logistics` when recipes rely on distribution chains.
- Do not inherit every tag from ingredients—focus on the crafting station and method.

### Equipment (EQP)
- Tag by construction method and combat/utility role (`metallurgy` for plate, `textiles` for robes).
- Use `arcana` for enchanted items; pair with material tags to show hybrid designs.
- For siege gear or fortification add-ons, include `siege`.

### Spells (SPL)
- Always include `arcana`; add thematic context (`logistics` for teleport beacons, `governance` for oathbinding).
- For spells enhancing crafts, mirror the relevant trade tag (`textiles` for loom-speed charms).

### Materials (MAT)
- Tag by processing lineage (`ceramics` for clay, `metallurgy` for ore/ingots, `textiles` for fibers, `leather` for hides).
- Add `agriculture` for farmed inputs and `logistics` for packaged goods (barrels, crates).

### Jobs (JOB)
- Tag by trade focus (`metallurgy` for smiths, `ceramics` for potters, `governance` for clerks/officers).
- Use secondary tags to show workplace context (`siege` engineers, `arcana` scholars, `logistics` quartermasters).

## Application tips
- Keep tags consistent across the same workflow so filters surface coherent chains (e.g., TEC `Bloomery Smelting` → STR `Bloomery` → CRF `Wrought Iron Bars` all use `metallurgy`).
- Prefer specificity over volume: two strong tags beat five weak ones.
- When in doubt, pick the tag that signals how a player *interacts* with the entry (builds, studies, fights, trades) to reinforce immersion during filtering.
