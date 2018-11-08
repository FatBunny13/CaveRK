import tcod as libtcod

from components.ai import BasicMonster
from entity import Entity
from fighter import Fighter
from render_functions import RenderOrder

fighter_component = Fighter(hp=80, defense=20, power=5, xp=500, agility=5, mana=0, base_psyche=0,
                                        attack_dice_minimum=4, attack_dice_maximum=8, ac=5, will=4,is_peaceful=True,talk_message= 'Oh my god you\'re alive!')
ai_component = BasicMonster()

leader = Entity(10, 5, '@', libtcod.hot_pink, 'The Duchess', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

fighter_component = Fighter(hp=10, power=5,defense=0, xp=10, agility=5, mana=0, base_psyche=0,
                                        attack_dice_minimum=4, attack_dice_maximum=8, ac=1, will=0,talk_message='Yeee')
ai_component = BasicMonster()

bandit = Entity(11, 5, '@', libtcod.black, 'Bandit', blocks=True,
                            render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)