from cocpyth.dtypes.character import Character
from cocpyth.utils.io import save_character, load_character


def test_save_character(tmp_path):
    file = tmp_path / "steve.yaml"
    steve = Character("Steve", "Minecraft")
    save_character(steve, file)


def test_load_character(tmp_path):
    file = tmp_path / "steve.yaml"
    steve = Character("Steve", "Minecraft")
    save_character(steve, file)

    new_steve = load_character(file)
    assert steve == new_steve
