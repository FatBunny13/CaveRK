import tcod as libtcod
from random import randint

from components.ai import BasicMonster
from entity import Entity
from fighter import Fighter
from render_functions import RenderOrder

duchess_component = Fighter(hp=80, defense=20, power=5, xp=500, agility=5, mana=0, base_psyche=0,
                                        attack_dice_minimum=4, attack_dice_maximum=8, ac=5, will=4,is_peaceful=True,talk_message= 'I can\'t believe you made it out! Come quick I need your help!')
ai_component = BasicMonster()

leader = Entity(10, 5, '@', libtcod.hot_pink, 'The Duchess', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=duchess_component, ai=ai_component)

bandit_component = Fighter(hp=10, power=5,defense=0, xp=10, agility=5, mana=0, base_psyche=0,
                                        attack_dice_minimum=4, attack_dice_maximum=8, ac=1, will=0,talk_message='Yer money or yer life!')
ai_component = BasicMonster()

bandit = Entity(11, 5, '@', libtcod.black, 'Bandit', blocks=True,
                            render_order=RenderOrder.ACTOR, fighter=bandit_component, ai=ai_component)

sprite_1_component = Fighter(hp=5, power=0,defense=0, xp=5, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=1, attack_dice_maximum=4, ac=3, will=-2,is_peaceful=True,talk_message= 'Uggggh! I\'m sooooo bored! And my friend! She\'s such a kill joy!',
                            talk_message_2='Like i\'m as bored as a dog who\'s owner isn\'t home', talk_message_3='Ugggggh. Maybe I should set something on fire! Thats fun!')

sprite_child_1 = Entity(randint(8,11), randint(4,6), 'f', libtcod.green, 'Rambunctious Sprite Child', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=sprite_1_component, ai=ai_component)
ai_component = BasicMonster()
sprite_2_component = Fighter(hp=5, power=0,defense=0, xp=5, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=0, attack_dice_maximum=1, ac=3, will=-2,is_peaceful=True,talk_message= 'Why is my friend so weird?',
                            talk_message_2='I\'m worried shes going to set something on fire again', talk_message_3='It\'s like she hates the very basics of law! *sigh*')
ai_component = BasicMonster()
sprite_child_2 = Entity(randint(6,10), randint(4,5), 'f', libtcod.green, 'Sprite Child', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=sprite_2_component, ai=ai_component)

dapper_trashling_1_component = Fighter(hp=5, power=0,defense=0, xp=5, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=0, attack_dice_maximum=2, ac=3, will=-2,is_peaceful=True,talk_message= 'Ah I see you\'r going for the dirt and grime look!',
                            talk_message_2='The blood and dirt looks simply marvelous!', talk_message_3='You might want to cover up those bite marks though...', talk_message_4='My sister likes more avant garde stuff. Ask her!')
ai_component = BasicMonster()
dapper_trashling = Entity(randint(30,31), randint(20,24), 'r', libtcod.purple, 'Dapper Trashling', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=dapper_trashling_1_component, ai=ai_component)

dapper_trashling_2_component = Fighter(hp=5, power=0,defense=0, xp=5, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=0, attack_dice_maximum=2, ac=3, will=-2,is_peaceful=True,talk_message= 'What by the great Fae are you wearing!',
                            talk_message_2='You look like you work in a slaughterhouse!', talk_message_3='Have you heard of a shower? A towel? SOAP!?! Oh great Fae...', talk_message_4='My brothers the only one who could like this wreck!')
ai_component = BasicMonster()
fancy_trashling = Entity(randint(30,31), randint(20,24), 'r', libtcod.purple, 'Fancy Trashling', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=dapper_trashling_2_component, ai=ai_component)

shy_giantess_component = Fighter(hp=60, power=0,defense=0, xp=200, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=6, attack_dice_maximum=8, ac=-5, will=3,is_peaceful=True,talk_message= 'Hmmm... Oh sorry what is it?',
                            talk_message_2='Sorry i\'m just working on some sewing?', talk_message_3='Well have a good day stranger.', talk_message_4='Ah god-fae. Sewing is so hard when you\'re so tall...')
ai_component = BasicMonster()
shy_giantess = Entity(randint(50,51), randint(21,22), 'G', libtcod.darkest_gray, 'Shy Giantesss', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=shy_giantess_component, ai=ai_component)

stressed_mother_component = Fighter(hp=10, power=0,defense=0, xp=50, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=2, attack_dice_maximum=3, ac=1, will=1,is_peaceful=True,talk_message= 'Hmmm... Oh thank the god-fae I have some peace!',
                            talk_message_2='I love being a mother. But it\'s so stressful!')
ai_component = BasicMonster()
stressed_mother = Entity(None,None, 't', libtcod.dark_red, 'Stressed Mother', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=stressed_mother_component, ai=ai_component)
old_farmer_component = Fighter(hp=10, power=0,defense=0, xp=50, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=2, attack_dice_maximum=3, ac=1, will=1,is_peaceful=True,talk_message= 'Ah a break from picking turnips and milking the cloudies!',
                            talk_message_2='Farming is a good life. But its very hard!')
ai_component = BasicMonster()
old_farmer = Entity(0,0, 't', libtcod.dark_green, 'Old Farmer', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=old_farmer_component, ai=ai_component)
