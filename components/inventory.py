import libtcodpy as libtcod

from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', libtcod.yellow)
            })
        elif item and item.upstairs:
            results.append({
                'item_added': item,
                'message': Message('You cannot pick that up.'.format(item.name), libtcod.blue)
            })

        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name), libtcod.blue)
            })

            self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity

        if item_component.equippable:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {0} cannot be used'.format(item_entity.name), libtcod.yellow)})
        else:
            if item_component.item.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.item.function_kwargs, **kwargs}
                item_use_results = item_component.item.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def apply(self, item_entity, **kwargs):
        results = []

        item_component = item_entity

        if item_component.equippable:
            if item_component.item.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            elif item_component.item.use_function == None:
                results.append({'consumed': True, 'message': Message('You cannot use this item', libtcod.green)})
            else:
                kwargs = {**item_component.item.function_kwargs, **kwargs}
                item_use_results = item_component.item.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):

                        results.extend(item_use_results)
        else:
            if item_component.item.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.item.function_kwargs, **kwargs}
                item_use_results = item_component.item.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                        results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item or self.owner.equipment.right_bracelet == item or self.owner.equipment.left_bracelet == item:
            self.owner.equipment.toggle_equip(item)


        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name),
                                                                 libtcod.yellow)})

        return results
