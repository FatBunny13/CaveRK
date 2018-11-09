import tcod as libtcod

from game_messages import Message

def talk_to_enemy(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.fighter:
            results.append({'message': Message(entity.fighter.talk_message, libtcod.lighter_blue)})
            results.append({'message': Message(entity.fighter.talk_message_2, libtcod.lighter_blue)})
            results.append({'message': Message(entity.fighter.talk_message_3, libtcod.lighter_blue)})
            results.append({'message': Message(entity.fighter.talk_message_4, libtcod.lighter_blue)})

    return results