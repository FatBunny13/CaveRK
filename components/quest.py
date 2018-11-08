import libtcodpy as libtcod

from game_messages import Message

class Quest:
    def __init__(self, completed=False):
        self.completed = completed