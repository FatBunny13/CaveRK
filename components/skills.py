import libtcodpy as libtcod
from dataclasses import dataclass, field
from typing import List
from game_messages import Message




class Skills:

    def __init__(self, capacity):

        self.capacity = int(capacity)
        self.skill_list = list()

    def add_skill(self, skill):
        results = list()
        if( len(self.skill_list) >= self.capacity):
            results.append({
                'item_added': None,
                'message': Message('You cannot learn anymore skills.', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': skill,
                'message': Message('You have learned the skill {0}!'.format(skill.name), libtcod.blue)
            })

            self.skill_list.append(skill)

        return results

    def use(self, skill_entity, **kwargs):
        results = []

        skill_component = skill_entity.skill

        if skill_component.use_function is None:
            results.append({'message': Message('You cannot use that skill.'.format(skill_entity.name), libtcod.yellow)})
        else:
            if skill_component.skill_targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'skill_targeting': skill_entity})
            else:
                kwargs = {**skill_component.function_kwargs, **kwargs}
                skill_use_results = skill_component.use_function(self.owner, **kwargs)

                for skill_use_result in skill_use_results:
                    if skill_use_result.get('used'):
                       self.remove_skill(skill_entity)

                    results.extend(skill_use_results)

        return results

    def remove_skill(self, item):
        pass