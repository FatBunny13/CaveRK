import libtcodpy as libtcod

from game_messages import Message

class Quest:
    def __init__(self,has_quest = False, completed=False):
        self.has_quest = has_quest
        self.completed = completed