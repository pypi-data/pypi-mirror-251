import random
from importlib.resources import open_text
from cocpyth.dtypes.character import GenderEnum

def generate_name(gender:GenderEnum, seed=False):
    namesf = "male_names.tsv"    
    lnamesf = "lnames.txt"

    if gender == GenderEnum.F:
        namesf = "fe" + namesf

    with open_text("cocpyth.data", namesf) as f:
        names = f.readlines()
    with open_text("cocpyth.data", lnamesf) as f:
        lnames = f.readlines()

    names = [n.strip() for n in names]
    lnames = [n.strip() for n in lnames]

    if seed:
        random.seed(seed)
    return random.choice(names), random.choice(lnames)