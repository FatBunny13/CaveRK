import libtcodpy as libtcod
from random import randint
import math

from game_messages import Message
from item_functions import heal

class Boss:
    def __init__(self,boss):
        self.boss = boss

class Jobs:
    def __init__(self, priest_level=0, fighter_level=0, thief_level=0,wizard_level=0,psychic_level=0,enchanter_level=0,diva_level=0,job=0):
        self.priest_level = priest_level
        self.wizard_level = wizard_level
        self.fighter_level = fighter_level
        self.thief_level = thief_level
        self.psychic_level = psychic_level
        self.enchanter_level = enchanter_level
        self.diva_level = diva_level
        self.job = job


class Fighter:
    def __init__(self, hp, defense, power, agility,mana,base_psyche,attack_dice_minimum,attack_dice_maximum,ac,will,blessed=0,doomed=1,poison_timer=0,
                clairvoyance=False,poisoned=0,blessed_timer=0,bless_bonus=0,starvation_bonus = 0,nutrition=0, gender=0,stealthed=0,riposte=0,
                 riposte_time=0,race=0, xp=0,sleep=False,sleep_timer=0,paralysis=False,haste=False,is_peaceful=False,haste_bonus=0,haste_time=0,paralysis_time=0,eat_function = None,
                 talk_message = '',talk_message_2='',talk_message_3='',talk_message_4='',boss=None):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.base_agility = agility
        self.xp = xp
        self.race = race
        self.gender = gender
        self.base_max_mana = mana
        self.mana = mana
        self.nutrition = nutrition
        self.stealthed = stealthed
        self.base_psyche = base_psyche
        self.starvation_bonus = starvation_bonus
        self.attack_dice_minimum = attack_dice_minimum
        self.attack_dice_maximum = attack_dice_maximum
        self.base_ac = ac
        self.base_will = will
        self.blessed = blessed
        self.blessed_timer = blessed_timer
        self.bless_bonus = bless_bonus
        self.poisoned = poisoned
        self.poison_timer = poison_timer
        self.doomed = doomed
        self.clairvoyance = clairvoyance
        self.riposte = riposte
        self.riposte_time = riposte_time
        self.sleep = sleep
        self.sleep_timer = sleep_timer
        self.paralysis = paralysis
        self.paralysis_time = paralysis_time
        self.haste = haste
        self.haste_bonus = haste_bonus
        self.haste_time = haste_time
        self.eat_function = eat_function
        self.is_peaceful = is_peaceful
        self.talk_message = talk_message
        self.talk_message_2 = talk_message_2
        self.talk_message_3 = talk_message_3
        self.talk_message_4 = talk_message_4
        self.boss = boss

    @property
    def max_mana(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_mana_bonus
        else:
            bonus = 0

        return self.base_max_mana + bonus

    @property
    def agility(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.agility_bonus
        else:
            bonus = 0

        return self.base_agility + bonus

    @property
    def psyche(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.psyche_bonus
        else:
            bonus = 0

        return self.base_psyche + bonus
        
    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return (self.base_defense + self.agility) / 2 + bonus

    @property
    def ac(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.ac_bonus
        else:
            bonus = 0

        return self.base_ac + self.haste_bonus + bonus + (self.agility // 3)

    @property
    def ac_agility_bonus(self):
            self.base_ac += 1



    @property
    def will(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.will_bonus
        else:
            bonus = 0

        return self.base_will + bonus + (self.power // 3)


    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def take_psychic_damage(self, amount):
        results = []

        self.hp -= (amount + self.starvation_bonus)

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def take_mana_damage(self, mana_cost):

        self.mana -= mana_cost

    def take_hunger_damage(self, hunger_cost):

        self.nutrition -= hunger_cost

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def eat(self, amount):
        self.nutrition += amount

        if self.nutrition > self.nutrition:
            self.nutrition = self.nutrition

    def weapon_damage (self,damage):
        if self.owner and self.owner.equipment:
            weapon_damage = self.owner.equipment.weapon_damage
        else:
            weapon_damage = 0

        return self.damage + weapon_damage
    
    def attack(self, target):
        results = []
        global damage
        global riposte_chance
        min = 1
        max = 20

        hit_chance = randint(min,max)
        defence_chance = randint(min, max)
        riposte_chance = randint(1,10)

        damage = randint(self.attack_dice_minimum,self.attack_dice_maximum) + self.bless_bonus / self.doomed

        if self.owner.equipment and self.owner.equipment.main_hand and self.owner.equipment.main_hand.equippable:
            damage = (randint(self.owner.equipment.main_hand.equippable.minimum_hit_dice,self.owner.equipment.main_hand.equippable.maximum_hit_dice) // self.doomed) + self.bless_bonus
        else:
            damage = randint(self.attack_dice_minimum, self.attack_dice_maximum) + (
                        self.power // 5) + self.bless_bonus / self.doomed
        if hit_chance + self.will + self.bless_bonus > defence_chance + target.fighter.ac + target.fighter.bless_bonus:
            results = []

            if damage > 0:
                results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                    self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
                results.extend(target.fighter.take_damage(damage))
                damage = randint(self.attack_dice_minimum, self.attack_dice_maximum) + self.bless_bonus / self.doomed
                if target.fighter.riposte == 1 and 9 <= riposte_chance <= 10:
                    results.append({'message': Message('But {0} swiftly reposte\'s {1} attack for {2} hit points!'.format(
                        target.name.capitalize(), self.owner.name, str(damage)), libtcod.white)})
                    results.extend(self.take_damage(damage/2))
                    riposte_chance = randint(1, 10)


            else:
                results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                    self.owner.name.capitalize(), target.name), libtcod.white)})
                damage = randint(self.attack_dice_minimum, self.attack_dice_maximum)

        elif hit_chance == 20:
            results = []

            if damage > 0:
                results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                    self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
                results.extend(target.fighter.take_damage(damage))
                damage = randint(self.attack_dice_minimum, self.attack_dice_maximum)
            elif damage > 2:
                results.append({'message': Message('{0} attacks {1} for {2} hit points. Its a critical strike!'.format(
                    self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
                results.extend(target.fighter.take_damage(damage))
                damage = randint(self.attack_dice_minimum, self.attack_dice_maximum)
            else:
                results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                    self.owner.name.capitalize(), target.name), libtcod.white)})
                damage = randint(self.attack_dice_minimum, self.attack_dice_maximum)

        elif defence_chance == 20:
            results.append({'message': Message('{0} attacks {1} but misses.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})
            damage = randint(self.attack_dice_minimum, self.attack_dice_maximum)


        else:
            results.append({'message': Message('{0} attacks {1} but misses.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})
            damage = randint(self.attack_dice_minimum, self.attack_dice_maximum)


        return results

    def sleep_attack(self,target):
        sleep_attack_chance = randint(1,10)
        sleep_defense_chance = randint(1,10)

        if sleep_attack_chance + self.fighter.will > sleep_defense_chance + self.fighter.will:
            target.fighter.sleep = True
            target.fighter.sleep_timer = randint(10,35)

    def hunger_attack(self,target):
        hunger_damage = randint(5,30)
        target.fighter.take_hunger_damage(target,hunger_damage)
    def paralysis_attack(self,target):
        global paralysis_attack_chance
        global paralysis_defense_chance
        paralysis_attack_chance = randint(1,10)
        paralysis_defense_chance = randint(1,10)

        results = []

        if paralysis_attack_chance + self.will > paralysis_defense_chance + target.fighter.will:
            results.append({'message': Message('{0} paralysis the {1}.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})
            target.fighter.paralysis = True
            target.fighter.paralysis_time = randint(10,35)
            paralysis_attack_chance = randint(1, 10)
            paralysis_defense_chance = randint(1, 10)

        return results

    def haste_self(self):

        results = []
        results.append({'message': Message('{0} suddenly speeds up!.'.format(
                self.owner.name.capitalize()), libtcod.white)})
        self.haste = True
        self.haste_bonus = self.ac
        self.haste_time = randint(10,35)

        return results

    def poison_attack(self,target):

        results = []

        results.append({'message': Message('{0} poisons the {1}!'.format(
            self.owner.name.capitalize(), target.name), libtcod.white)})



    def poison(self, target):
        global poisondamage

        poisondamage = randint(0,4)

        results = []
        results.extend(target.fighter.take_damage(damage))
        poisondamage = randint(0,4)
        return results
