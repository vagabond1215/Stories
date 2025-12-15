# District systems

| Key | Name | Qualifying tags | Min buildings | Radius | Bonuses | Penalties | Notable adjacency pairs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| district.industrial | Industrial Yard | metallurgy, craft | 3 | 3 | em+0.10_per_building_cap0.30; r+0.05_with_fire_watch; labor_pool+1_at5 | housing_desirability-; fire_risk+ | industrial+residential=desirability_drop; industrial+arcane=unsteady_mana |
| district.agriculture | Agrarian Fields | farming | 3 | 4 | bo+0.08_per_building_cap0.24; r+0.03_with_drainage | pest_weight+; fire_risk+in_drought | agriculture+residential=food_security_up; agriculture+maritime=fishery_boost |
| district.artisan | Artisan Quarter | craft, textile | 3 | 2 | em+0.08_per_building_cap0.24; qt+1_when_guildhall_present | housing_desirability- | artisan+residential=comfort_up; artisan+industrial=throughput_up |
| district.maritime | Maritime Front | maritime, logistics | 3 | 3 | em+0.12_with_STR-145_plus; cap+10_per_storage | storm_risk+; upkeep+0.10 | maritime+industrial=shipwright_speed; maritime+civic=tariff_bonus |
| district.arcane | Arcane Enclave | arcana | 2 | 2 | qt+1_all; r+0.05_if_grounded | upkeep+0.15; event_weight+ | arcane+residential=mana_comfort; arcane+industrial=wild_flux |
| district.civic | Civic Core | civic | 3 | 2 | r+0.08_with_fire_service; event_recovery-0.10 | upkeep+0.05 | civic+residential=order_bonus; civic+industrial=tax_resistance |
| district.residential | Residential Block | housing | 3 | 2 | morale+; r+0.03_with_sanitation | labor_pool-when_overcrowded | residential+agriculture=food_rations; residential+artisan=amenity_bonus |
| district.military | Garrison Grounds | military, civic | 2 | 2 | patrol_risk-0.10; em+0.05_for_weaponsmiths | morale-when_unfed; upkeep+0.10 | military+industrial=armament_flow; military+residential=desirability_drop |
