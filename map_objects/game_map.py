import tcod as libtcod
from random import randint

from components.ai import BasicMonster, SlimeMonster, ShrubMonster,SleepMonster,HasteSelfMonster,PeacefulMonster,PoisonMonster,HungerMonster,BeeSpawnerMonster,MagicAttackMonster
from components.equipment import EquipmentSlots, Equipment
from components.equippable import Equippable
from components.inventory import Inventory
from fighter import Fighter, Boss
from components.item import Item
from components.stairs import Stairs
from components.upstair import Upstairs

from entity import Entity
from quest_list import starting_quest
from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, heal, throw_shurikin,special_powder

from map_objects.rectangle import Rect, Hexagon
from map_objects.tile import Tile

from random_utils import from_dungeon_level, random_choice_from_dict
from npc_list import leader,bandit,sprite_child_1,sprite_child_2,dapper_trashling,fancy_trashling,shy_giantess

from render_functions import RenderOrder
from static_npc_and_location_spawns import *
from entity_list import *
from eat_functions import eat,eat_cursed,eat_poison


class GameMap:

    def __init__(self, width, height, dungeon_level=1,red_cave_level=0,moth_cave_level=0,village = False,overworld=False,wyld=False,bees_nest_level = 0):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level
        self.red_cave_level = red_cave_level
        self.moth_cave_level = moth_cave_level
        self.bees_nest_level = bees_nest_level
        self.village = village
        self.overworld = overworld
        self.wyld = wyld

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def create_tile(self, x,y):
        # go through the tiles in the rectangle and make them passable
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def make_map(self, max_rooms, room_min_size, room_max_size,max_maze_rooms,maze_min_size, maze_max_size, map_width, map_height, player, entities):
        global players_stairs
        if 3 >= self.red_cave_level >= 2:
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_rooms):
                # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

                # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

                # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                    # this means there are no intersections, so this room is valid

                    # "paint" it to the map's tiles
                    self.create_room(new_room)

                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                        # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_red_cave_entities(new_room, entities)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

            stairs_component = Stairs(self.red_cave_level + 1, red_cave_stairs=True)
            down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.darker_red, 'Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)

            upstairs_component = Upstairs(self.red_cave_level + 1, red_cave_stairs=True)
            cave_stairs = Entity(player.x, player.y, '<', libtcod.darker_red, 'Cave Stairs',
                               render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(cave_stairs)
        elif self.bees_nest_level == 3:
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_rooms):
                # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

                # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

                # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                    # this means there are no intersections, so this room is valid

                    # "paint" it to the map's tiles
                    self.create_honeycomb(new_room,map_width,map_height)

                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                        # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    elif num_rooms == 1:
                        text_story_1 = Entity(28, 10, '*', libtcod.white, 'Tile with a Drawing', has_message=True,
                                               text_message_1='You see a drawing on the ground.',
                                               text_message_2='The drawing is of a sickly bee man in bed and a bee-woman',
                                               text_message_3='The bee-woman is tending to the bee-man. The bee-man is thankful')
                        entities.append(text_story_1)
                        text_story_1.x = new_x
                        text_story_1.y = new_y
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    elif num_rooms == 2:
                        text_story_1 = Entity(28, 10, '*', libtcod.white, 'Tile with a Drawing', has_message=True,
                                               text_message_1='You see a drawing on the ground.',
                                               text_message_2='The drawing is of a sickly bee man in a wheelchair and a bee-woman',
                                               text_message_3='The bee-woman is sitting outside with the bee-man. They look content')
                        entities.append(text_story_1)
                        text_story_1.x = new_x
                        text_story_1.y = new_y
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    elif num_rooms == 3:
                        text_story_1 = Entity(28, 10, '*', libtcod.white, 'Tile with a Drawing', has_message=True,
                                               text_message_1='You see a drawing on the ground.',
                                               text_message_2='The drawing is of a sickly bee man in bed and a bee woman.',
                                               text_message_3='They are kissing. They look euphoric.')
                        entities.append(text_story_1)
                        text_story_1.x = new_x
                        text_story_1.y = new_y
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    elif num_rooms == 4:
                        text_story_1 = Entity(28, 10, '*', libtcod.white, 'Tile with a Drawing', has_message=True,
                                               text_message_1='You see a drawing on the ground.',
                                               text_message_2='The drawing is of a sickly bee man in a wheelchair and a bee woman.',
                                               text_message_3='The bee-man is teaching the bee-woman magic. The bee-woman is on fire. The bee woman is not happy.')
                        entities.append(text_story_1)
                        text_story_1.x = new_x
                        text_story_1.y = new_y
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    elif num_rooms == 5:
                        text_story_1 = Entity(28, 10, '*', libtcod.white, 'Tile with a Drawing', has_message=True,
                                               text_message_1='You see a drawing on the ground.',
                                               text_message_2='The drawing is of a sickly bee man in a wheelchair and a bee woman and some powder.',
                                               text_message_3='The bee-woman gives some of the powder to the bee-man. He looks healthier and happier.')
                        entities.append(text_story_1)
                        text_story_1.x = new_x
                        text_story_1.y = new_y
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_bee_nest_entities(new_room, entities)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

            stairs_component = Stairs(self.red_cave_level + 1, bees_stairs=True)
            down_stairs = Entity(center_of_last_room_y, center_of_last_room_y, '>', libtcod.yellow, 'Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)
            upstairs_component = Upstairs(self.dungeon_level + 1, dungeon_stairs=True, bees_stairs=True)
            up_stairs = Entity(player.x, player.y, '<', libtcod.yellow, 'Stairs back to the Wyld',
                               render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(up_stairs)
        elif self.bees_nest_level == 2:
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_rooms):
                # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

                # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

                # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                    # this means there are no intersections, so this room is valid

                    # "paint" it to the map's tiles
                    self.create_honeycomb(new_room,map_width,map_height)

                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                        # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    elif num_rooms == 1:
                        text_story_1 = Entity(28, 10, '*', libtcod.white, 'Tile with a Drawing', has_message=True,
                                               text_message_1='You see a drawing on the ground.',
                                               text_message_2='The drawing is of the Moth-Mother and a bee-woman and some powder',
                                               text_message_3='The The Moth-Mother is taking some powder away from the bee-woman. She is crying')
                        entities.append(text_story_1)
                        text_story_1.x = new_x
                        text_story_1.y = new_y
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    elif num_rooms == 2:
                        text_story_1 = Entity(28, 10, '*', libtcod.white, 'Tile with a Drawing', has_message=True,
                                               text_message_1='You see a drawing on the ground.',
                                               text_message_2='The drawing is of a coffin and a bee-woman',
                                               text_message_3='The bee-woman is crying.')
                        entities.append(text_story_1)
                        text_story_1.x = new_x
                        text_story_1.y = new_y
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    elif num_rooms == 3:
                        text_story_1 = Entity(28, 10, '*', libtcod.white, 'Tile with a Drawing', has_message=True,
                                               text_message_1='You see a drawing on the ground.',
                                               text_message_2='The drawing is of a lich and a bee-woman',
                                               text_message_3='The bee-woman is bargaining with the lich. The lich is laughing.')
                        entities.append(text_story_1)
                        text_story_1.x = new_x
                        text_story_1.y = new_y
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    elif num_rooms == 4:
                        text_story_1 = Entity(28, 10, '*', libtcod.white, 'Tile with a Drawing', has_message=True,
                                               text_message_1='You see some writing on the ground.',
                                               text_message_2='WHAT HAPPENED TO OUR QUEEN!.',)
                        entities.append(text_story_1)
                        text_story_1.x = new_x
                        text_story_1.y = new_y
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_bee_nest_entities(new_room, entities)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

            stairs_component = Stairs(self.red_cave_level + 1, bees_stairs=True)
            down_stairs = Entity(center_of_last_room_y, center_of_last_room_y, '>', libtcod.yellow, 'Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)
            upstairs_component = Upstairs(self.dungeon_level + 1, bees_stairs=True)
            up_stairs = Entity(player.x, player.y, '<', libtcod.yellow, 'Stairs',
                               render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(up_stairs)
        elif self.bees_nest_level == 1:
            map = open('beehive.txt')
            contents = map.read()
            player.x = 32
            player.y = 12
            inventory_component = Inventory(26)
            boss_component_1 = Boss(boss=3)
            bee_boss_1_component = Fighter(hp=80, defense=2, power=4, xp=50, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=2, attack_dice_maximum=8, ac=0, will=5,
                                boss=boss_component_1)
            food_boss_1_component = Item(use_function=eat_poison, amount=-30,
                                  eat_message='You eat the Queen-Bee. Agh its poisonous!')
            bee_boss_1_ai_component = PoisonMonster()

            bee_boss_1 = Entity(32, 3, 'b', libtcod.darker_purple, 'Ghostly Queen-Bee', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=bee_boss_1_component, ai=bee_boss_1_ai_component,
                             item=food_boss_1_component,inventory=inventory_component)
            entities.append(bee_boss_1)
            boss_component_2 = Boss(boss=4)
            bee_boss_2_component = Fighter(hp=30, defense=2, power=4, xp=50, agility=1, mana=0, base_psyche=0,
                                           attack_dice_minimum=1, attack_dice_maximum=3, ac=0, will=5,
                                boss=boss_component_2)
            food_boss_2_component = Item(use_function=eat_poison, amount=-30,
                                         eat_message='You eat the Drone-Bee. Agh its poisonous!')
            bee_boss_2_ai_component = MagicAttackMonster()

            bee_boss_2 = Entity(32, 4, 'b', libtcod.lighter_blue, 'Ghostly Drone-Bee', blocks=True,
                                render_order=RenderOrder.ACTOR, fighter=bee_boss_2_component,inventory=inventory_component,
                                ai=bee_boss_2_ai_component,
                                item=food_boss_2_component)
            entities.append(bee_boss_2)
            for tile_y, line in enumerate(contents.split('\n')):
                for tile_x, tile_character in enumerate(line):
                    if tile_character == '.':
                        self.create_tile(tile_x, tile_y)
        elif self.red_cave_level == 4:
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_rooms):
                # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

                # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

                # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                    # this means there are no intersections, so this room is valid

                    # "paint" it to the map's tiles
                    self.create_room(new_room)

                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                        # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_red_cave_entities(new_room, entities)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

            fighter_component = Fighter(hp=10, defense=1, power=2, xp=100, agility=4, mana=0, base_psyche=0,
                                        attack_dice_minimum=1, attack_dice_maximum=2, ac=10, will=0,boss=2,
                                        talk_message='The Trash-King starts screaming in rage!')
            ai_component = ShrubMonster(closest_distance=5)
            food_component = Item(use_function=eat_cursed, amount=25,
                                  eat_message='That meal is truly for a king! Smells like trash though.')

            trash_king = Entity(center_of_last_room_x, center_of_last_room_y, 'T', libtcod.gray, 'Trash-King',
                                blocks=True,
                                fighter=fighter_component,
                                render_order=RenderOrder.ACTOR, ai=ai_component,item=food_component)
            entities.append(trash_king)

            upstairs_component = Upstairs(self.red_cave_level + 1, red_cave_stairs=True)
            up_stairs = Entity(center_of_last_room_y, center_of_last_room_y, '<', libtcod.darker_red, 'Stairs',
                               render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(up_stairs)

        elif self.red_cave_level == 1:
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_rooms):
                # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

                # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

                # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                    # this means there are no intersections, so this room is valid

                    # "paint" it to the map's tiles
                    self.create_room(new_room)

                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                        # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_red_cave_entities(new_room, entities)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

            stairs_component = Stairs(self.red_cave_level + 1, red_cave_stairs=True)
            down_stairs = Entity(center_of_last_room_y, center_of_last_room_y, '>', libtcod.darker_red, 'Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)
            upstairs_component = Upstairs(self.dungeon_level + 1, dungeon_stairs=True, red_cave_stairs=True)
            up_stairs = Entity(player.x, player.y, '<', libtcod.darker_red, 'Stairs back to Havoc',
                               render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(up_stairs)

        elif self.moth_cave_level == 1:
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_rooms):
                # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

                # "Rect" class makes rectangles easier to work with
                new_room = Hexagon(x, y, w, h)

                # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                    # this means there are no intersections, so this room is valid

                    # "paint" it to the map's tiles
                    self.create_hexagon(new_room,map_width,map_height)

                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    if self.tiles[new_x][new_y].blocked == True:
                        self.tiles[new_x][new_y].blocked = False
                        self.tiles[new_x][new_y].block_sight = False

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                        # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_moth_cave_entities(new_room, entities)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

            stairs_component = Stairs(self.red_cave_level + 1, moth_stairs=True)
            down_stairs = Entity(center_of_last_room_y, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)
            upstairs_component = Upstairs(self.dungeon_level + 1, wyld_stairs=True, moth_stairs=True)
            up_stairs = Entity(player.x, player.y, '<', libtcod.white, 'Stairs back to the Wyld',
                               render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(up_stairs)
        elif self.moth_cave_level == 2:
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_rooms):
                # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

                # "Rect" class makes rectangles easier to work with
                new_room = Hexagon(x, y, w, h)

                # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                    # this means there are no intersections, so this room is valid

                    # "paint" it to the map's tiles
                    self.create_hexagon(new_room, map_width, map_height)

                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    if self.tiles[new_x][new_y].blocked == True:
                        self.tiles[new_x][new_y].blocked = False
                        self.tiles[new_x][new_y].block_sight = False

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                        # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_moth_cave_entities(new_room, entities)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

            stairs_component = Stairs(self.red_cave_level + 1, moth_stairs=True)
            down_stairs = Entity(center_of_last_room_y, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)
            upstairs_component = Upstairs(self.dungeon_level + 1, moth_stairs=True)
            up_stairs = Entity(player.x, player.y, '<', libtcod.white, 'Stairs',
                               render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(up_stairs)
        elif self.moth_cave_level == 3:
            moth = open('moth_cave.txt')
            contents = moth.read()
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for tile_y, line in enumerate(contents.split('\n')):
                for tile_x, tile_character in enumerate(line):
                    if tile_character == '.':
                        self.create_tile(tile_x,tile_y)

            for r in range(max_rooms):
                # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

                # "Rect" class makes rectangles easier to work with
                new_room = Hexagon(x, y, w, h)

                # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                    # this means there are no intersections, so this room is valid

                    # "paint" it to the map's tiles
                    self.create_hexagon(new_room, map_width, map_height)

                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    if self.tiles[new_x][new_y].blocked == True:
                        self.tiles[new_x][new_y].blocked = False
                        self.tiles[new_x][new_y].block_sight = False

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                        # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                        prev_x = 15
                        prev_y = 10
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_moth_cave_entities(new_room, entities)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

            fighter_component = Fighter(hp=5, defense=2, power=5, xp=5000, agility=1, mana=0, base_psyche=0,
                                        attack_dice_minimum=1, attack_dice_maximum=4, ac=5, will=3, talk_message='hi')
            food_component = Item(use_function=eat_cursed, amount= -20,
                                  eat_message='You feel a darkness brewing inside you.')
            ai_component = PoisonMonster()
            inventory_component = Inventory(26)

            mother_moth = Entity(15, 10, 'm', libtcod.darker_purple, 'Mother-Moth', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                             item=food_component,inventory=inventory_component)
            entities.append(mother_moth)
            item_component = Item(use_function=special_powder,entities=entities,game_map = self)

            powder = Entity(3, 4, '*', libtcod.yellow, 'Strange Powder', item=item_component)
            mother_moth.inventory.add_item(powder)
            upstairs_component = Upstairs(self.dungeon_level + 1, moth_stairs=True)
            up_stairs = Entity(player.x, player.y, '<', libtcod.white, 'Stairs',
                               render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(up_stairs)

        elif self.wyld == True:
            wyld = open('wyld.txt')
            contents = wyld.read()
            stairs_component = Upstairs(self.dungeon_level - 1, wyld_stairs=True)
            havoc_stairs = Entity(30, 16, '<', libtcod.white, 'Stairs back to Havoc',
                                 render_order=RenderOrder.STAIRS, upstairs=stairs_component)
            moth_component = Stairs(self.dungeon_level - 1, moth_stairs=True)
            moth_stairs = Entity(30, 15, '>', libtcod.white, 'Stairs to the Moth-Nest',
                                  render_order=RenderOrder.STAIRS, stairs=moth_component)
            item_component = Item(use_function=special_powder, entities=entities, game_map=self)

            powder = Entity(2, 4, '*', libtcod.yellow, 'Strange Powder', item=item_component)
            entities.append(powder)
            if player.game_variables.bees_nest_spawned == False:
                entities.append(buzzing_tile)
            else:
                bees_component = Stairs(self.dungeon_level - 1,bees_stairs=True)
                bees_stairs = Entity(3, 4, '>', libtcod.yellow, 'Stairs to the Bees-Nest',
                                     render_order=RenderOrder.STAIRS, stairs=bees_component)
                entities.append(bees_stairs)
            entities.append(havoc_stairs)
            entities.append(moth_stairs)
            entities.append(tree2)
            entities.append(tree3)
            entities.append(tree4)
            entities.append(tree5)
            entities.append(tree6)
            entities.append(tree7)
            entities.append(tree8)
            entities.append(tree9)
            entities.append(tree10)
            entities.append(tree11)
            entities.append(tree12)
            entities.append(tree13)
            entities.append(tree14)
            entities.append(tree15)
            entities.append(tree16)
            entities.append(tree17)
            entities.append(tree18)
            entities.append(btree2)
            entities.append(btree3)
            entities.append(btree4)
            entities.append(btree5)
            entities.append(btree6)
            entities.append(btree7)
            entities.append(btree8)
            entities.append(btree9)
            entities.append(btree10)
            entities.append(btree11)
            entities.append(btree12)
            entities.append(btree13)
            entities.append(btree14)
            entities.append(btree15)
            entities.append(btree16)
            entities.append(btree17)
            entities.append(btree18)
            entities.append(ctree2)
            entities.append(ctree3)
            entities.append(ctree4)
            entities.append(ctree5)
            entities.append(ctree6)
            entities.append(ctree7)
            entities.append(ctree8)
            entities.append(ctree9)
            entities.append(ctree10)
            entities.append(ctree11)
            entities.append(ctree12)
            entities.append(ctree13)
            entities.append(ctree14)
            entities.append(ctree15)
            entities.append(ctree16)
            entities.append(ctree17)
            entities.append(ctree18)
            entities.append(dtree2)
            entities.append(dtree3)
            entities.append(dtree4)
            entities.append(dtree5)
            entities.append(dtree6)
            entities.append(dtree7)
            entities.append(dtree8)
            entities.append(dtree9)
            entities.append(dtree10)
            entities.append(dtree11)
            entities.append(dtree12)
            entities.append(dtree13)
            entities.append(dtree14)
            entities.append(dtree15)
            entities.append(dtree16)
            entities.append(dtree17)
            entities.append(dtree18)
            entities.append(ftree2)
            entities.append(ftree3)
            entities.append(ftree4)
            entities.append(ftree5)
            entities.append(ftree6)
            entities.append(ftree7)
            entities.append(ftree8)
            entities.append(ftree9)
            entities.append(ftree10)
            entities.append(ftree11)
            entities.append(ftree12)
            entities.append(ftree13)
            entities.append(ftree14)
            entities.append(ftree15)
            entities.append(ftree16)
            entities.append(ftree17)
            entities.append(ftree18)
            entities.append(sapling)
            entities.append(sapling2)
            entities.append(sapling3)
            entities.append(sapling4)
            entities.append(sapling5)
            entities.append(sapling6)
            entities.append(sapling7)
            entities.append(sapling8)
            entities.append(sapling9)
            entities.append(sapling10)
            entities.append(sapling11)
            entities.append(sapling12)
            entities.append(sapling13)
            entities.append(sapling14)
            entities.append(sapling15)
            entities.append(sapling16)
            entities.append(sapling17)
            entities.append(sapling18)
            entities.append(sapling19)
            entities.append(sapling20)
            entities.append(sapling21)
            entities.append(sapling22)
            entities.append(sapling23)
            entities.append(sapling24)
            entities.append(sapling25)
            entities.append(sapling26)
            for tile_y, line in enumerate(contents.split('\n')):
                for tile_x, tile_character in enumerate(line):
                    if tile_character == '.':
                        self.create_tile(tile_x,tile_y)
        elif self.dungeon_level == -1:
            p = open('village.txt')
            contents = p.read()
            center_of_last_room_x = None
            center_of_last_room_y = None
            player.x = 4
            player.y = 5
            stairs_component = Stairs(self.dungeon_level - 1,dungeon_stairs=True)
            down_stairs = Entity(4, 5, '>', libtcod.darker_green, 'Stairs back to the Caves',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            stairs_component = Stairs(self.dungeon_level - 1,red_cave_stairs=True)
            red_cave_stairs = Entity(17, 20, '>', libtcod.darker_red, 'Stairs to the Red Cave',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            stairs_component = Stairs(self.dungeon_level - 1, wyld_stairs=True)
            wyld_stairs = Entity(4, 20, '>', libtcod.darkest_green, 'Path to the Wyld',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            text_square_1 = Entity(29, 10, '*', libtcod.white, 'Tile with Writing',has_message=True,text_message_1='You see some writing on the ground. It says',text_message_2='Welcome to the Church of Havoc',text_message_3='May the God-Fae protect you from the mists of Chaos')
            text_square_2 = Entity(28, 10, '*', libtcod.white, 'Tile with Writing', has_message=True,
                                   text_message_1='You see some writing on the ground. It says',
                                   text_message_2='Welcome to the Church of Havoc',
                                   text_message_3='May the God-Fae protect you from the mists of Chaos')
            entities.append(text_square_1)
            entities.append(text_square_2)
            entities.append(down_stairs)
            entities.append(red_cave_stairs)
            entities.append(wyld_stairs)
            entities.append(leader)
            entities.append(bandit)
            entities.append(sprite_child_1)
            entities.append(sprite_child_2)
            entities.append(dapper_trashling)
            entities.append(fancy_trashling)
            entities.append(shy_giantess)
            entities.append(stressed_mother)
            entities.append(stressed_mother_2)
            entities.append(old_farmer)
            entities.append(old_farmer_2)
            entities.append(horned_cloudie)
            entities.append(horned_cloudie_2)
            entities.append(horned_cloudie_3)
            self.village = True
            for tile_y, line in enumerate(contents.split('\n')):
                for tile_x, tile_character in enumerate(line):
                    if tile_character == '.':
                        self.create_tile(tile_x,tile_y)
                    elif tile_character == '<':
                        self.create_tile(tile_x,tile_y)
                    elif tile_character =='>':
                        self.create_tile(tile_x, tile_y)
                        entities = [player]
        elif self.dungeon_level == 0:
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_maze_rooms):
            # random width and height
                w = randint(maze_min_size, maze_max_size)
                h = randint(maze_min_size, maze_max_size)
            # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                    self.create_room(new_room)

                # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                    # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                        # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_entities(new_room, entities)

                # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1
            stairs_component = Stairs(self.red_cave_level + 1, dungeon_stairs=True)
            down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)

            upstairs_component = Upstairs(self.red_cave_level + 1, dungeon_stairs=True)
            up_stairs = Entity(player.x, player.y, '<', libtcod.white, 'Stairs',
                               render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(up_stairs)

        else:
            self.village = False
            rooms = []
            num_rooms = 0

            center_of_last_room_x = None
            center_of_last_room_y = None

            for r in range(max_rooms):
            # random width and height
                w = randint(room_min_size, room_max_size)
                h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
                x = randint(0, map_width - w - 1)
                y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                    self.create_room(new_room)

                # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                    # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                    else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                        if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                        # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y,  new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)



                    self.place_entities(new_room, entities)

                # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1
            stairs_component = Stairs(self.red_cave_level + 1,dungeon_stairs=True)
            down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                                render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)

            upstairs_component = Upstairs(self.red_cave_level + 1,dungeon_stairs=True)
            up_stairs = Entity(player.x, player.y, '<', libtcod.white, 'Stairs',
                                render_order=RenderOrder.UPSTAIRS, upstairs=upstairs_component)
            entities.append(up_stairs)

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_hexagon(self, room,map_width,map_height):
        ymid = (room.y1 + room.y2) // 2
        for y in range(room.y1 + 1, room.y2):
            extra_width = int((ymid - room.y1) - abs(ymid - y))
            for x in range(room.y1 + 1 + extra_width, room.y2):
                if (map_width > x >= 0) and (map_height > y >= 0):
                    self.tiles[y][x].blocked = False
                    self.tiles[y][x].block_sight = False
                else:
                    self.tiles[y][x].blocked = True
                    self.tiles[y][x].block_sight = True

    def create_honeycomb(self, room,map_width,map_height):
        ymid = (room.y1 + room.y2) // 2
        for y in range(room.y1 + 1, room.y2):
            extra_width = int((ymid - room.y1) - abs(ymid - y))
            for x in range(room.y1 + 1 - extra_width, room.y2 + 1):
                if (map_width > x >= 0) and (map_height > y >= 0):
                    self.tiles[y][x].blocked = False
                    self.tiles[y][x].block_sight = False
                else:
                    self.tiles[y][x].blocked = True
                    self.tiles[y][x].block_sight = True


    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_moth_cave_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([ [1, 0],[2, 1], [3, 4], [5, 6]], self.moth_cave_level)
        max_items_per_room = from_dungeon_level([[0, 0], [3, 1]], self.moth_cave_level)
        min_items_per_room = from_dungeon_level([[1, 0]], self.moth_cave_level)

        # Get a random number of monsters
        number_of_monsters = randint(1, max_monsters_per_room)

        # Get a random number of items
        number_of_items = randint(0, max_items_per_room)
        monster_chances = {
                'stalker': from_dungeon_level([[5, 1]], self.moth_cave_level),
                'maiden': from_dungeon_level([[5, 1]], self.moth_cave_level),
                'mistmaiden': from_dungeon_level([[6, 1]], self.moth_cave_level)}

        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level([[10, 1]], self.moth_cave_level),
            'shield': from_dungeon_level([[15, 8]], self.moth_cave_level),
            'lance': from_dungeon_level([[15, 3]], self.moth_cave_level),
            'rbrace': from_dungeon_level([[15, 3]], self.moth_cave_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.moth_cave_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.moth_cave_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.moth_cave_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check if an entity is already in that location
            if not any([entity for entity in entities if entity.x == x and entity.y == y]) and self.tiles[x][y].blocked is False:
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':
                        fighter_component = Fighter(hp=10, defense=2, power=4, xp=100, agility=4,mana = 0,base_psyche = 0,attack_dice_minimum=2,attack_dice_maximum=6,ac=2,will=5,talk_message = 'The Striker-Moth screeches horribly!')
                        ai_component = BasicMonster()
                        food_component = Item(use_function=eat,amount=15,eat_message='You eat the Striker-Moth! Bleh! It\'s slimy!')

                        monster = Entity(x, y, 'm', libtcod.desaturated_green, 'Striker-Moth', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'stalker':
                        fighter_component = Fighter(hp=20, defense=2, power=4, xp=5000, agility=1, mana=0, base_psyche=0,attack_dice_minimum=1, attack_dice_maximum=4, ac=0, will=0)
                        food_component = Item(use_function=eat, amount=60,
                                              eat_message='You eat the Hunger-Moth. Tastes like chicken!')
                        ai_component = HungerMonster()

                        monster = Entity(x, y, 'm', libtcod.red, 'Hunger-Moth', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'maiden':
                        fighter_component = Fighter(hp=5, defense=2, power=5, xp=5000, agility=1, mana=0, base_psyche=0,
                                                attack_dice_minimum=1, attack_dice_maximum=4, ac=0, will=3)
                        food_component = Item(use_function=eat, amount=-50,
                        eat_message='You eat the Vomit-Moth. You vomit! What did you think was going to happen you moron!')
                        ai_component = PoisonMonster()

                        monster = Entity(x, y, 'm', libtcod.lighter_yellow, 'Vomit-Moth', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'mistmaiden':
                        fighter_component = Fighter(hp=5, defense=2, power=5, xp=5000, agility=1, mana=0, base_psyche=0,
                                                attack_dice_minimum=1, attack_dice_maximum=4, ac=5, will=3,talk_message = 'hi')
                        food_component = Item(use_function=eat, amount= 60,
                                              eat_message='You eat the Speedy-Spider! Mmmm! Nice and tangy!')
                        ai_component = HasteSelfMonster()

                        monster = Entity(x, y, 's', libtcod.darker_blue, 'Speedy-Spider', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1, room.x2)
            y = randint(room.y1, room.y2)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]) and self.tiles[x][y].blocked is False:
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND and EquipmentSlots.OFF_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.white, 'Sword', equippable=equippable_component,item=item_component)
                elif item_choice == 'lance':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=6, defense_bonus=-5)
                    item_component = Item(use_function=None)
                    item = Entity(x, y, '/', libtcod.white, 'Lance', equippable=equippable_component,item=item_component)
                elif item_choice == 'shield':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component,item=item_component)
                elif item_choice == 'rbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.black, 'Right Bracelet of Defense', equippable=equippable_component,item=item_component)
                elif item_choice == 'rlightbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=1, agility_bonus=-1,)
                    item = Entity(x, y, '[', libtcod.black, 'Rotten Right Bracelet',
                                  equippable=equippable_component,item=item_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, '?', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    item = Entity(x, y, '?', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '?', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(use_function=throw_shurikin, damage=20, maximum_range=10)
                    item = Entity(x, y, '+', libtcod.gray, 'Shuriken', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

    def place_bee_nest_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([ [1, 0],[5, 1], [5, 4], [5, 6]], self.bees_nest_level)
        max_items_per_room = from_dungeon_level([[0, 0], [3, 1]], self.bees_nest_level)
        min_items_per_room = from_dungeon_level([[1, 0]], self.bees_nest_level)

        # Get a random number of monsters
        number_of_monsters = randint(1, max_monsters_per_room)

        # Get a random number of items
        number_of_items = randint(0, max_items_per_room)
        monster_chances = {
                'orc': from_dungeon_level([[5, 2]], self.bees_nest_level),
                'mage': from_dungeon_level([[4, 2]], self.bees_nest_level),
                'stalker': from_dungeon_level([[5, 1]], self.bees_nest_level),
                'maiden': from_dungeon_level([[5, 1]], self.bees_nest_level),
                'mistmaiden': from_dungeon_level([[6, 1]], self.bees_nest_level)}

        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level([[10, 1]], self.bees_nest_level),
            'shield': from_dungeon_level([[15, 8]], self.bees_nest_level),
            'lance': from_dungeon_level([[15, 3]], self.bees_nest_level),
            'rbrace': from_dungeon_level([[15, 3]], self.bees_nest_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.bees_nest_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.bees_nest_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.bees_nest_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check if an entity is already in that location
            if not any([entity for entity in entities if entity.x == x and entity.y == y]) and self.tiles[x][y].blocked is False:
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':
                        fighter_component = Fighter(hp=10, defense=2, power=4, xp=100, agility=4,mana = 0,base_psyche = 0,attack_dice_minimum=2,attack_dice_maximum=6,ac=2,will=5,talk_message = 'The Striker-Moth screeches horribly!')
                        ai_component = BeeSpawnerMonster()
                        food_component = Item(use_function=eat,amount=15,eat_message='You eat the Bee-Princess! Bleh! It\'s slimy!')

                        monster = Entity(x, y, 'b', libtcod.light_pink, 'Bee-Princess', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'stalker':
                        fighter_component = Fighter(hp=20, defense=2, power=4, xp=50, agility=1, mana=0, base_psyche=0,attack_dice_minimum=1, attack_dice_maximum=4, ac=0, will=0)
                        food_component = Item(use_function=eat_poison, amount=-30,
                                              eat_message='You eat the Soldier-Bee. Agh its poisonous!')
                        ai_component = PoisonMonster()

                        monster = Entity(x, y, 'b', libtcod.lighter_green, 'Soldier-Bee', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'maiden':
                        fighter_component = Fighter(hp=5, defense=2, power=5, xp=5000, agility=1, mana=0, base_psyche=0,
                                                attack_dice_minimum=1, attack_dice_maximum=4, ac=0, will=3)
                        food_component = Item(use_function=eat, amount=5,
                        eat_message='You eat the Worker-Bee. It tastes very bland.')
                        ai_component = BasicMonster()

                        monster = Entity(x, y, 'b', libtcod.yellow, 'Worker-bee', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'mistmaiden':
                        fighter_component = Fighter(hp=5, defense=2, power=5, xp=5000, agility=1, mana=0, base_psyche=0,
                                                attack_dice_minimum=1, attack_dice_maximum=4, ac=5, will=3,talk_message = 'hi',stealthed=1)
                        food_component = Item(use_function=eat, amount= 60,
                                              eat_message='You eat the Drone-Bee Rogue! Mmmm! Nice and tangy!')
                        ai_component = BasicMonster()

                        monster = Entity(x, y, 'b', libtcod.darker_yellow, 'Drone-Bee Rogue', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'mage':
                    fighter_component = Fighter(hp=5, defense=2, power=5, xp=5000, agility=1, mana=0, base_psyche=0,
                                                attack_dice_minimum=1, attack_dice_maximum=4, ac=5, will=3,
                                                talk_message='hi')
                    food_component = Item(use_function=eat, amount=60,
                                          eat_message='You eat the Speedy-Spider! Mmmm! Nice and tangy!')
                    ai_component = MagicAttackMonster()

                    monster = Entity(x, y, 'b', libtcod.darker_blue, 'Drone-Bee Mage', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                     item=food_component)

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1, room.x2)
            y = randint(room.y1, room.y2)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]) and self.tiles[x][y].blocked is False:
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND and EquipmentSlots.OFF_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.white, 'Sword', equippable=equippable_component,item=item_component)
                elif item_choice == 'lance':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=6, defense_bonus=-5)
                    item_component = Item(use_function=None)
                    item = Entity(x, y, '/', libtcod.white, 'Lance', equippable=equippable_component,item=item_component)
                elif item_choice == 'shield':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component,item=item_component)
                elif item_choice == 'rbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.black, 'Right Bracelet of Defense', equippable=equippable_component,item=item_component)
                elif item_choice == 'rlightbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=1, agility_bonus=-1,)
                    item = Entity(x, y, '[', libtcod.black, 'Rotten Right Bracelet',
                                  equippable=equippable_component,item=item_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, '?', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    item = Entity(x, y, '?', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '?', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(use_function=throw_shurikin, damage=20, maximum_range=10)
                    item = Entity(x, y, '+', libtcod.gray, 'Shuriken', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([ [1, 0],[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[0, 0], [3, 1]], self.dungeon_level)
        min_items_per_room = from_dungeon_level([[1, 0]], self.dungeon_level)

        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        # Get a random number of items
        number_of_items = randint(0, max_items_per_room)
        monster_chances = {
                'orc': 20,
                'maiden': from_dungeon_level([[5, 6], [10, 5], [1, 7]], self.moth_cave_level),
                'mistmaiden': from_dungeon_level([[4, 1], [10, 5], [1, 7]], self.moth_cave_level),
                'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.moth_cave_level),
                'stalker': from_dungeon_level([[15, 3], [30, 5], [60, 7]],self.moth_cave_level),
                'fairy': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.moth_cave_level),
                'slime': from_dungeon_level([[20, 3], [30, 5], [60, 7]], self.moth_cave_level),
                'shrub': from_dungeon_level([[15, 0],[0, 1]], self.moth_cave_level),
                'stone': from_dungeon_level([[5, 2], [10, 4]], self.moth_cave_level)}



        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level([[10, 1]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'lance': from_dungeon_level([[15, 3]], self.dungeon_level),
            'rbrace': from_dungeon_level([[15, 3]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check if an entity is already in that location
            if not any([entity for entity in entities if entity.x == x and entity.y == y]) and self.tiles[x][y].blocked is False:
                monster_choice = random_choice_from_dict(monster_chances)
                if self.dungeon_level >= 0:

                    if monster_choice == 'orc':
                        fighter_component = Fighter(hp=20, defense=2, power=5, xp=5000, agility=1,mana = 0,base_psyche = 0,attack_dice_minimum=1,attack_dice_maximum=4,ac=0,will=0,talk_message = 'hiya')
                        ai_component = BasicMonster()
                        inventory_component = Inventory(26)
                        food_component = Item(use_function=eat,amount=30,eat_message='You eat the Orc! It tastes like graphite.')

                        monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component,inventory=inventory_component)
                    elif monster_choice == 'stalker':
                        fighter_component = Fighter(hp=5, defense=2, power=5, xp=5000, agility=1, mana=0, base_psyche=0,attack_dice_minimum=1, attack_dice_maximum=4, ac=0, will=0,stealthed=1)
                        food_component = Item(use_function=eat, amount=0,
                                              eat_message='You eat the Stalker. It feels like eating air')
                        ai_component = BasicMonster()

                        monster = Entity(x, y, '@', libtcod.gray, 'Invisible Stalker', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                    elif monster_choice == 'maiden':
                        fighter_component = Fighter(hp=5, defense=2, power=5, xp=5000, agility=1, mana=0, base_psyche=0,
                                                attack_dice_minimum=1, attack_dice_maximum=4, ac=0, will=3)
                        food_component = Item(use_function=eat, amount=-50,
                        eat_message='You vomit! You\'re stomach feels like its exploding!')
                        ai_component = SleepMonster()

                        monster = Entity(x, y, '@', libtcod.lighter_yellow, 'Blinding Maiden', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                    elif monster_choice == 'mistmaiden':
                        fighter_component = Fighter(hp=5, defense=2, power=5, xp=5000, agility=1, mana=0, base_psyche=0,
                                                attack_dice_minimum=1, attack_dice_maximum=4, ac=5, will=3,talk_message = 'hi')
                        food_component = Item(use_function=eat, amount=-50,
                                              eat_message='You vomit! You\'re stomach feels like its exploding!')
                        ai_component = HasteSelfMonster()

                        monster = Entity(x, y, '@', libtcod.darker_blue, 'Mist Maiden', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                    elif monster_choice == 'troll':
                        fighter_component = Fighter(hp=50, defense=3, power=6, xp=100, agility=1,mana = 0,base_psyche = 0,attack_dice_minimum=1,attack_dice_maximum=8,ac= -3,will=2)
                        food_component = Item(use_function=eat, amount=50,
                                              eat_message='What a filling meal!')
                        ai_component = BasicMonster()

                        monster = Entity(x, y, 'T', libtcod.darker_green, 'Cave Troll', blocks=True, fighter=fighter_component,item=food_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                    elif monster_choice == 'stone':
                        fighter_component = Fighter(hp=10, defense=25, power=8, xp=160, agility= -1,mana = 0,base_psyche = 0,attack_dice_minimum=1,attack_dice_maximum=2,ac= -3,will=0)
                        food_component = Item(use_function=eat, amount=-50,
                                              eat_message='Agh! You vomit trying to swallow rocks!')
                        ai_component = BasicMonster()

                        monster = Entity(x, y, 'G', libtcod.gray, 'Stone Golem', blocks=True, fighter=fighter_component,item=food_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                    elif monster_choice == 'slime':
                        fighter_component = Fighter(hp=10, defense=25, power=8, xp=160, agility= 2,mana = 0,base_psyche = 0,attack_dice_minimum=1,attack_dice_maximum=8,ac=1,will=1)
                        food_component = Item(use_function=eat, amount=10,
                                              eat_message='That was a very slimy meal.')
                        ai_component = SlimeMonster()

                        monster = Entity(x, y, 's', libtcod.green, 'Slime', blocks=True, fighter=fighter_component,item=food_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                    elif monster_choice == 'shrub':
                        fighter_component = Fighter(hp=10, defense=0, power=5, xp=160, agility= 3,mana = 0,base_psyche = 0,attack_dice_minimum=4,attack_dice_maximum=8,ac=-15,will=0)
                        food_component = Item(use_function=eat, amount=-10,
                                              eat_message='Agh that hurts! You choke on the thorns')
                        ai_component = ShrubMonster(closest_distance=5)

                        monster = Entity(x, y, '"', libtcod.desaturated_green, 'Thorn-Shrub', blocks=True, fighter=fighter_component,item=food_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                    else:
                        fighter_component = Fighter(hp=10, defense=1, power=2, xp=100, agility=4,mana = 0,base_psyche = 0,attack_dice_minimum=1,attack_dice_maximum=2,ac=10,will=0)
                        food_component = Item(use_function=eat, amount= 60,
                                              eat_message='That was a very fizzy meal!')
                        ai_component = BasicMonster()

                        monster = Entity(x, y, 'f', libtcod.black, 'Fairy', blocks=True,fighter=fighter_component,item=food_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)




                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1, room.x2)
            y = randint(room.y1, room.y2)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]) and self.tiles[x][y].blocked is False:
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND and EquipmentSlots.OFF_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.white, 'Sword', equippable=equippable_component,item=item_component)
                elif item_choice == 'lance':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=6, defense_bonus=-5)
                    item_component = Item(use_function=None)
                    item = Entity(x, y, '/', libtcod.white, 'Lance', equippable=equippable_component,item=item_component)
                elif item_choice == 'shield':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component,item=item_component)
                elif item_choice == 'rbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.black, 'Right Bracelet of Defense', equippable=equippable_component,item=item_component)
                elif item_choice == 'rlightbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=1, agility_bonus=-1,)
                    item = Entity(x, y, '[', libtcod.black, 'Rotten Right Bracelet',
                                  equippable=equippable_component,item=item_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, '?', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    item = Entity(x, y, '?', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '?', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(use_function=throw_shurikin, damage=20, maximum_range=10)
                    item = Entity(x, y, '+', libtcod.gray, 'Shuriken', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

    def place_red_cave_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([ [1, 0],[2, 1], [3, 4], [5, 6]], self.red_cave_level)
        max_items_per_room = from_dungeon_level([[0, 0], [3, 1]], self.red_cave_level)
        min_items_per_room = from_dungeon_level([[1, 0]], self.red_cave_level)

        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        # Get a random number of items
        number_of_items = randint(0, max_items_per_room)
        monster_chances = {
                'trash': from_dungeon_level([[5, 1], [6, 2], [2, 3]], self.red_cave_level),
                'trashwizard': from_dungeon_level([[1, 1], [3, 2], [6, 3]], self.red_cave_level),
                'mole': from_dungeon_level([[0, 1], [3, 2], [6, 3]], self.red_cave_level),
                'turret': from_dungeon_level([[3, 1], [5, 5], [8, 3]], self.red_cave_level)}



        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level([[10, 1]], self.red_cave_level),
            'shield': from_dungeon_level([[15, 8]], self.red_cave_level),
            'lance': from_dungeon_level([[15, 3]], self.red_cave_level),
            'rbrace': from_dungeon_level([[15, 3]], self.red_cave_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.red_cave_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.red_cave_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.red_cave_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check if an entity is already in that location
            if not any([entity for entity in entities if entity.x == x and entity.y == y]) and self.tiles[x][y].blocked is False:
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'trash':
                        fighter_component = Fighter(hp=20, defense=2, power=5, xp=100, agility=1,mana = 0,base_psyche = 0,attack_dice_minimum=2,attack_dice_maximum=6,ac=3,will=3,talk_message = 'The Trash Bandit screeches')
                        ai_component = BasicMonster()
                        food_component = Item(use_function=eat, amount=25,
                                              eat_message='That meal tastes like trash!.')

                        monster = Entity(x, y, 't', libtcod.desaturated_green, 'Trash Bandit', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'trashwizard':
                        fighter_component = Fighter(hp=15, defense=2, power=5, xp=100, agility=1, mana=0, base_psyche=0,attack_dice_minimum=1, attack_dice_maximum=3, ac=0, will=0,stealthed=0,talk_message='The Trash Bandit screeches')
                        ai_component = SleepMonster()
                        food_component = Item(use_function=eat_cursed, amount=25,
                                              eat_message='You feel truly c u r s e d.')

                        monster = Entity(x, y, 't', libtcod.gray, 'Trash Bandit Witchdoctor', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'mole':
                        fighter_component = Fighter(hp=5, defense=2, power=5, xp=100, agility=1, mana=0, base_psyche=0,
                                                attack_dice_minimum=1, attack_dice_maximum=5, ac=4, will= -1, stealthed=0,
                                                talk_message='The Fuzzy-Screecher screams and giggles')
                        ai_component = HasteSelfMonster()
                        food_component = Item(use_function=eat, amount=25,
                                              eat_message='You feel like your stomach is doing donuts.')

                        monster = Entity(x, y, 's', libtcod.darker_amber, 'Fuzzy-Screecher', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,item=food_component)
                elif monster_choice == 'turret':
                        fighter_component = Fighter(hp=10, defense=1, power=2, xp=100, agility=4,mana = 0,base_psyche = 0,attack_dice_minimum=1,attack_dice_maximum=2,ac=10,will=0,talk_message='The Bone Turret whirrs loudly')
                        food_component = Item(use_function=eat, amount= 5,
                                              eat_message='Turns out bone shavings aren\'t very filling. Who would have guessed?')
                        ai_component = ShrubMonster(closest_distance=5)

                        monster = Entity(x, y, 'T', libtcod.white, 'Bone Turret', blocks=True,fighter=fighter_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component,item=food_component)




                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1, room.x2)
            y = randint(room.y1, room.y2)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]) and self.tiles[x][y].blocked is False:
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND and EquipmentSlots.OFF_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.white, 'Sword', equippable=equippable_component,item=item_component)
                elif item_choice == 'lance':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=6, defense_bonus=-5)
                    item_component = Item(use_function=None)
                    item = Entity(x, y, '/', libtcod.white, 'Lance', equippable=equippable_component,item=item_component)
                elif item_choice == 'shield':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component,item=item_component)
                elif item_choice == 'rbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=4, agility_bonus =-3)
                    item = Entity(x, y, '[', libtcod.black, 'Right Bracelet of Defense', equippable=equippable_component,item=item_component)
                elif item_choice == 'rlightbrace':
                    item_component = Item(use_function=None)
                    equippable_component = Equippable(EquipmentSlots.RIGHT_BRACELET, defense_bonus=1, agility_bonus=-1,)
                    item = Entity(x, y, '[', libtcod.black, 'Rotten Right Bracelet',
                                  equippable=equippable_component,item=item_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, '?', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    item = Entity(x, y, '?', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '?', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(use_function=throw_shurikin, damage=20, maximum_range=10)
                    item = Entity(x, y, '+', libtcod.gray, 'Shuriken', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

    def place_tile_entities(self, x,y,entities, entity):
        entities.append(entity)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))


        for entity in entities:
            if entity.upstairs:
                entity.x = player.x
                entity.y = player.y


        return entities

    def go_to_wyld(self, player, message_log, constants):
        self.wyld = True
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))


        return entities

    def leave_wyld(self, player, message_log, constants):
        self.wyld = False
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))


        return entities

    def next_red_cave_floor(self, player, message_log, constants):
        self.red_cave_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        for entity in entities:
            if entity.upstairs:
                entity.x = player.x
                entity.y = player.y

        return entities

    def next_bee_nest_floor(self, player, message_log, constants):
        self.wyld = False
        self.bees_nest_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        for entity in entities:
            if entity.upstairs:
                entity.x = player.x
                entity.y = player.y

        return entities
    def next_moth_cave_floor(self, player, message_log, constants):
        self.wyld = False
        self.moth_cave_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        for entity in entities:
            if entity.upstairs:
                entity.x = player.x
                entity.y = player.y

        return entities

    def previous_moth_cave_floor(self, player, message_log, constants):
        self.wyld = False
        self.moth_cave_level -= 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        for entity in entities:
            for stairs in entities:
                if entity.upstairs and stairs.stairs:
                    entity.x = stairs.x
                    entity.y = stairs.y

        for entity in entities:
            if entity.stairs:
                entity.x = player.x
                entity.y = player.y


        return entities

    def leave_moth_cave(self, player, message_log, constants):
        self.wyld = True
        self.moth_cave_level = 0
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        player.x = 30
        player.y = 15

        return entities
    def leave_bees_nest(self, player, message_log, constants):
        self.wyld = True
        self.bees_nest_level = 0
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        libtcod.console_flush()
        libtcod.console_clear(constants)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        player.x = 3
        player.y = 4

        return entities
    def previous_floor(self, player, message_log, constants):
        self.dungeon_level -= 2
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'],player, entities,)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        for entity in entities:
            for stairs in entities:
                if entity.upstairs and stairs.stairs and self.dungeon_level != -1:
                    entity.x = stairs.x
                    entity.y = stairs.y

        for entity in entities:
            if entity.stairs and self.dungeon_level != -1:
                entity.x = player.x
                entity.y = player.y


        return entities
    def leave_red_cave(self, player, message_log, constants):
        self.dungeon_level = -1
        self.red_cave_level = 0
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'],player, entities,)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        player.x = 17
        player.y = 20

        return entities
    def previous_red_cave_floor(self, player, message_log, constants):
        self.dungeon_level = 0
        self.red_cave_level -= 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['max_maze_rooms'], constants['maze_min_size'], constants['maze_max_size'],
                      constants['map_width'], constants['map_height'],player, entities,)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        for entity in entities:
            for stairs in entities:
                if entity.upstairs and stairs.stairs:
                    entity.x = stairs.x
                    entity.y = stairs.y

        for entity in entities:
            if entity.stairs:
                entity.x = player.x
                entity.y = player.y

        return entities
