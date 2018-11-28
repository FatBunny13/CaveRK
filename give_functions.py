import tcod as libtcod

from game_messages import Message

def give_item_to_enemy(item,**kwargs):
    player = kwargs.get('player')
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    maximum_range = 1

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.distance(target_x, target_y) <= maximum_range and entity.fighter:
            for entity in entities:
                if entity.x == target_x and entity.y == target_y and entity != player:
                    print(item)
                    player.inventory.add_item(item)
                    player.inventory.remove_item(item)
                    entity.inventory.add_item(item)
                    break


    return results