from shutil import get_terminal_size
from enum import Enum
from typing import Optional, Union
from pydantic.dataclasses import dataclass
import pandas as pd
from tabulate import tabulate
from cocpyth.dtypes.dice import d4, d6
from cocpyth.dtypes.skill import SKILLS1920
from cocpyth.dtypes.occupation import Occupation
from cocpyth.utils.weird_math import cthulhu_round
import cocpyth.dtypes.stat as stat


@dataclass
class Character:
    first_name: str
    last_name: str
    sanity: stat.Sanity = stat.Sanity()
    strength: stat.Strength = stat.Strength()
    dexterity: stat.Dexterity = stat.Dexterity()
    size: stat.Size = stat.Size()
    constitution: stat.Constitution = stat.Constitution()
    intelligence: stat.Intelligence = stat.Intelligence()
    education: stat.Education = stat.Education()
    power: stat.Power = stat.Power()
    appearance: stat.Appearance = stat.Appearance()
    luck: stat.Luck = stat.Luck()
    hp: stat.Hitpoints = stat.Hitpoints()
    mp: stat.Magicpoints = stat.Magicpoints()
    occupation : Optional[Occupation] = None
    occupational_skill_points: int = 0
    personal_skill_points: int = 0
    seed: Union[bool,int] = False

    def __post_init__(self):
        if self.seed:
            self.sanity = stat.Sanity(seed=self.seed)
            self.strength = stat.Strength(seed=self.seed)
            self.dexterity = stat.Dexterity(seed=self.seed)
            self.size = stat.Size(seed=self.seed)
            self.constitution = stat.Constitution(seed=self.seed)
            self.intelligence = stat.Intelligence(seed=self.seed)
            self.education = stat.Education(seed=self.seed)
            self.power = stat.Power(seed=self.seed)
            self.appearance = stat.Appearance(seed=self.seed)
            self.luck = stat.Luck(seed=self.seed)
        self.full_name = self.first_name + " " + self.last_name
        self.sanity.current = self.power.current
        self.sanity.max = self.sanity.current
        self.hp.current = cthulhu_round((self.constitution.current + self.size.current) / 10)
        self.hp.max = self.hp.current
        self.mp.current = cthulhu_round(self.power.current / 5)
        self.mp.max = self.mp.current
        self.skills = SKILLS1920
        self.skills.dodge.set(self.dexterity.current/2)
        self.damage_bonus, self.build = self._determine_build_db()
        self.moverate = self._determine_move_rate()
        self.personal_skill_points = (self.intelligence * 10).current


    def _determine_build_db(self):
        physique = self.strength.current + self.size.current

        if physique < 65:
            return -2, -2
        elif physique < 85:
            return -1, -1
        elif physique < 125:
            return 0, 0
        elif physique < 165:
            return d4, 1
        else: return d6, 2

    def _determine_move_rate(self):

        STR = self.strength.current
        DEX = self.dexterity.current
        SIZ = self.size.current

        if STR < SIZ and DEX < SIZ:
            return 7
        if STR > SIZ and DEX > SIZ:
            return 9
        return 8

    def _calculate_occupational_skill_points(self, formula:str):
        """Calculates the total occupational skill points based on the values of characterstics.
         An example formula: 2*Education+2*Power
        """
        total = 0
        if "*" not in formula:
            raise SyntaxError(f"Formula {formula} could not be interpreted to a skill points value.")
        parts = formula.split("+")
        for part in parts:
            skill, modifier = part.split("*")
            skill = getattr(self, skill.lower())
            total += (skill.current * int(modifier))
        return total

    
    def add_occupation(self, occupation: Occupation):
        self.occupation = occupation
        options = occupation.points_rule.split("|")
        options_points = [self._calculate_occupational_skill_points(o) for o in  options]
        self.occupational_skill_points = max(options_points)


    def list_skills(self):
        return list(self.skills)

    def stats_to_record(self):
        """Return the current base stats of the character as a single dictionary item"""
        settings = [ k for k in stat.__dict__.keys() if k.endswith("_settings")]
        stats = [setting.split("_")[0] for setting in settings]
        # Abbreviated hp and mp
        stats = list(map(lambda x: x.replace("hitpoints", "hp"), stats))
        stats = list(map(lambda x: x.replace("magicpoints", "mp"), stats))
        return {s:getattr(self, s).current for s in stats}
        

    def format_stats(self):
        
        stats = self.stats_to_record()
        stats_table = pd.DataFrame(stats, index=[0])
        stats_table.columns = [c.capitalize() for c in stats_table.columns]
        
        if get_terminal_size()[0] < 150:
            return tabulate(stats_table.T, headers=["Stat","Value"], tablefmt='psql')
        else: return tabulate(stats_table, headers="keys", showindex=False, tablefmt='psql')


    def _add_skillpoints(self, skill:str, amount:int):

        if skill not in self.list_skills():
            raise KeyError(f"Skill {skill} is not defined.")
        if self.skills[skill] + amount > self.skills[skill].max:
            raise OverflowError(f"Skill can't be more than {self.skills[skill].max}")
        self.skills[skill] += amount


    def spend_occupational_skill_points(self, skill:str, amount:int):
        if self.occupational_skill_points - amount < 0:
            raise OverflowError(f"Cannot spend {amount} skill points, while only having {self.occupational_skill_points} left. ")
        self._add_skillpoints(skill, amount)
        self.occupational_skill_points -= amount


    def spend_personal_skill_points(self, skill:str, amount:int):
        if self.personal_skill_points - amount < 0:
            raise OverflowError(f"Cannot spend {amount} skill points, while only having {self.personal_skill_points} left. ")
        self._add_skillpoints(skill, amount)
        self.personal_skill_points -= amount


class GenderEnum(str, Enum):
    M = "male"
    F = "female"


if __name__ == "__main__":

    steve = Character("Steve", "Minecraft")
    print(steve.skills.jump)
    print(steve.skills.jump + 10)
    print(steve.skills.jump)
    # for skills with spaces
    print(steve.skills.arts_and_crafts)
