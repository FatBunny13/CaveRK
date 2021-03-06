import libtcodpy as libtcod


from components.ai import ConfusedMonster,CharmedMonster


from game_messages import Message
from random import randint
from entity_list import buzzing_tile
from entity import Entity
from components.stairs import Stairs
from render_functions import RenderOrder

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

def special_powder(*args,**kwargs):
    entity = args[0]

    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    constants = kwargs.get('constants')
    message_log = kwargs.get('message_log')


    results = []

    for tile in entities:
        if buzzing_tile.x == entity.x and buzzing_tile.y == entity.y:
            results.append({'consumed': False, 'message': Message('Suddenly the buzzing hole opens! You see some solid beeswax stairs leading down.', libtcod.red)})
            entity.game_variables.bees_nest_spawned = True
            bees_component = Stairs(game_map.dungeon_level - 1, bees_stairs=True)
            bees_stairs = Entity(3, 4, '>', libtcod.yellow, 'Stairs to the Bees-Nest',
                                 render_order=RenderOrder.STAIRS, stairs=bees_component)
            entities.append(bees_stairs)
            entities.remove(buzzing_tile)
            break
        elif buzzing_tile.x != entity.x and buzzing_tile.y != entity.y:
            results.append({'consumed': False,
                            'message': Message('You sprinkle the powder. It smells sweet.',
                                               libtcod.pink)})
            break

    return results



def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})

    return results

def cast_bless(*args,**kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    target = None
    mana_cost = kwargs.get('mana_cost')

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append(
            {'used': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y:
            caster.fighter.take_mana_damage(mana_cost)
            entity.fighter.blessed = 1
            entity.fighter.blessed_timer += 10
            entity.fighter.bless_bonus += 1

            entity.owner = entity

            results.append({'used': True, 'message': Message(
                'The {0} is bathed in a bright light!'.format(entity.name),
                libtcod.light_green)})

            break
    else:
        results.append(
            {'used': False, 'message': Message('There is nothing targetable at that location.', libtcod.yellow)})

    return results

def cast_doom(*args,**kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    target = None
    mana_cost = kwargs.get('mana_cost')

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append(
            {'used': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y:
            caster.fighter.take_mana_damage(mana_cost)
            entity.fighter.doomed = 2

            entity.owner = entity

            results.append({'used': True, 'message': Message(
                'The {0} is bathed in a dark and gloomy shadow!'.format(entity.name),
                libtcod.red)})

            break
    else:
        results.append(
            {'used': False, 'message': Message('There is nothing targetable at that location.', libtcod.yellow)})

    return results

def paralyse(*args,**kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    target = None
    mana_cost = kwargs.get('mana_cost')

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append(
            {'used': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y:
            caster.fighter.take_mana_damage(mana_cost)
            entity.fighter.paralysis = 1
            entity.fighter.paralysis_time = 30

            entity.owner = entity

            results.append({'used': True, 'message': Message(
                'The {0}\'s muscles suddenly lock up!'.format(entity.name),
                libtcod.red)})

            break
    else:
        results.append(
            {'used': False, 'message': Message('There is nothing targetable at that location.', libtcod.yellow)})

    return results


def hide(*args,**kwargs):
    caster = args[0]
    results = []

    if caster.fighter.stealthed == 1:
        results.append({'stealthed': False, 'message': Message('You are already hidden!', libtcod.yellow)})

    else:
        caster.fighter.stealthed += 1
        results.append({'stealthed': True, 'message': Message('You hide in the shadows!', libtcod.yellow)})

    return results

def riposte(*args,**kwargs):
    caster = args[0]
    results = []

    if caster.fighter.riposte == 1:
        results.append({'stealthed': False, 'message': Message('You can already riposte!', libtcod.yellow)})

    else:
        caster.fighter.riposte += 1
        caster.fighter.riposte_time = randint(10,20)
        results.append({'stealthed': True, 'message': Message('You suddenly feel graceful!', libtcod.yellow)})

    return results

def become_clairvoyant(*args,**kwargs):
    caster = args[0]
    results = []

    if caster.fighter.clairvoyance is True:
        results.append({'stealthed': False, 'message': Message('You are already clairvoyant!', libtcod.yellow)})

    else:
        caster.fighter.clairvoyance = True
        results.append({'stealthed': True, 'message': Message('You can suddenly see everything!', libtcod.yellow)})

    return results

def prayer(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')
    mana_cost = kwargs.get('mana_cost')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'used': False, 'message': Message('You are already at full health', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        entity.fighter.take_mana_damage(mana_cost)
        results.append({'used': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})

    return results


def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('A lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})

    return results

def cast_mind_lightning(*args, **kwargs,):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = 0 + caster.fighter.starvation_bonus + caster.fighter.psyche
    maximum_range = kwargs.get('maximum_range')
    hunger_cost = 40 +caster.fighter.psyche + (caster.fighter.starvation_bonus / 2)

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        caster.fighter.take_hunger_damage(hunger_cost)
        results.append({'used': True, 'target': target, 'message': Message('A lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'used': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})

    return results

def cast_tornado(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'used': True, 'target': target, 'message': Message('A lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'used': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})

    return results

def throw_shurikin(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('The shuriken strikes the {0} with a loud slash! The damage is {1}'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})

    return results



def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    mana_cost = kwargs.get('mana_cost')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results

def poison_enemy(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    mana_cost = kwargs.get('mana_cost')
    maximum_range = kwargs.get('maximum_range')
    closest_distance = maximum_range + 1

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.distance(target_x, target_y) <= maximum_range and entity.fighter and entity != caster:
            results.append({'message': Message('The {0} is poisoned!'.format(entity.name), libtcod.green)})
            entity.fighter.poisoned = 1
            entity.fighter.poison_timer = randint(10,20)

    return results

def cast_spell_fireball(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    mana_cost = kwargs.get('mana_cost')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    caster.fighter.take_mana_damage(mana_cost)
    results.append({'consumed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_shockwave(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    mana_cost = kwargs.get('mana_cost')

    results = []

    caster.fighter.take_mana_damage(mana_cost)
    results.append({'consumed': True, 'message': Message('A shockwave comes from the {0}\'s feet, damaging everything within {1} tiles!'.format(caster.name,radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(caster.x,caster.y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_charm(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'used': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            charmed_ai = CharmedMonster(entity.ai, 10)

            charmed_ai.owner = entity
            entity.ai = charmed_ai

            results.append({'used': True, 'message': Message('The eyes of the {0} beam with malice! As they attack in frothing fury!'.format(entity.name), libtcod.light_green)})

            break
    else:
        results.append({'used': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results



def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} look vacant, as he starts to stumble around!'.format(entity.name), libtcod.light_green)})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results

def cast_mind_confuse(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []
    hunger_cost = 40 + caster.fighter.psyche + (caster.fighter.starvation_bonus / 2)

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            caster.fighter.take_hunger_damage(hunger_cost)
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} look vacant, as he starts to stumble around!'.format(entity.name), libtcod.light_green)})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results
