import yaml
import re
import importlib.resources
from typing import Optional, List
from pydantic import BaseModel
from cocpyth.utils.weird_math import cthulhu_round


occupations = yaml.safe_load(importlib.resources.open_text("cocpyth.data", "occupations.yaml"))
coc_settings = occupations.keys()


class OccupationConstructor(BaseModel):
    name: str
    points: str
    skills: List[str]
    description: Optional[str] = None

class Occupation(BaseModel):
    name: str
    points_rule: str
    skill_choices: int
    specific_skill_choices : List[List[str]] = []
    specialization_choices : List[str] = []
    specialization_n_choices : int = 0 
    social_choices: int
    skills: List[str]
    description: Optional[str] = None

    def _translate_specialization_formula(self, formula):
        n_choices = formula[0]
        choices = formula[2:-1].split("|")
        return n_choices, choices

    def __init__(self, constructor: OccupationConstructor):
        
        skills = [sk.strip() for sk in constructor.skills if sk.strip() not in ["Any", "Interpersonal"]]
        specialization_n_choices = 0
        specialization_choices = []
        
        specialization_formula = [s for s in constructor.skills if "(" in s]
        for specialization_candidate in specialization_formula:
            specialization_match = re.search(r'\d\(.*\)', specialization_candidate)

            if specialization_match:
                constructor.skills.remove(specialization_candidate)
                specialization_n_choices, specialization_choices = \
                    self._translate_specialization_formula(specialization_candidate)
        
        specific_skill_choices = [s.strip().split("|") for s in constructor.skills if "|" in s]
        super().__init__(
            name=constructor.name.strip(),
            points_rule=constructor.points.strip(),
            skills=skills,
            skill_choices=constructor.skills.count("Any"),
            social_choices=constructor.skills.count("Interpersonal"),
            specific_skill_choices = specific_skill_choices,
            specialization_choices = specialization_choices,
            specialization_n_choices = specialization_n_choices,
            description=constructor.description,
        )           


class OccupationDict(dict):
    def __init__(self, *args, **kwargs):
        super(OccupationDict, self).__init__(*args, **kwargs)
        safe_keys = {k.lower().replace(" ", "_"): v for k, v in self.items()}
        self.__dict__ = safe_keys


def build_occupations(setting: str) -> [Occupation]:
    setting_occupations = occupations[setting]
    setting_occupations = {o["name"]: OccupationConstructor(**o) for o in setting_occupations}
    for k, constructor in setting_occupations.items():
        setting_occupations[k] = Occupation(constructor)
    return OccupationDict(setting_occupations)


SETTING_OCCUPATIONS = {setting: build_occupations(setting) for setting in coc_settings}
OCCUPATIONS1920 = SETTING_OCCUPATIONS["coc1920"]

if __name__ == "__main__":
    skills = OCCUPATIONS1920.antiquarian.skills
    print(skills)