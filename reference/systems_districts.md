# District System

| Key | Name | Qualifying tags | Min buildings | Radius | Bonuses | Penalties | Notable adjacency pairs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| district.industrial | Industrial District | metallurgy, craft, maintenance | 4 | 3 | em+0.10_per_building_cap0.30; fuel_upkeep-0.10_at3; r+0.05_at5 | housing_desire-; fire_risk+0.10_if_no_fire_service | adjacency:sanitation+water boosts r; housing adjacency adds unrest |
| district.agriculture | Agriculture District | farming, husbandry, food | 4 | 3 | bo+0.05_per_building_cap0.20; r+0.03_with_water; cap+50_on_storage | attracts_pests+; drought_risk_if_no_irrigation | adjacency:storage boosts cap; sanitation adjacency reduces disease |
| district.artisan | Artisan District | craft, jewelry, arcana | 3 | 2 | qt+1_at3; em+0.05_per_building_cap0.15 | fire_risk+0.05_if_no_safety; upkeep+0.05 | adjacency:civic reduces unrest; arcane adjacency improves qt |
| district.maritime | Maritime District | maritime | 3 | 3 | em+0.10_with_dock; cap+100_on_storage; r+0.05_if_lighthouse | storm_loss+0.05_if_no_lighthouse; upkeep+0.05 | adjacency:warehouse+dock improves logistics; shipyard+harbor boosts craft |
| district.arcane | Arcane District | arcana, arcane_focus | 2 | 2 | qt+1_at2; r+0.05_with_maintenance | surge_risk+0.05; labor_strain+ | adjacency:sanitation mitigates flux; civic adjacency eases permits |
| district.civic | Civic District | civic, safety, maintenance | 3 | 2 | r+0.05; event_mitigation+; labor_pool+ | upkeep+0.05; bo-0.05_on_noise_sensitive | adjacency:residential morale+; industrial adjacency unrest+ |
| district.residential | Residential District | housing | 4 | 2 | morale+; labor_pool+0.05; pop_density+ | fire_risk+0.05_if_no_safety; disease_risk+ if no sanitation | adjacency:civic boosts safety; agriculture adjacency boosts food access |
