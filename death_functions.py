import libtcodpy as libtcod

from game_messages import Message

from game_states import GameStates

from render_functions import RenderOrder
from quest_list import trash_king_quest



def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red
    game_state = GameStates.PLAYER_DEAD

    return Message('You died!', libtcod.red),game_state


def kill_monster(monster,player,entities):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), libtcod.orange)
    if monster.fighter.boss == 2:
        player.game_variables.killed_trash_king = True
    if monster.inventory:
        for item in monster.inventory.items:
                monster.inventory.remove_item(item)
                entities.append(item)
                item.x = monster.x
                item.y = monster.y
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
