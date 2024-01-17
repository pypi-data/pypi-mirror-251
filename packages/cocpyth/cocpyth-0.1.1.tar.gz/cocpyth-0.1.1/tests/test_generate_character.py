from unittest import mock
from cocpyth.dtypes.occupation import OCCUPATIONS1920
from cocpyth.generator.character import CharacterGenerator
# Test for criminal, for 4(|||) rule

def test_generate_criminal():
    generator = CharacterGenerator(rstats=True, rgender=True, rname=True, seed=42)
    character = generator.generate()
    character.add_occupation(OCCUPATIONS1920["Criminal"])
    assert character.occupation.specialization_n_choices == 4
    assert character.occupation.specialization_choices == ['Appraise', 'Disguise', 'Fighting', 'Firearms', 'Locksmith', 'Mechanical Repair', 'Sleight of Hand']
