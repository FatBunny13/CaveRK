import libtcodpy as libtcod

from random import randint

from game_messages import Message
from entity import Entity
from render_functions import RenderOrder
from fighter import Fighter
from components.item import Item
from eat_functions import eat

class PeacefulMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        results = []

        random_x = self.owner.x + randint(0, 2) - 1
        random_y = self.owner.y + randint(0, 2) - 1

        if random_x != self.owner.x and random_y != self.owner.y:
            self.owner.move_towards(random_x, random_y, game_map, entities)
        return results

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        global npc_target

        results = []

        monster = self.owner
        closest_distance = 10
        for entity in entities:
            if entity.ai and entity.fighter.is_peaceful == False and entity != monster:
                npc_target = entity
        if monster.fighter.is_peaceful == True and npc_target.ai and npc_target.fighter and npc_target.fighter.is_peaceful == False :

            distance = monster.distance_to(npc_target)

            if distance < closest_distance:
                target = npc_target
                closest_distance = distance
                if monster.distance_to(target) >= 2:
                    monster.move_astar(target, entities, game_map)
                elif target.fighter.hp > 0:
                    attack_results = monster.fighter.attack(target)
                    results.extend(attack_results)
            else:
                random_x = self.owner.x + randint(0, 2) - 1
                random_y = self.owner.y + randint(0, 2) - 1

                if random_x != self.owner.x and random_y != self.owner.y:
                    self.owner.move_towards(random_x, random_y, game_map, entities)
        else:
                if monster.fighter.is_peaceful == False and libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

                    if monster.distance_to(target) >= 2:
                        if target.fighter.stealthed == 0:
                            monster.move_astar(target, entities, game_map)
                        else:
                            random_x = self.owner.x + randint(0, 2) - 1
                            random_y = self.owner.y + randint(0, 2) - 1

                            if random_x != self.owner.x and random_y != self.owner.y:
                                self.owner.move_towards(random_x, random_y, game_map, entities)
                    elif target.fighter.hp > 0:
                        attack_results = monster.fighter.attack(target)
                        results.extend(attack_results)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)

        return results

class MagicAttackMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        global npc_target

        results = []

        monster = self.owner
        closest_distance = 10
        for entity in entities:
            if entity.ai and entity.fighter.is_peaceful == False and entity != monster:
                npc_target = entity
        if monster.fighter.is_peaceful == True and npc_target.ai and npc_target.fighter and npc_target.fighter.is_peaceful == False :

            distance = monster.distance_to(npc_target)

            if distance < closest_distance:
                target = npc_target
                closest_distance = distance
                if monster.distance_to(target) >= 2:
                    attack_results = monster.fighter.magic_attack(target)
                    results.extend(attack_results)
                    monster.move_astar(target, entities, game_map)
                elif target.fighter.hp > 0:
                    attack_results = monster.fighter.attack(target)
                    results.extend(attack_results)
            else:
                random_x = self.owner.x + randint(0, 2) - 1
                random_y = self.owner.y + randint(0, 2) - 1

                if random_x != self.owner.x and random_y != self.owner.y:
                    self.owner.move_towards(random_x, random_y, game_map, entities)
        else:
                if monster.fighter.is_peaceful == False and libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

                    if monster.distance_to(target) >= 2:
                        if target.fighter.stealthed == 0:
                            attack_results = monster.fighter.magic_attack(target)
                            results.extend(attack_results)
                            monster.move_astar(target, entities, game_map)
                        else:
                            random_x = self.owner.x + randint(0, 2) - 1
                            random_y = self.owner.y + randint(0, 2) - 1

                            if random_x != self.owner.x and random_y != self.owner.y:
                                self.owner.move_towards(random_x, random_y, game_map, entities)
                    elif target.fighter.hp > 0:
                        attack_results = monster.fighter.attack(target)
                        results.extend(attack_results)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)

        return results

class BeeSpawnerMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        global npc_target

        results = []

        monster = self.owner
        closest_distance = 10
        for entity in entities:
            if entity.ai and entity.fighter.is_peaceful == False and entity != monster:
                npc_target = entity
        if monster.fighter.is_peaceful == True and npc_target.ai and npc_target.fighter and npc_target.fighter.is_peaceful == False :

            distance = monster.distance_to(npc_target)

            if distance < closest_distance:
                target = npc_target
                closest_distance = distance
                if monster.distance_to(target) >= 2:
                    monster.move_astar(target, entities, game_map)
                elif target.fighter.hp > 0:
                    attack_results = monster.fighter.attack(target)
                    results.extend(attack_results)
            else:
                random_x = self.owner.x + randint(0, 2) - 1
                random_y = self.owner.y + randint(0, 2) - 1

                if random_x != self.owner.x and random_y != self.owner.y:
                    self.owner.move_towards(random_x, random_y, game_map, entities)
        else:
                if monster.fighter.is_peaceful == False and libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

                    if monster.distance_to(target) >= 2:
                        if target.fighter.stealthed == 0:
                            monster.move_astar(target, entities, game_map)
                        else:
                            random_x = self.owner.x + randint(0, 2) - 1
                            random_y = self.owner.y + randint(0, 2) - 1

                            if random_x != self.owner.x and random_y != self.owner.y:
                                self.owner.move_towards(random_x, random_y, game_map, entities)
                    elif target.fighter.hp > 0:
                        fighter_component = Fighter(hp=20, defense=2, power=5, xp=100, agility=1, mana=0, base_psyche=0,
                                                    attack_dice_minimum=2, attack_dice_maximum=6, ac=3, will=3,
                                                    talk_message='The Bee-Spawn buzzes')
                        ai_component = BasicMonster()
                        food_component = Item(use_function=eat, amount=25,
                                              eat_message='That meal tastes like jelly!')

                        monster = Entity(self.owner.x, self.owner.y, 'b', libtcod.white, 'Bee-Spawn', blocks=True,
                                         render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                         item=food_component)
                        entities.append(monster)
                        attack_results = monster.fighter.attack(target)
                        results.extend(attack_results)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)

        return results

class HungerMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        global npc_target

        results = []

        monster = self.owner
        closest_distance = 10
        for entity in entities:
            if entity.ai and entity.fighter.is_peaceful == False and entity != monster:
                npc_target = entity
        if monster.fighter.is_peaceful == True and npc_target.ai and npc_target.fighter and npc_target.fighter.is_peaceful == False :

            distance = monster.distance_to(npc_target)

            if distance < closest_distance:
                target = npc_target
                closest_distance = distance
                if monster.distance_to(target) >= 2:
                    monster.move_astar(target, entities, game_map)
                elif target.fighter.hp > 0:
                    attack_results = monster.fighter.attack(target)
                    results.extend(attack_results)
            else:
                random_x = self.owner.x + randint(0, 2) - 1
                random_y = self.owner.y + randint(0, 2) - 1

                if random_x != self.owner.x and random_y != self.owner.y:
                    self.owner.move_towards(random_x, random_y, game_map, entities)
        else:
                if monster.fighter.is_peaceful == False and libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

                    if monster.distance_to(target) >= 2:
                        if target.fighter.stealthed == 0:
                            monster.move_astar(target, entities, game_map)
                        else:
                            random_x = self.owner.x + randint(0, 2) - 1
                            random_y = self.owner.y + randint(0, 2) - 1

                            if random_x != self.owner.x and random_y != self.owner.y:
                                self.owner.move_towards(random_x, random_y, game_map, entities)
                    elif target.fighter.hp > 0:
                        attack_results = monster.fighter.hunger_attack(target)
                        results.extend(attack_results)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)

        return results

class SleepMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        global npc_target
        global attacks
        results = []

        monster = self.owner
        attacks = randint(1,10)
        closest_distance = 10
        for entity in entities:
            if entity.ai and entity.fighter.is_peaceful == False and entity != monster:
                npc_target = entity
        if monster.fighter.is_peaceful == True and npc_target.ai and npc_target.fighter and npc_target.fighter.is_peaceful == False:
            target = npc_target
            if monster.distance_to(target) >= 2:
                if target.fighter.stealthed == 0:
                    monster.move_astar(target, entities, game_map)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)
                        attacks = randint(1, 10)
            elif target.fighter.hp > 0 and target.fighter.paralysis == 0 and 8 <= attacks >= 9 <= attacks <= 10:
                attack_results = monster.fighter.paralysis_attack(target)
                results.extend(attack_results)
                attacks = randint(1, 10)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
                attacks = randint(1, 10)
        else:
                if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

                    if monster.distance_to(target) >= 2:
                        if target.fighter.stealthed == 0:
                            monster.move_astar(target, entities, game_map)
                        else:
                            random_x = self.owner.x + randint(0, 2) - 1
                            random_y = self.owner.y + randint(0, 2) - 1

                            if random_x != self.owner.x and random_y != self.owner.y:
                                self.owner.move_towards(random_x, random_y, game_map, entities)
                                attacks = randint(1, 10)
                    elif target.fighter.hp > 0 and target.fighter.paralysis == 0 and 8 <= attacks >= 9 <= attacks <= 10:
                        attack_results = monster.fighter.paralysis_attack(target)
                        results.extend(attack_results)
                        attacks = randint(1, 10)
                    elif target.fighter.hp > 0:
                        attack_results = monster.fighter.attack(target)
                        results.extend(attack_results)
                        attacks = randint(1, 10)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)

        return results

class PoisonMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        global npc_target
        global attacks
        results = []

        monster = self.owner
        attacks = randint(1,10)
        closest_distance = 10
        for entity in entities:
            if entity.ai and entity.fighter.is_peaceful == False and entity != monster:
                npc_target = entity
        if monster.fighter.is_peaceful == True and npc_target.ai and npc_target.fighter and npc_target.fighter.is_peaceful == False:
            target = npc_target
            if monster.distance_to(target) >= 2:
                if target.fighter.stealthed == 0:
                    monster.move_astar(target, entities, game_map)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)
                        attacks = randint(1, 10)
            elif target.fighter.hp > 0:
                target.fighter.poisoned = 1
                target.fighter.poison_timer = 12
                poison_results = monster.fighter.poison_attack(target)
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
                results.extend(poison_results)
                attacks = randint(1, 10)
        else:
                if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

                    if monster.distance_to(target) >= 2:
                        if target.fighter.stealthed == 0:
                            monster.move_astar(target, entities, game_map)
                        else:
                            random_x = self.owner.x + randint(0, 2) - 1
                            random_y = self.owner.y + randint(0, 2) - 1

                            if random_x != self.owner.x and random_y != self.owner.y:
                                self.owner.move_towards(random_x, random_y, game_map, entities)
                                attacks = randint(1, 10)
                    elif target.fighter.hp > 0 and target.fighter.poisoned == 0 and 8 <= attacks >= 9 <= attacks <= 10:
                        target.fighter.poisoned = 1
                        target.fighter.poison_timer = 12
                        poison_results = monster.fighter.poison_attack(target)
                        attack_results = monster.fighter.attack(target)
                        results.extend(attack_results)
                        results.extend(poison_results)
                        attacks = randint(1, 10)
                    elif target.fighter.hp > 0:
                        attack_results = monster.fighter.attack(target)
                        results.extend(attack_results)
                        attacks = randint(1, 10)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)

        return results

class HasteSelfMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        global attacks
        results = []

        monster = self.owner
        attacks = randint(1,10)
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                if target.fighter.stealthed == 0:
                    monster.move_astar(target, entities, game_map)
                else:
                    random_x = self.owner.x + randint(0, 2) - 1
                    random_y = self.owner.y + randint(0, 2) - 1

                    if random_x != self.owner.x and random_y != self.owner.y:
                        self.owner.move_towards(random_x, random_y, game_map, entities)
                        attacks = randint(1, 10)
            elif monster.fighter.haste == False and 5 <= attacks:
                attack_results = monster.fighter.haste_self()
                results.extend(attack_results)
                attacks = randint(1, 10)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
                attacks = randint(1, 10)
        else:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

        return results


class CharmedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        closest_distance = 10
        if self.number_of_turns > 0:
            for entity in entities:
                if entity.ai and entity.ai != PeacefulMonster and entity != monster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
                    distance = monster.distance_to(entity)

                    if distance < closest_distance:
                        target = entity
                        closest_distance = distance
                        if monster.distance_to(target) >= 2:
                                monster.move_astar(target, entities, game_map)
                        elif target.fighter.hp > 0:
                            attack_results = monster.fighter.attack(target)
                            results.extend(attack_results)
                    else:
                        random_x = self.owner.x + randint(0, 2) - 1
                        random_y = self.owner.y + randint(0, 2) - 1

                        if random_x != self.owner.x and random_y != self.owner.y:
                            self.owner.move_towards(random_x, random_y, game_map, entities)
            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer charmed!'.format(self.owner.name), libtcod.red)})

        return results



class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results

class SlimeMonster:
    def take_turn(self, target, fov_map, game_map, entities,):
        results = []
        monster = self.owner

        random_x = self.owner.x + randint(0, 2) - 1
        random_y = self.owner.y + randint(0, 2) - 1
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

                if target.fighter.hp > 0 and monster.distance_to(target) == 1:
                    attack_results = monster.fighter.attack(target)
                    results.extend(attack_results)

        return results

class ShrubMonster:
    def __init__(self,closest_distance):
        self.closest_distance = closest_distance

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            distance = monster.distance_to(target)
            if distance <= self.closest_distance:

                if target.fighter.hp > 0:
                    attack_results = monster.fighter.attack(target)
                    results.extend(attack_results)

        return results