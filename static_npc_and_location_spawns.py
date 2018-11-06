import tcod as libtcod
from random import randint

from components.ai import BasicMonster, SleepMonster
from entity import Entity
from fighter import Fighter
from render_functions import RenderOrder

#These are the spawns for the Village of Havoc.
stressed_mother_component = Fighter(hp=10, power=0,defense=0, xp=50, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=2, attack_dice_maximum=3, ac=1, will=1,is_peaceful=True,talk_message= 'Hmmm... Oh thank the god-fae I have some peace!',
                            talk_message_2='I love being a mother. But it\'s so stressful!')
ai_component = BasicMonster()
stressed_mother = Entity(41,4, 't', libtcod.dark_red, 'Stressed Mother', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=stressed_mother_component, ai=ai_component)
old_farmer_component = Fighter(hp=10, power=0,defense=0, xp=50, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=2, attack_dice_maximum=3, ac=1, will=1,is_peaceful=True,talk_message= 'Ah a break from picking turnips and milking the cloudies!',
                            talk_message_2='Farming is a good life. But its very hard!')
ai_component = BasicMonster()
old_farmer = Entity(40,4, 't', libtcod.dark_green, 'Old Farmer', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=old_farmer_component, ai=ai_component)

old_farmer_component = Fighter(hp=10, power=0,defense=0, xp=50, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=2, attack_dice_maximum=3, ac=1, will=1,is_peaceful=True,talk_message= 'Ah a break from picking turnips and milking the cloudies!',
                            talk_message_2='Farming is a good life. But its very hard!')
ai_component = BasicMonster()
old_farmer_2 = Entity(41,4, 't', libtcod.dark_green, 'Old Farmer', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=old_farmer_component, ai=ai_component)
stressed_mother_component = Fighter(hp=10, power=0, defense=0, xp=50, agility=1, mana=0, base_psyche=0,
                                    attack_dice_minimum=2, attack_dice_maximum=3, ac=1, will=1, is_peaceful=True,
                                    talk_message='Hmmm... Oh thank the god-fae I have some peace!',
                                    talk_message_2='I love being a mother. But it\'s so stressful!')
ai_component = BasicMonster()
stressed_mother_2 = Entity(41, 5, 't', libtcod.dark_red, 'Stressed Mother', blocks=True,fighter=stressed_mother_component,ai=ai_component)

horned_cloudie_component = Fighter(hp=10, power=0, defense=0, xp=50, agility=1, mana=0, base_psyche=0,
                                    attack_dice_minimum=2, attack_dice_maximum=3, ac=1, will=1, is_peaceful=True,
                                    talk_message='Moo!')
sleep_component = SleepMonster()
horned_cloudie = Entity(65, 15, 's', libtcod.lightest_blue, 'Horned Cloudie', blocks=True,fighter=horned_cloudie_component,ai=sleep_component)

horned_cloudie_component = Fighter(hp=10, power=0, defense=0, xp=50, agility=1, mana=0, base_psyche=0,
                                    attack_dice_minimum=2, attack_dice_maximum=3, ac=1, will=1, is_peaceful=True,
                                    talk_message='Moo!')
sleep_component = SleepMonster()
horned_cloudie_2 = Entity(65, 16, 's', libtcod.lightest_blue, 'Horned Cloudie', blocks=True,fighter=horned_cloudie_component,ai=sleep_component)

horned_cloudie_component = Fighter(hp=10, power=0, defense=0, xp=50, agility=1, mana=0, base_psyche=0,
                                    attack_dice_minimum=2, attack_dice_maximum=3, ac=1, will=1, is_peaceful=True,
                                    talk_message='Moo!')
sleep_component = SleepMonster()
horned_cloudie_3 = Entity(64, 15, 's', libtcod.lightest_blue, 'Horned Cloudie', blocks=True,fighter=horned_cloudie_component,ai=sleep_component)

#End of Village Spawns