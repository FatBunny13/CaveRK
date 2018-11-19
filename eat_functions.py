import tcod as libtcod
import random

from game_messages import Message

def eat(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')
    eat_message = kwargs.get('eat_message')
    results = []

    if entity.fighter.nutrition > 999:
        entity.fighter.nutrition -= 850
        results.append({'consumed': False, 'message': Message('You are so full you vomit!', libtcod.yellow)})
    else:
        entity.fighter.eat(amount)
        results.append({'consumed': True, 'message': Message(eat_message, libtcod.green)})

    return results

def eat_poison(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')
    eat_message = kwargs.get('eat_message')
    results = []

    if entity.fighter.nutrition > 999:
        entity.fighter.nutrition -= 850
        results.append({'consumed': False, 'message': Message('You are so full you vomit!', libtcod.yellow)})
    else:
        entity.fighter.eat(amount)
        entity.fighter.poisoned = 1
        entity.fighter.poison_timer = randint(10,30)
        results.append({'consumed': True, 'message': Message(eat_message, libtcod.green)})

    return results

def eat_cursed(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')
    eat_message = kwargs.get('eat_message')

    results = []

    if entity.fighter.nutrition > 999:
        entity.fighter.nutrition -= 850
        results.append({'consumed': False, 'message': Message('You are so full you vomit!', libtcod.yellow)})
    else:
        entity.fighter.eat(amount)
        entity.fighter.doomed = 1
        results.append({'consumed': True, 'message': Message(eat_message, libtcod.green)})

    return results