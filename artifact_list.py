import tcod as libtcod

from entity import Entity
from components.item import Item
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from item_functions import paralyse, cast_fireball
from game_messages import Message
artifact_1_component = Item(use_function=paralyse,mana_cost=15,targeting=True, targeting_message=Message(
                        'Left-click a target tile for paralysing, or right-click to cancel.', libtcod.light_cyan))
equippable_component = Equippable(EquipmentSlots.MAIN_HAND, minimum_hit_dice=2,maximum_hit_dice=8)
honey_blade = Entity(0,0,'/',libtcod.yellow,'Honey Blade',item=artifact_1_component,equippable=equippable_component)

artifact_2_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
    'Left-click a target tile for the ball of honey, or right-click to cancel.', libtcod.light_cyan),
                      damage=25, radius=5)
equippable_2_component = Equippable(EquipmentSlots.MAIN_HAND, ac_bonus=6, will_bonus= -5)
honey_shield = Entity(0,0,'}'.libtcod.yellow,'Honey Shield',item=artifact_2_component,equippable=equippable_2_component)