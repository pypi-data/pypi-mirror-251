import random
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError
from cocpyth import POSSIBLE_COMMANDS
from cocpyth.dtypes.occupation import OCCUPATIONS1920
from cocpyth.dtypes.character import GenderEnum
import cocpyth.prompts.default_responses as responses

def yes_or_no(response:str):
    res = response.lower().strip()
    if res in responses.AFFIRM or res == "":
        return True
    if res in responses.DECLINE:
        return False
    raise ValidationError(message="Not sure what you mean by that...")

class YesNoValidator(Validator):
    """Validate a yes/no response."""
    def validate(self, document: Document) -> None:
        txt = document.text
        if txt:
            yes_or_no(txt)


class YesNoRandomValidator(Validator):
    """Validate a yes/no response."""
    def validate(self, document: Document) -> None:
        txt = document.text
        valid_responses = responses.AFFIRM + responses.DECLINE + responses.RANDOM
        if txt and txt.lower() not in valid_responses:
            raise ValidationError(message="Not sure what you mean by that...") 


def gender_or_random(response:str):

    res = response.lower().strip()
    if res in responses.GENDERM:
        return GenderEnum.M
    if res in responses.GENDERF:
        return GenderEnum.F
    if res in responses.RANDOM:
        return True
    return False


class GenderOrRandomValidator(Validator):
    """Validate if a biological gender is chosen"""
    def validate(self, document: Document) -> None:
        txt = document.text
        if txt and not gender_or_random(txt):
            raise ValidationError(message="Not a valid biological gender.")

def interpret_occupation(input):
    res = input.strip()
    possible_occupations = list(OCCUPATIONS1920.keys())
    if res in possible_occupations: 
        return res
    if res in responses.RANDOM or res =="":
        return random.choice(possible_occupations)
    raise ValidationError(message="Not a valid occupation.")

class OccupationValidator(Validator):
    """Validate if occupation exists in setting"""        
    def validate(self, document: Document) -> None:
        txt = document.text
        if txt:
            interpret_occupation(txt)

def interpret_skill(input, valid_choices:list):
    res = input.strip()
    if res in valid_choices:
        return res
    raise ValidationError(message="Not a valid skill")


class SkillValidator(Validator):    
    """Validate if skill exists in setting"""

    def __init__(self, choices:list) -> None:
        super().__init__()
        self.valid_choices = choices

    def validate(self, document: Document) -> None:
        txt = document.text
        if txt:
            interpret_skill(txt, self.valid_choices)

class MaxNumberValidator(Validator):
    """Validate if number is below treshold"""
    def __init__(self, max:int) -> None:
        super().__init__()
        self.max_num = int(max)


    def validate(self, document: Document) -> None:
        txt = document.text
        
        if txt and not txt.isdigit():
            raise ValidationError(message="Not a number.")
        if txt and txt.isdigit() and int(txt) > self.max_num:
            raise ValidationError(message="You're trying to use more than you have.")
        

def interpret_command(cmd):
    res = cmd.strip().upper()
    if res in POSSIBLE_COMMANDS:
        return res
    if res == "":
        return "ROLL"
    raise ValidationError("Not a known command.")

class CommandValidator(Validator):

    def validate(self, document:Document) -> None:
        txt = document.text

        if txt:
            interpret_command(txt)