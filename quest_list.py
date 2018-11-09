import tcod as libtcod

from entity import QuestEntity
from components.quest import Quest

from game_messages import Message


starting_quest_component = Quest(has_quest=True,completed=False)
starting_quest = QuestEntity('Get back to Havoc', quest=starting_quest_component)

trash_king_quest_component = Quest(has_quest=False,completed=False)
trash_king_quest = QuestEntity('Kill the Trash-King', quest=trash_king_quest_component)