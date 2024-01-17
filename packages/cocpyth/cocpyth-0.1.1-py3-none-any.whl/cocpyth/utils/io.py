import yaml
from yaml import Loader
from functools import partial
from cocpyth.dtypes.character import Character
from cocpyth.dtypes.skill import Skill, SkillDict
from cocpyth.dtypes.stat import (
    Stat,
    Strength,
    Sanity,
    Dexterity,
    Constitution,
    Hitpoints,
    Magicpoints,
    Appearance,
    Intelligence,
    Education,
    Size,
    Luck,
    Power,
)


def skill_representer(dumper, data):
    return dumper.represent_scalar(u'!Skill', f'{data.name}: ({data.current}|{data.half}|{data.fifth})')


def skill_constructor(loader, node):
    value = loader.construct_scalar(node)
    parts = value.split(":")
    skname = parts[0].strip()
    skval = parts[1].split("|")[0].strip().lstrip("(")
    return Skill(name=skname, current=int(float(skval)))


def stat_representer(dumper, data):
    return dumper.represent_scalar(f'!{data.name}', f'{data.current}')


def stat_constructor(loader, node, stat_class: Stat):
    value = loader.construct_scalar(node)
    stat = stat_class()
    stat.set(int(float(value)))
    return stat


yaml.add_representer(Skill, skill_representer)
yaml.add_constructor('!Skill', skill_constructor)
for stat in [
    Strength,
    Sanity,
    Dexterity,
    Constitution,
    Hitpoints,
    Magicpoints,
    Appearance,
    Intelligence,
    Education,
    Size,
    Luck,
    Power,
]:
    yaml.add_representer(stat, stat_representer)
    this_stat_constructor = partial(stat_constructor, stat_class=stat)
    yaml.add_constructor("!{}".format(stat.__name__), this_stat_constructor)


def save_character(char: Character, file):
    with open(file, "w") as f:
        skills = list(char.skills.values())
        char.skills = skills
        yaml.dump(char, f)
    return file


def load_character(file):
    with open(file, "r") as f:
        character = yaml.load(f, Loader)
        skills = {v.name: v for v in character.skills}
        character.skills = SkillDict(skills)
        return character
