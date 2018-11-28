import tcod as libtcod

from entity import Entity
from components.item import Item
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from item_functions import paralyse
artifact_1_component = Item(use_function=paralyse,mana_cost=15)
equippable_component = Equippable(EquipmentSlots.MAIN_HAND, defense_bonus=4, agility_bonus =-3)
honey_blade = Entity(0,0,'/',libtcod.yellow,'Honey Blade',item=artifact_1_component,equippable=equippable_component)