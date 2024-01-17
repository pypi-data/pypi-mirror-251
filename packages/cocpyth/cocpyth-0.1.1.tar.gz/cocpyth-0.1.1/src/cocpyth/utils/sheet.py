import shutil
import urllib.request

from pypdf import PdfReader, PdfWriter

from cocpyth.dtypes.character import Character

COC_GREYSCALE_1920_SHEET_URL = "https://www.chaosium.com/content/FreePDFs/CoC/Character%20Sheets/V2/CoC7%20PC%20Sheet%20-%20Auto-Fill%20-%201920s%20-%20Standard%20-%20Greyscale.pdf"
COC_COLOR_1920_SHEET_URL = "https://www.chaosium.com/content/FreePDFs/CoC/Character%20Sheets/V2/CoC7%20PC%20Sheet%20-%20Auto-Fill%20-%201920s%20-%20Standard%20-%20Color.pdf"



def download_charactersheet(file_name, color=False):

    url = COC_GREYSCALE_1920_SHEET_URL
    if color:
        url = COC_COLOR_1920_SHEET_URL
    
    with urllib.request.urlopen(url) as response,\
        open(file_name, 'wb') as outf:
        shutil.copyfileobj(response, outf)
    
    return file_name

def add_skill_values_to_dict(skdict, skill_name, character):

    if skill_name == "Fighting": return skdict

    skill_name_spaceless = skill_name.replace(" ","")
    # Some abbriviations are used randomly
    if skill_name == "Sleight of Hand":
        skill_name_spaceless = "Sleight"
    if skill_name == "Firearms (Handgun)":
        skill_name_spaceless = "FireArmsHandguns"
    if skill_name == "Firearms (Rifle/Shotgun)":
        skill_name_spaceless = "FireArmsRifles"
    if skill_name == "Fighting (Brawl)":
        skill_name_spaceless = "Fighting"
    if skill_name_spaceless.startswith("Electrical"):
        skill_name_spaceless = "ElecRepair"
    if skill_name_spaceless.startswith("Mechanical"):
        skill_name_spaceless = "MechRepair"
    if skill_name in ["Credit Rating", "Drive Auto"]:
        skill_name_spaceless = skill_name.split(" ")[0]
    if skill_name.endswith("1"):
        skill_name = skill_name.rstrip("1") + " (Brawl)"

    if skill_name.endswith("_Copy"):
        skill_name = skill_name.split("_")[0]

    else: skill_name_spaceless = "Skill_" + skill_name_spaceless

    skdict[skill_name_spaceless] = character.skills[skill_name].current
    skdict[skill_name_spaceless + "_half"] = character.skills[skill_name].half
    skdict[skill_name_spaceless + "_fifth"] = character.skills[skill_name].fifth
    return skdict


def add_stat_to_dict(skdict, stat_name, character):

    abbrev = stat_name[:3].upper()
    skdict[abbrev] = getattr(character, stat_name).current
    skdict[abbrev + "_half"] = getattr(character, stat_name).half
    skdict[abbrev + "_fifth"] = getattr(character, stat_name).fifth
    return skdict

def fill_in_charactersheet(sheet_file, character):
    
    reader = PdfReader(sheet_file)
    writer = PdfWriter()

    first_page = reader.pages[0]
    second_page = reader.pages[1]
    third_page = reader.pages[2]

    fields = reader.get_fields()

    writer.add_page(first_page)

    to_update = {
        'Investigators_Name' : character.full_name,
        'Occupation' : character.occupation,
        'Age' : "",
        'StartingSanity' : character.sanity.current,
        'StartingHP' : character.hp.max,
        'StartingMagic' : character.mp.max,
        'StartingLuck' : character.luck.current,
        'DamageBonus' : character.damage_bonus,
        'Build' : character.build,
        'MOV' : character.moverate
    }

    for skill in character.skills:
        to_update = add_skill_values_to_dict(to_update, skill, character)
        if skill == "Dodge":
            to_update = add_skill_values_to_dict(to_update, "Dodge_Copy", character)
        if skill == "Fighting (Brawl)":
            to_update = add_skill_values_to_dict(to_update, "Fighting1", character)

    for stat in ['strength', 'dexterity', 'size', 'constitution', 'intelligence', 'education', 'power', 'appearance']:
        to_update = add_stat_to_dict(to_update, stat, character)

    writer.update_page_form_field_values(
        writer.pages[0], to_update
    )

    writer.add_page(second_page)
    writer.add_page(third_page)

    with open(sheet_file, "wb") as fs:
        writer.write(fs)

if __name__ == "__main__":
    sheet = download_charactersheet("sheet.pdf")
    steve = Character("Steve", "Minecraft")
    fill_in_charactersheet(sheet, steve)
