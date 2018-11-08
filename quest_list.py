import tcod as libtcod

from entity import QuestEntity
from components.quest import Quest

from game_messages import Message


starting_quest_component = Quest(completed=False)
starting_quest = QuestEntity('Get back to Havoc', quest=starting_quest_component)