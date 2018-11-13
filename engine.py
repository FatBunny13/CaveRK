import tcod as libtcod

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from initialize_new_game import get_constants, get_game_variables
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from render_functions import clear_all, render_all
from character import Gender
from item_functions import prayer, cast_tornado, heal, cast_lightning,cast_mind_lightning, hide, cast_spell_fireball,cast_charm,cast_shockwave,cast_bless,cast_doom,cast_mind_confuse,become_clairvoyant,poison_enemy
from item_functions import riposte
from components.skills import Skills
from components.skill import Skill
from entity import Entity
from components.ai import PeacefulMonster,BasicMonster
from talk_functions import talk_to_enemy
from npc_list import leader
from quest_list import starting_quest, trash_king_quest
from random import randint

def play_game(player, entities, game_map, message_log,game_state, con, panel, constants):
    fov_recompute = True
    charm_learned = False
    psybolt_learned = False
    hide_learned = False
    fireball_learned = False
    cure_light_learned = False
    shockwave_learned = False
    bless_learned = False
    doom_learned = False
    clairvoyant_learned = False
    cobrakiss_learned = False
    ripostedance_learned = False
    player_has_reached_village = False

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()


    game_state = GameStates.CHARACTER_CREATION
    previous_game_state = game_state

    targeting_item = None
    targeting_skill = None
    ggender = Gender.male


    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            if player.fighter.clairvoyance == 1:
                constants['fov_radius'] = 20
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'],game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(player,key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        use_skills = action.get('use_skills')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        skill_index = action.get('skill_index')
        take_stairs = action.get('take_stairs')
        take_upstairs = action.get('take_upstairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        character_creation = action.get('character_creation')
        job = action.get('job')
        gender = action.get('gender')
        skill_selection = action.get('skill_selection')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        do_you_want_to_attack = action.get('do_you_want_to_attack')
        talk = action.get('talk')
        show_quests = action.get('show_quests')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []


        if move and game_state == GameStates.PLAYERS_TURN and player.fighter.paralysis == 0:
            starvation_variable = 1
            player.fighter.nutrition -= 1
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            for entity in entities:
                if entity.ai and entity.fighter.stealthed is 1 and player.fighter.clairvoyance is False:
                    entity.char = ' '
                elif entity.ai and entity.fighter.stealthed is 1 and player.fighter.clairvoyance is True:
                    entity.char = entity.CHAR

            for entity in entities:
                if entity.fighter and entity.fighter.poisoned == 1:
                    entity.fighter.take_damage(randint(1,4))
                    if entity.ai and entity.fighter.hp <= 1:
                        kill_monster(entity)
                    if entity.player and entity.fighter.hp <= 1:
                        kill_player(entity)
                        game_state = GameStates.PLAYER_DEAD

            for entity in entities:
                if entity.fighter and entity.fighter.riposte == 1:
                    entity.fighter.riposte_time -= 1
                    if entity.fighter.riposte_time == 0:
                        message_log.add_message(Message(
                            'The {0} suddenly has less grace.'.format(entity.name), libtcod.red))
                        entity.fighter.riposte = 0

            for entity in entities:
                if entity.fighter and entity.fighter.poisoned == 1:
                    entity.fighter.poison_timer -= 1
                    if entity.fighter.poison_timer == 0:
                        entity.fighter.poison = 0

            for entity in entities:
                if entity.fighter and entity.ai and entity.fighter.paralysis == 1:
                    entity.fighter.paralysis_time -= 1
                    if entity.fighter.paralysis_time == 0:
                        entity.fighter.paralysis = 0
                        message_log.add_message(Message('The {0}!'.format(entity.name), libtcod.yellow))
                    pass





            if player.fighter.nutrition <= 0:
                kill_player(player)
                game_state = GameStates.PLAYER_DEAD
                message_log.add_message(Message('You have starved to death.', libtcod.red))

            if player.fighter.starvation_bonus >= 20 and player.fighter.psyche <= 5 or player.fighter.psyche == 5:
                starvation_variable = 0
            elif player.fighter.starvation_bonus >= 40 and player.fighter.psyche <= 10 or player.fighter.psyche == 10:
                starvation_variable = 0

            if player.fighter.nutrition <= 100:
                player.fighter.starvation_bonus += starvation_variable

            elif player.fighter.nutrition >= 100:
                player.fighter.starvation_bonus += 0

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target and target.fighter:
                    if target.fighter.is_peaceful is False:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)
                        game_state = GameStates.ENEMY_TURN
                    elif target.fighter.is_peaceful is True:
                        game_state = GameStates.ATTACK_MENU
                elif target and target.blocks == True:
                    message_log.add_message(Message('You cannot walk through the {0}!'.format(target.name)))
                    pass
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                    game_state = GameStates.ENEMY_TURN

        elif talk:
            message_log.add_message(Message('Click on a monster to talk. Right click to cancel talking'))
            previous_game_state = GameStates.PLAYERS_TURN
            game_state = GameStates.TALK_TARGETING


        elif do_you_want_to_attack:
            if do_you_want_to_attack == 'yes':
                attack_results = player.fighter.attack(target)
                player_turn_results.extend(attack_results)
                target.fighter.is_peaceful = False
                game_state = GameStates.ENEMY_TURN
            else:
                game_state = GameStates.ENEMY_TURN

        elif game_state == GameStates.PLAYERS_TURN and player.fighter.paralysis == 1:
                game_state = GameStates.ENEMY_TURN
                player.fighter.paralysis_time -= 1
                if player.fighter.paralysis_time == 0:
                    player.fighter.paralysis = 0
                    message_log.add_message(Message('You are no longer paralysed!', libtcod.yellow))
                pass

        elif wait:
            game_state = GameStates.ENEMY_TURN

        elif gender == Gender.male:
            player.fighter.gender = 1

        elif gender == Gender.female:
            player.fighter.gender = 2

        elif gender == Gender.agender:
            player.fighter.gender = 3

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if (entity.item or entity.equippable) and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY
            libtcod.console_flush()

        if show_quests:
            previous_game_state = game_state
            game_state = GameStates.QUEST_MENU
            libtcod.console_flush()

        if use_skills:
            previous_game_state = game_state
            game_state = GameStates.SHOW_SKILL_MENU
            libtcod.console_flush()

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY
            libtcod.console_flush()

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
                libtcod.console_flush()
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))
                libtcod.console_flush()

        if skill_index is not None and previous_game_state != GameStates.PLAYER_DEAD and skill_index < len(
                player.skills.number_of_skills):
            skill = player.skills.number_of_skills[skill_index]

            if game_state == GameStates.SHOW_SKILL_MENU:
                player_turn_results.extend(player.skills.use(skill, entities=entities, fov_map=fov_map))
                libtcod.console_flush()

        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.upstairs and entity.x == player.x and entity.y == player.y:
                    message_log.add_message(Message('You cannot go down these stairs.', libtcod.yellow))
                    break
                elif entity.stairs and entity.stairs.moth_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_moth_cave_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)
                elif entity.stairs and entity.stairs.wyld_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.go_to_wyld(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
                elif entity.stairs and entity.stairs.dungeon_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break

                elif entity.stairs and entity.stairs.red_cave_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_red_cave_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        if take_upstairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:

                if entity.upstairs and entity.upstairs.dungeon_stairs == True and entity.upstairs and entity.upstairs.red_cave_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.leave_red_cave(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
                elif entity.upstairs and entity.upstairs.wyld_stairs == True and entity.upstairs.moth_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.leave_moth_cave(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
                elif entity.upstairs and entity.upstairs.wyld_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.leave_wyld(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
                elif entity.upstairs and entity.upstairs.dungeon_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.previous_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
                elif entity.upstairs and entity.upstairs.moth_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.previous_moth_cave_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
                elif entity.upstairs and entity.upstairs.red_cave_stairs == True and entity.x == player.x and entity.y == player.y:
                    entities = game_map.previous_red_cave_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 10
                player.fighter.hp += 10
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1
            libtcod.console_flush()
            game_state = GameStates.JOB_SELECTION

        if job:
            if job == 'pri':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
                player.job.job = 1
                player.job.priest_level += 1
                skill_component = Skill(use_function=prayer, amount=40, mana_cost=5)
                cure_light = Entity(0, 0, '?', libtcod.yellow, 'Cure Light Wounds', skill=skill_component)
                if cure_light and cure_light_learned is False:
                    cure_light_learned = True
                    player.skills.add_skill(cure_light)
            elif job == 'fig':
                player.fighter.base_power += 2
                player.fighter.base_defense += 1
                player.job.job = 2
                player.job.fighter_level += 1
            elif job == 'thi':
                skill_component = Skill(use_function=hide)
                shadow_self = Entity(0, 0, '?', libtcod.yellow, 'Hide', skill=skill_component)
                player.fighter.base_defense += 2
                player.fighter.base_power += 1
                player.fighter.base_agility += 1
                player.job.job = 3
                player.job.thief_level += 1
                if shadow_self and hide_learned is False:
                    hide_learned = True
                    player.skills.add_skill(shadow_self)
            elif job == 'wiz':
                player.job.job = 4
                player.job.wizard_level += 1
                shock_component = Skill(use_function=cast_shockwave, mana_cost=10,
                                        damage=25, radius=3)
                skill_component = Skill(use_function=cast_spell_fireball, mana_cost=10, skill_targeting=True,
                                        targeting_message=Message(
                                            'Left-click a target tile for the fireball, or right-click to cancel.',
                                            libtcod.light_cyan),
                                        damage=25, radius=3)
                x = entity.x
                y = entity.y
                shockwave = Entity(x,y,'?',libtcod.red, 'Shockwave',skill=shock_component)
                fireball = Entity(x, y, '?', libtcod.red, 'Fireball', skill=skill_component)
                if shockwave and shockwave_learned is False:
                    shockwave_learned = True
                    player.skills.add_skill(shockwave)
                if fireball and fireball_learned is False:
                    fireball_learned = True
                    player.skills.add_skill(fireball)
            elif job == 'psy':
                skill_component = Skill(use_function=cast_mind_confuse, skill_targeting=True,
                                        targeting_message=Message(
                                            'Left-click on an enemy to charm them, or right-click to cancel.',
                                            libtcod.light_cyan))
                x = entity.x
                y = entity.y
                charm = Entity(x, y, '?', libtcod.red, 'Feeblemind', skill=skill_component)
                player.fighter.base_psyche += 3
                player.job.job = 5
                player.job.psychic_level += 1
                skill_component = Skill(use_function=cast_mind_lightning, maximum_range=5,
                                        hunger_cost=40 + player.fighter.psyche / 2)
                psybolt = Entity(0, 0, ' ', libtcod.yellow, 'PsyBolt', skill=skill_component)
                if psybolt and psybolt_learned is False:
                    psybolt_learned = True
                    player.skills.add_skill(psybolt)
                if charm and charm_learned is False and player.job.psychic_level >= 4:
                    player.skills.add_skill(charm)
                    charm_learned = True
            elif job == 'enchant':
                skill_component = Skill(use_function=cast_bless, mana_cost=10, skill_targeting=True,
                                        targeting_message=Message(
                                            'Left-click a target tile to bless them, or right-click to cancel.',
                                            libtcod.light_cyan))
                x = entity.x
                y = entity.y
                bless = Entity(x, y, '?', libtcod.red, 'Bless', skill=skill_component)
                skill_component = Skill(use_function=cast_doom, mana_cost=10, skill_targeting=True,
                                        targeting_message=Message(
                                            'Left-click a target tile to doom them, or right-click to cancel.',
                                            libtcod.light_cyan))
                x = entity.x
                y = entity.y
                doom = Entity(x, y, '?', libtcod.red, 'Doom', skill=skill_component)
                clairvoyance_component = Skill(use_function=become_clairvoyant, mana_cost=10, skill_targeting=True,
                                        targeting_message=Message(
                                            'Left-click a target tile to doom them, or right-click to cancel.',
                                            libtcod.light_cyan))
                x = entity.x
                y = entity.y
                clairvoyant = Entity(x, y, '?', libtcod.red, 'Clairvoyance', skill=clairvoyance_component)
                player.job.enchanter_level += 1
                if bless_learned is False:
                    bless_learned = True
                    player.skills.add_skill(bless)
                if clairvoyant_learned is False and player.job.enchanter_level >= 1:
                    clairvoyant_learned = True
                    player.skills.add_skill(clairvoyant)
                if doom_learned is False and player.job.enchanter_level >= 10:
                    doom_learned = True
                    player.skills.add_skill(doom)
            elif job == 'diva':
                player.job.diva_level += 1
                riposte_component = Skill(use_function=riposte)
                ripostedance = Entity(0, 0, '?', libtcod.yellow, 'Riposte Dance', skill=riposte_component)
                skill_component = Skill(use_function=poison_enemy, mana_cost=10, skill_targeting=True, maximum_range=1,
                                        targeting_message=Message(
                                            'Left-click a target tile to poison them, or right-click to cancel.',
                                            libtcod.light_cyan))
                x = entity.x
                y = entity.y
                cobrakiss = Entity(x, y, '?', libtcod.red, 'Kiss of the Cobra', skill=skill_component)
                if ripostedance_learned is False and player.job.diva_level == 2:
                    ripostedance_learned = True
                    player.skills.add_skill(ripostedance)
                if cobrakiss_learned is False:
                    cobrakiss_learned = True
                    player.skills.add_skill(cobrakiss)
            libtcod.console_flush()
            game_state = GameStates.PLAYERS_TURN

        if character_creation:
            if character_creation == 'mern':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
                player.fighter.race += 1
            elif character_creation == 'avis':
                player.fighter.base_power += 1
                player.fighter.race += 2
            elif character_creation == 'lepra':
                player.fighter.base_defense += 1
                player.fighter.race += 3
            elif character_creation == 'giant':
                player.fighter.base_agility -= 5
                player.fighter.base_power += 6
                player.fighter.hp += 60
                player.fighter.base_max_hp += 60
                player.fighter.race += 4
            elif character_creation == 'change':
                player.fighter.base_agility += 2
                player.fighter.race += 5
            elif character_creation == 'fae':
                player.fighter.base_agility += 10
                player.fighter.hp -= 75
                player.fighter.base_max_hp -= 75
                player.fighter.race += 6
            libtcod.console_flush()
            game_state = GameStates.GENDER_SELECTION
        # damn son thats a lot of menus
        # like a lot

        if gender:
                if gender == 'm':
                    player.fighter.base_max_hp += 10
                    player.fighter.hp += 10
                    player.fighter.gender += 1
                elif gender == 'f':
                    player.fighter.base_power += 5
                    player.fighter.base_max_hp -= 20
                    player.fighter.hp -= 20
                    player.fighter.gender += 2
                elif gender == 'a':
                    player.fighter.gender += 3
                libtcod.console_flush()
                game_state = GameStates.PLAYERS_TURN

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
                libtcod.console_flush()
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})
                libtcod.console_flush()

        if game_state == GameStates.SKILL_TARGETING:
            if left_click:
                target_x, target_y = left_click

                skill_use_results = player.skills.use(targeting_skill, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(skill_use_results)
                libtcod.console_flush()
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})
                libtcod.console_flush()

        if game_state == GameStates.TALK_TARGETING:
            if left_click:
                target_x, target_y = left_click
                for entity in entities:
                    if entity == leader and leader.x == target_x and leader.y == target_y and player_has_reached_village == False:
                        leader.fighter.talk_message =('Oh my god-fae you\'re alive! We need your help! While you were gone we have been under attack by Trashling Rebels')
                        leader.fighter.talk_message_2 = ('They have been trying to send a message to the other races')
                        leader.fighter.talk_message_3 = ('By trying to raid our villages. ')
                        leader.fighter.talk_message_4 = ('We need your help. Please slay their leader. The cruel Trash-King!')
                        player_has_reached_village = True
                        player.fighter.xp += 50
                        starting_quest.completed = True
                        trash_king_quest.quest.has_quest = True
                        player.quests.add_quest(trash_king_quest)
                        for quest in player.quests.quests:
                            player.quests.remove_quest(starting_quest)
                    elif entity == leader and leader.x == target_x and leader.y == target_y and player_has_reached_village == True and player.game_variables.killed_trash_king == True and trash_king_quest.quest.completed ==False:
                        message_log.add_message(Message('Hooray the Trash-King is dead!', libtcod.lighter_blue))
                        message_log.add_message(Message('Now we can mine Red Clay now!', libtcod.lighter_blue))
                        message_log.add_message(Message('Well you\'re certainly strong! Some of the villagers need help!', libtcod.lighter_blue))
                        message_log.add_message(Message('We need a hero like you. Talk to me when you get stronger', libtcod.lighter_blue))
                        leader.fighter.talk_message = (
                            'Have you finished all of the villagers demands?')
                        leader.fighter.talk_message_2 = 'If you have. Maybe go exploring! Who knows what you may find!'
                        leader.fighter.talk_message_3 = 'I know that one of the sprites wants to get her friend some sweets! Maybe ask her?'
                        leader.fighter.talk_message_4 = 'I know that dapper looking Trashling also needs some help too!'
                        player.fighter.xp += 500
                        trash_king_quest.quest.completed = True
                        player.quests.remove_quest(trash_king_quest)
                    elif entity == leader and leader.x == target_x and leader.y == target_y and player_has_reached_village == True and trash_king_quest.quest.has_quest == True and player.game_variables.killed_trash_king == False:
                        leader.fighter.talk_message = (
                            'I fear for the village! Please defeat the rebels!')
                        leader.fighter.talk_message_2 = 'I wish for the little sprite darlings I tutor to be safe!'
                        leader.fighter.talk_message_3 = 'I love them so much! But my goodness! One is so rambunctious she nearly snow on fire!'
                        leader.fighter.talk_message_4 = 'It\'s literally impossible yet she did it anyways!'
                    elif entity == leader and leader.x == target_x and leader.y == target_y and trash_king_quest.quest.completed == True:
                        pass

                talk_results = talk_to_enemy(player=player,entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(talk_results)
                libtcod.console_flush()

            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})
                libtcod.console_flush()

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
                libtcod.console_flush()
            elif game_state == GameStates.SHOW_SKILL_MENU:
                game_state = GameStates.PLAYERS_TURN
                libtcod.console_flush()
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
                libtcod.console_flush()
            elif game_state == GameStates.SKILL_TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
                libtcod.console_flush()
            elif game_state == GameStates.TALK_TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
                libtcod.console_flush()
            elif game_state == GameStates.QUEST_MENU:
                game_state = GameStates.PLAYERS_TURN
                libtcod.console_flush()
            else:
                save_game(player, entities, game_map, message_log, game_state)
                libtcod.console_flush()

                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            skill_added = player_turn_result.get('skill_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            skill_targeting = player_turn_result.get('skill_targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')
            skill_used = player_turn_result.get('used')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity,player)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if skill_added:
                game_state = GameStates.ENEMY_TURN

            if skill_used:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))

                    if dequipped:
                        message_log.add_message(Message('You dequipped the {0}'.format(dequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if skill_targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.SKILL_TARGETING

                targeting_skill = skill_targeting

                message_log.add_message(targeting_skill.skill.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('You gain {0} experience points.'.format(xp)))

                if leveled_up:

                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP


        if game_state == GameStates.ENEMY_TURN:

            if player.fighter.nutrition <= 0:
                kill_player(player)
                game_state = GameStates.PLAYER_DEAD
                message_log.add_message(Message('You have starved to death.', libtcod.red))

            if player.fighter.nutrition <= 100 and player.fighter.stealthed == 1:
                player.fighter.stealthed = 0

            for entity in entities:
                if entity.fighter:
                    if entity.fighter.blessed == 1:
                        entity.fighter.blessed_timer -= 1
                        if entity.fighter.blessed_timer == 0:
                            message_log.add_message(Message(
                                'The {0}\'s shine fades away.'.format(entity.name),libtcod.red))
                            entity.fighter.blessed = 0
                            entity.fighter.bless_bonus = 0

                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity,player)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


def main():
    constants = get_constants()

    libtcod.console_set_custom_font('dejavu_wide16x16_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])

    # Debugging info: at this point con is a big integer. Later on we find that it is something
    # else. What is going on?
    # Hopefully fixed. Most likely an error in libtcod engine. Fixed when moving to more python
    # specific engine. Python-tcod

    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None
    ggender = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = libtcod.image_load('menu_background.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'],
                      constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key, player,)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state, ggender = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state, ggender = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            libtcod.console_flush()
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con,panel, constants)
            show_main_menu = True


if __name__ == '__main__':
    main()
