import libtcodpy as libtcod

from game_messages import Message

class Quests:
    def __init__(self, quest_max):
        self.quest_max = quest_max
        self.quests = []

    def add_quest(self, quest):
        results = []

        if len(self.quests) >= self.quest_max:
            results.append({
                'item_added': None,
                'message': Message('You cannot do this quest. Finish some of your others.', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': quest,
                'message': Message('You have started the quest!'.format(quest.name), libtcod.blue)
            })

            self.quests.append(quest)

        return results

    def remove_quest(self, quest):
        self.quests.remove(quest)