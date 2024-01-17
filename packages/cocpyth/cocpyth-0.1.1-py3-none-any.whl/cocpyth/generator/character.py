import random
from typing import Union
from pydantic.dataclasses import dataclass
from prompt_toolkit import prompt
from cocpyth.generator.name import generate_name
from cocpyth.dtypes.character import GenderEnum, Character

@dataclass
class CharacterGenerator():
    rstats: bool
    rgender: Union[bool, GenderEnum]
    rname: Union[bool,str]
    seed: Union[bool,int] = False

    def generate(self):

        if self.seed:
            random.seed(self.seed)
            #raise NotImplementedError("Implement seeded version")

        if self.rgender == True:
            self.rgender = random.choice(list(GenderEnum))

        if not self.rname:
            fname = prompt("First name?", type=str)
            lname = prompt("Last name?", type=str)
        elif type(self.rname) == str:
            fname, lname = self.rname.split(" ", 1)
        else: 
            fname, lname = generate_name(self.rgender, seed=self.seed)
        if self.rstats:
            character = Character(first_name=fname, last_name=lname, seed=self.seed)
        else:
            # TODO: lookup array spending mode and implement
            raise NotImplementedError
    
        return character