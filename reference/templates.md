# Templates and ID conventions

## ID prefixes
- `BIO-###` — Biomes, habitats, and landmass types
- `FAU-###` — Fauna/monsters
- `FLR-###` — Flora/fungi
- `MAT-###` — Raw/refined materials
- `EQP-###` — Equipment (weapons, armor, accessories, consumables)
- `CRF-###` — Crafting recipes
- `TEC-###` — Technologies
- `STR-###` — Structures (buildings, furniture, tools)
- `SPL-###` — Spells
- `PPF-###` — Player profiles
- `STP-###` — Settlement profiles
- `INV-###` — Inventories

## General entry template (markdown table row)
| ID | Name | Type/Category | Description | Key stats/qualities | Sources | Used in |
| --- | --- | --- | --- | --- | --- | --- |

## Spawn template (fauna)
| ID | Name | Appearance | Difficulty | Skills | Abilities | Spawn (location/habitat/time/weather) | Trigger | Loot (IDs) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Flora template
| ID | Name | Appearance | Habitat/time | Harvest method | Yield (IDs) | Uses (IDs) | Hazards/notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Material template
| ID | Name | Type | Source (IDs/biome) | Refinement | Uses (IDs) | Unlocked by (TEC) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Biome/habitat template
| ID | Name | Category | Landmass type | Climate/Environment | Notable features | Native flora/fauna/material IDs | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Equipment template
| ID | Name | Slot | Quality | Effects | Coverage/Restrictions | Weight | Components (IDs) | Unlocked by (TEC) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Crafting recipe template
| ID | Name | Products (IDs) | Ingredients (IDs & qty) | Tools (IDs) | Structures (IDs) | Time | Unlocked by (TEC) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Technology template
| ID | Name | Tier | Prerequisites (IDs) | Unlocks (IDs) | Time/Cost | Notes |
| --- | --- | --- | --- | --- | --- | --- |

## Structure template
| ID | Name | Type | Purpose | Requirements (IDs) | Enabled actions (IDs) | Required tech (TEC) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Spell template
| ID | Name | Element | School | Effect | Components/Focus (IDs) | Tier/Level | Unlocked by (TEC) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Profile template
| ID | Name | Type | Traits | Skills/Stats | Affiliation/Origin | Notes |
| --- | --- | --- | --- | --- | --- | --- |

## Inventory template
| ID | Owner (PPF/STP) | Items (IDs & qty) | Capacity | Notes |
| --- | --- | --- | --- | --- |
