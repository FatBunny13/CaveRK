class Equippable:
    def __init__(self, slot, use_function=None, minimum_hit_dice=0,maximum_hit_dice=0,ac_bonus=0,will_bonus=0, power_bonus=0,psyche_bonus=0,max_mana_bonus=0, defense_bonus=0, max_hp_bonus=0, agility_bonus=0):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.agility_bonus = agility_bonus
        self.max_mana_bonus = max_mana_bonus
        self.psyche_bonus = psyche_bonus
        self.ac_bonus = ac_bonus
        self.will_bonus = will_bonus
        self.minimum_hit_dice = minimum_hit_dice
        self.maximum_hit_dice = maximum_hit_dice
