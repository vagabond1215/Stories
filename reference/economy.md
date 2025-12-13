# Economy, Coinage, and Pricing Model

## Baseline value
- **Standard Value Unit (SVU)**: 1 copper coin (c) buys a filling meal or a simple tool handle. All prices below reference SVU.
- Everyday subsistence (food + shared bunk for one day) costs **5 SVU**; frugal weekly upkeep for a laborer is **30–40 SVU**.

## Coinage and exchange
- Coins scale by at least **10:1** in value; mint adjusts thickness to keep metal worth aligned with face value.
- Gemstones act as high-value notes; quality grades (flawed/fair/fine/excellent) double value per step.

| Coin | Metal | Value (SVU) | Exchange | Notes |
| --- | --- | --- | --- | --- |
| ci | Cold iron | 0.01 | 10 ci = 1 st | Smallest change; brittle washers for tolls |
| st | Steel | 0.1 | 10 st = 1 c | Durable trade coin for guild dues |
| c | Copper | 1 | 10 c = 1 s | Baseline coin; priced to metal weight |
| s | Silver | 10 | 10 s = 1 g | Common for craftsman pay |
| g | Gold | 100 | 10 g = 1 p | Stored wealth; often stamped by city seal |
| p | Platinum | 1,000 | 10 p = 1 small gemstone | Rare mint; braided rim to deter shaving |
| Gemstone chit | Ruby/sapphire/emerald/diamond | 10,000–80,000 (size/grade dependent) | 1 small gemstone = 10 p | Appraised and sealed in lacquer to prevent swaps |

## Pricing bands for goods
| Tier | Typical items | Base price (SVU) | Notes |
| --- | --- | --- | --- |
| Common raw | Firewood bundle, grain sack, rough ore | 5–20 | Matches daily wages for gatherers |
| Refined material | Ingots, treated planks, alchemical reagents | 30–120 | Includes smelting/treatment fuel |
| Finished mundane | Tools, simple weapons, travel clothes | 80–300 | Assumes journeyman labor and overhead |
| Fine crafted | Masterwork arms, fitted armor, enchanted focuses | 500–3,000 | Requires guild skill/rare inputs |
| Luxury/rare | Unique relics, noble commissions | 5,000+ | Price floats by patron prestige and scarcity |

## Wholesale vs. market vs. retail
- **Wholesale (gatherer → buyer)**: `Base Value × (0.35–0.55)` depending on freshness, bulk, and buyer leverage. Governments or guild contracts usually pay the higher end.
- **Market stall (self-sold)**: `Base Value × (0.8–1.1)`; adds time cost but captures most value.
- **Merchant retail (shop)**: `Base Value × (1.2–1.6)`; covers storage, risk, taxes, and credit terms.
- **Reasonable value check**: If sale price exceeds `Base Value × 2` without rarity justification, apply a scarcity note or lower markup to keep values believable.

### Profit calculations
- `Gross Profit = Sale Price – Cost of Goods (materials + wages + fees)`
- `Margin % = (Gross Profit ÷ Sale Price) × 100`
- **Example**: A gatherer sells herbs (Base 50 SVU) wholesale at 0.5× for **25 SVU**. An apothecary bottles tonics (Cost 25 + 20 labor = 45) and retails at 1.4× base (**70 SVU**). Profit = 25; Margin ≈ 35.7%.

## Wage and reward estimation
- **Base day wage (low risk, 8 hours)**: 5–8 SVU (subsistence); skilled artisan: 12–18 SVU; militia guard: 15–25 SVU.
- **Commission/contract formula**:
  - `Pay = BaseWage × TimeFactor × (1 + Difficulty + Risk + Scarcity + Urgency) + HazardBonus + UniqueReward`
  - **TimeFactor**: hours ÷ 8 (minimum 0.5 for short tasks).  
  - **Difficulty**: 0.1 (simple) to 0.6 (expert-only).  
  - **Risk**: 0 (safe) to 1.0 (life-threatening monster hunts).  
  - **Scarcity**: 0–0.4 based on rarity of target resource.  
  - **Urgency**: 0–0.3 for rush deliveries.  
  - **HazardBonus**: flat 5–50 SVU for injuries, hostile zones, or smuggling heat.  
  - **UniqueReward**: quantity of finished goods worth 10–30% of contract value (e.g., 2 tonics from an alchemist order).
- **Adventurer example**: Risk 0.8, Difficulty 0.5, 2-day hunt (TimeFactor 2). BaseWage 18 SVU ⇒ Pay ≈ 18 × 2 × (1 + 0.5 + 0.8) = 93.6 SVU plus HazardBonus/UniqueReward.

## Regional supply, demand, and trade flags
- **Supply score (0–5)**: 0 = scarce/absent, 3 = stable local production, 5 = glut/surplus.
- **Demand score (0–5)**: 0 = unwanted, 3 = routine need, 5 = acute shortage.
- **Import/Export flag**: `Export` if Supply − Demand ≥ 2; `Import` if Demand − Supply ≥ 2; otherwise `Local`.
- **Seasonal/events modifiers**: adjust Supply by −1 in harsh winters for forage; adjust Demand by +1–2 during festivals, wars, or plagues for relevant goods.

| Region | Goods focus | Supply | Demand | Flag | Seasonal/Event criteria |
| --- | --- | --- | --- | --- | --- |
| Marshport Delta | Salt fish, bog iron | Supply 4 (fish), 3 (iron) | Demand 2 (fish), 3 (iron) | Export fish; Local iron | Storm season −1 fish supply; war +1 iron demand |
| Highvale Hold | Wool, hardwood | Supply 3 (wool), 4 (wood) | Demand 4 (wool), 2 (wood) | Import wool; Export wood | Winter −1 wool supply; caravan fair +1 wool demand |
| Emberreach | Alchemical reagents, charcoal | Supply 5 (reagents), 2 (charcoal) | Demand 3 (reagents), 4 (charcoal) | Export reagents; Import charcoal | Eruption event +2 reagent demand; logging ban −1 charcoal supply |

## Usage guidelines
- Anchor all new item prices to the SVU baseline and pick a band from the pricing table.
- Choose markup tier based on who sells the good (gatherer, stall, or merchant) and whether scarcity/urgency applies.
- Apply the wage formula for contracts; add unique rewards when the commissioner can pay partly in product without destabilizing coin flow.
- When regions shift, update supply/demand scores and flip import/export flags to reflect shortages or surpluses.
