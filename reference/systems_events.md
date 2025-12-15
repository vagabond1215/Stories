# Events and Failures

| Key | Name | Category | Base chance | Triggers | Effects | Mitigation |
| --- | --- | --- | --- | --- | --- | --- |
| event.fire.workshop | Workshop Fire | disaster | 0.02 | tags=metallurgy_or_craft; heat_load>60; no=safety_watch | r-=0.20_for_3d; disable=str:nearest_workshop_2d | requires=safety (STR-164 or higher); water_access |
| event.fire.district | District Conflagration | disaster | 0.01 | district=industrial_or_residential; wind=high; no=fire_brigade | lose=cap:storage10%; r-=0.30_for_3d | mitigation=STR-166; stone_construction |
| event.breakdown.tools | Tool Breakdown | maintenance | 0.03 | tags=craft_or_metallurgy; no=maintenance | em-=0.10_for_2d; up+=1_for_2d | mitigation=STR-168; spare_parts |
| event.spoilage.pests | Pest Spoilage | economy | 0.025 | storage<r=0.9; grain_or_food>200 | lose=bo:0.10_for_2d; cap_loss=5% | mitigation=STR-127; sanitation |
| event.drought.crop | Crop Drought | environment | 0.015 | district=agriculture; no=irrigation | bo-=0.20_for_7d | mitigation=STR-102; waterworks |
| event.blight.crop | Crop Blight | environment | 0.010 | farming_density>5; no=crop_rotation | bo-=0.25_for_7d; qt-=1_for_7d | mitigation=STR-103; sanitation |
| event.livestock.disease | Livestock Disease | environment | 0.012 | tags=husbandry; shelter<2 | bo-=0.20_for_5d; r-=0.10_for_5d | mitigation=STR-114; STR-115 |
| event.sea.storm_loss | Storm Loss at Sea | disaster | 0.008 | district=maritime; storm=true; no=lighthouse | lose=bo:0.30_for_2d; cap_loss=10% | mitigation=STR-150; STR-177 |
| event.labor.strike | Labor Strike | social | 0.006 | morale<0.4; taxes=high; no=civic_presence | disable=district:affected_2d; bo-=0.10_for_3d | mitigation=STR-147; morale_programs |
| event.arcane.surge | Arcane Surge | arcane | 0.004 | district=arcane; arcane_load>50; no=grounding | r-=0.15_for_3d; qt+=1_for_2d | mitigation=tags=arcana+maintenance; STR-129 |
| event.positive.boom | Prosperity Boom | positive | 0.005 | stability>0.6; storage>500 | bo+=0.10_for_7d; labor_pool+0.05 | mitigation=None |
