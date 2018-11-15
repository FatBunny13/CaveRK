import tcod as libtcod

class GameVariables:
    def __init__(self,killed_trash_king=False,bees_nest_spawned=False):
        self.killed_trash_king = killed_trash_king
        self.bees_nest_spawned = bees_nest_spawned