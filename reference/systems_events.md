# Events and incidents

| Key | Name | Category | Base chance | Triggers | Effects | Mitigation |
| --- | --- | --- | --- | --- | --- | --- |
| event.fire.workshop | Workshop Fire | Hazard | 0.03 | tags=metallurgy; r<0.80; no_fire_service | disable=STR-130_2_cycles; r-=0.20_for_neighbors; lose_mat=MAT-041x6 | STR-164_present; water_source=near |
| event.spoilage.pests | Spoilage: Pests | Economy | 0.04 | storage_without_STR-127; tags=storage | lose_mat=grainx10; r-=0.10_for_storage; bo-=0.05_for_farms | STR-127_present; sanitation=active |
| event.sea.storm_loss | Storm Loss | Maritime | 0.02 | district=maritime; weather=storm | disable=STR-090_1_cycle; lose_inv=INV-002x4; r-=0.10_for_maritime | STR-150_present; raftering=checked |
| event.bounty.rich_harvest | Rich Harvest | Positive | 0.03 | district=agriculture_tier2; rotations_marked | bo+=0.15_for_farms_2_cycles; cap+=5_for_STR-121 | STR-103_present; pest_control=active |
| event.discovery.vein | Vein Discovery | Positive | 0.01 | tags=metallurgy; job=JOB-021_active | unlock_mat=MAT-095x12; r+=0.05_for_STR-025 | survey_maps_prepared |
| event.outbreak.sickness | Sickness Outbreak | Hazard | 0.025 | district=residential; sanitation<1 | labor_pool-=2_2_cycles; r-=0.10_for_housing; bo-=0.08_for_farms | STR-162_present; healer=JOB-009 |
