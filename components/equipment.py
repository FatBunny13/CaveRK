from equipment_slots import EquipmentSlots


class Equipment:
    def __init__(self, main_hand=None, use_function=None, off_hand=None, left_bracelet=None, right_bracelet=None, targeting=False,armour=None, targeting_message=None, **kwargs):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.right_bracelet = right_bracelet
        self.left_bracelet = left_bracelet
        self.armour = armour
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        if self.armour and self.off_hand.equippable:
            bonus += self.armour.equippable.max_hp_bonus

        if self.right_bracelet and self.right_bracelet.equippable:
            bonus += self.right_bracelet.equippable.max_hp_bonus

        if self.left_bracelet and self.left_bracelet.equippable:
            bonus += self.left_bracelet.equippable.max_hp_bonus

        return bonus

    @property
    def weapon_damage(self):
        weapon_damage = 0

        if self.main_hand and self.main_hand.equippable:
           weapon_damage = self.main_hand.equippable.damage

        return weapon_damage

    @property
    def psyche_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.psyche_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.psyche_bonus

        if self.armour and self.off_hand.equippable:
            bonus += self.armour.equippable.psyche_bonus

        if self.right_bracelet and self.right_bracelet.equippable:
            bonus += self.right_bracelet.equippable.psyche_bonus

        if self.left_bracelet and self.left_bracelet.equippable:
            bonus += self.left_bracelet.equippable.psyche_bonus

        return bonus

    @property
    def max_mana_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_mana_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_mana_bonus

        if self.armour and self.off_hand.equippable:
            bonus += self.armour.equippable.max_mana_bonus

        if self.right_bracelet and self.right_bracelet.equippable:
            bonus += self.right_bracelet.equippable.max_mana_bonus

        if self.left_bracelet and self.left_bracelet.equippable:
            bonus += self.left_bracelet.equippable.max_mana_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        if self.armour and self.off_hand.equippable:
            bonus += self.armour.equippable.power_bonus

        if self.right_bracelet and self.right_bracelet.equippable:
            bonus += self.right_bracelet.equippable.power_bonus

        if self.left_bracelet and self.left_bracelet.equippable:
            bonus += self.left_bracelet.equippable.power_bonus

        return bonus

    @property
    def agility_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.agility_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.agility_bonus

        if self.armour and self.off_hand.equippable:
            bonus += self.armour.equippable.agility_bonus

        if self.right_bracelet and self.right_bracelet.equippable:
            bonus += self.right_bracelet.equippable.agility_bonus

        if self.left_bracelet and self.left_bracelet.equippable:
            bonus += self.left_bracelet.equippable.agility_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        if self.armour and self.off_hand.equippable:
            bonus += self.armour.equippable.defense_bonus

        if self.right_bracelet and self.right_bracelet.equippable:
            bonus += self.right_bracelet.equippable.defense_bonus

        if self.left_bracelet and self.left_bracelet.equippable:
            bonus += self.left_bracelet.equippable.defense_bonus

        return bonus

    @property
    def ac_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.ac_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.ac_bonus

        if self.armour and self.off_hand.equippable:
            bonus += self.armour.equippable.ac_bonus

        if self.right_bracelet and self.right_bracelet.equippable:
            bonus += self.right_bracelet.equippable.ac_bonus

        if self.left_bracelet and self.left_bracelet.equippable:
            bonus += self.left_bracelet.equippable.ac_bonus

        return bonus

    @property
    def will_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.will_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.will_bonus

        if self.armour and self.off_hand.equippable:
            bonus += self.armour.equippable.will_bonus

        if self.right_bracelet and self.right_bracelet.equippable:
            bonus += self.right_bracelet.equippable.will_bonus

        if self.left_bracelet and self.left_bracelet.equippable:
            bonus += self.left_bracelet.equippable.will_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'unequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'unequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.RIGHT_BRACELET:
            if self.right_bracelet == equippable_entity:
                self.right_bracelet = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.right_bracelet:
                    results.append({'unequipped': self.off_hand})

                self.right_bracelet = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.LEFT_BRACELET:
            if self.left_bracelet == equippable_entity:
                self.left_bracelet = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.left_bracelet:
                    results.append({'unequipped': self.off_hand})

                self.left_bracelet = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.ARMOUR:
            if self.armour == equippable_entity:
                self.armour = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.armour:
                    results.append({'unequipped': self.armour})

                self.armour = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
