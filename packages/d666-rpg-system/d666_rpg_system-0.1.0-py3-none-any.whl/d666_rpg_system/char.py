import random
from typing import Dict, List

from d666_rpg_system.data import (
    SKILLS,
    EXTRAORDINARY_ABILITIES,
    BACKGROUNDS,
    BASE_EQUIPMENT,
    CLOTHING_ITEMS,
    EQUIPMENT_A,
    EQUIPMENT_B,
    EQUIPMENT_C,
    LIGHT_MELEE_WEAPONS,
    HEAVY_MELEE_WEAPONS,
    RANGED_WEAPONS,
    SPELLS,
)


class D666Character:
    """Yeah."""

    def __init__(self, level: int = 1) -> None:
        self.name: str = ""
        self.level: int = level
        self.hit_points: int = 3
        self.skills_count: int = 2
        self.extraordinary_abilities_count: int = 1
        self.level_abilities()
        self.skills: List[Dict[str, str]] = self.get_skills()
        self.extraordinary_abilities: List[Dict[str, str]] = self.get_extraordinary_abilities()
        self.special_ea_rules()
        self.weapon: str = self.get_weapon()
        self.equipment: List[str] = self.get_equipment()
        self.background: str = self.get_background()
        self.spells: List[Dict[str, str]] = self.get_spells()
        self.money: str = self.get_money()

    def level_abilities(self):
        """For each level above 1st, get additional hp, skills, or extraordinary abilities."""
        level_ups = ["hp", "sk", "ea"]
        for _ in range(self.level - 1):
            level_up = random.choices(level_ups, weights=[3, 2, 1])[0]
            if level_up == "hp":
                self.hit_points += 1
            elif level_up == "sk":
                self.skills_count += 1
            elif level_up == "ea":
                self.extraordinary_abilities_count += 1
            else:
                raise Exception(f"Unexpected value for level_up: {level_up}")

    def get_skills(self):
        _skills = random.sample(SKILLS, k=self.skills_count)
        return _skills

    def get_extraordinary_abilities(self):
        _extraordinary_abilities = random.sample(
            EXTRAORDINARY_ABILITIES,
            k=self.extraordinary_abilities_count,
        )
        return _extraordinary_abilities

    def special_ea_rules(self):
        """Check for special rules."""
        ea_keys = [list(ea.keys())[0] for ea in self.extraordinary_abilities]
        self.has_wizardry = "Wizardry" in ea_keys
        self.has_weapon_training = "Weapon Training" in ea_keys
        self.check_for_weapon_training()
        self.get_spells()

    def check_for_weapon_training(self):
        """Check if character has the 'Weapon Training' extraordinary ability."""
        self.trained_weapon = None
        if self.has_weapon_training:
            self.trained_weapon = random.choice(
                [
                    "Unarmed",
                    "Light Melee",
                    "Heavy Melee",
                    "Ranged",
                ]
            )
        for ea in self.extraordinary_abilities:
            if list(ea.keys())[0] == "Weapon Training":
                ea[f"Weapon Training ({self.trained_weapon})"] = ea.pop("Weapon Training")
                ea[
                    f"Weapon Training ({self.trained_weapon})"
                ] = f"You make {self.trained_weapon} combat checks as skilled."

    def get_weapon(self):
        if self.has_weapon_training:
            if self.trained_weapon == "Light Melee":
                weapon = random.choice(LIGHT_MELEE_WEAPONS)
            elif self.trained_weapon == "Heavy Melee":
                weapon = random.choice(HEAVY_MELEE_WEAPONS)
            elif self.trained_weapon == "Ranged":
                weapon = random.choice(RANGED_WEAPONS)
            elif self.trained_weapon == "Unarmed":
                weapon = "Unarmed"
        else:
            weapon = random.choice(LIGHT_MELEE_WEAPONS + HEAVY_MELEE_WEAPONS + RANGED_WEAPONS)
        return weapon

    def get_equipment(self):
        """Base equipment plus one item from each list."""
        equipment = []
        equipment.extend(BASE_EQUIPMENT)
        for items in [
            CLOTHING_ITEMS,
            EQUIPMENT_A,
            EQUIPMENT_B,
            EQUIPMENT_C,
        ]:
            equipment.append(random.choice(items))
        return equipment

    def get_background(self):
        """Select a random background."""
        return random.choice(BACKGROUNDS)

    def get_spells(self):
        """Roll on the Knave spells table if character has Wizardry."""
        spells = []
        if self.has_wizardry:
            spell_keys = random.sample(list(SPELLS.keys()), k=3)
            print(f"{spell_keys = }")
            spells = [{k: v} for k, v in SPELLS.items() if k in spell_keys]
        return spells

    def get_money(self):
        """Roll 3d6 for starting money."""
        money = 0
        for _ in range(3):
            money += random.randint(1, 6)
        return money

    def to_dict(self):
        return self.__dict__


if __name__ == "__main__":
    from pprint import pprint

    level = random.randint(1, 9)
    print(f"{level = }")
    character = D666Character(level=level)
    pprint(character.to_dict())
