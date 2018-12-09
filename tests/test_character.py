import pytest
import os
from rol_bot.database import RpgDatabase
from rol_bot.character import Character, NotExistentStatException

@pytest.fixture
def database(tmpdir):
    path = tmpdir.mkdir('test').join('test.json').realpath()
    database = RpgDatabase(path)
    return database

@pytest.fixture
def character(database):
    return Character(database, "test")

def test_create_empty_character(database):
    username = "test"
    character = Character(database, username)
    assert character.username == username


@pytest.mark.parametrize("stat, value, check_stat", [
    ("met", 3, "metlle"),
    ("METLLE", 3, "metlle"),
    ("metlle", 3, "metlle"),
    ("Influence", 2, "influence"),
    ("INF", 2, "influence"),
    ("PSYQUE", 2, "psyque"),
    ("PSY", "2", "psyque"),
    ("interface", 2, "interface"),
    ("INT", 2, "interface"),
    ("Arm", "3", "armor"),
    ("armor", -1, "armor")
])
def test_set_stats(character, stat, value, check_stat):
    character.set_stat(stat, value)
    assert character.stats[check_stat] == int(value)


@pytest.mark.parametrize("stat, value", [
    ("Y", 3),
    (None, 3),
    (6, 3),
    ("METLLLE", 3),
    (4.2, 3),
    ("", 3)
])
def test_set_bad_stat(character, stat, value):
    with pytest.raises(NotExistentStatException):
        character.set_stat(stat, value)


@pytest.mark.parametrize("stat, value", [
    ("metlle", "A"),
    ("metlle", ""),
    ("metlle", None)
])
def test_set_bad_stat_value(character, stat, value):
    with pytest.raises(ValueError):
        character.set_stat(stat, value)


@pytest.mark.parametrize("stat, value, check_stat", [
    ("MET", 3, "metlle"),
    ("METLLE", 3, "metlle"),
    ("metlle", 3, "metlle"),
    ("Influence", 2, "influence"),
    ("INF", 2, "influence"),
    ("PSYQUE", 2, "psyque"),
    ("PSY", "2", "psyque"),
    ("interface", 2, "interface"),
    ("INT", 2, "interface"),
    ("ARM", "3", "armor"),
    ("armor", -1, "armor")
])
def test_get_stats(character, check_stat, value, stat):
    character.set_stat(stat, value)
    value_saved = character.get_stat(check_stat)
    assert value_saved == int(value)

@pytest.mark.parametrize("archetypes, expected",[
    ("academic", set(["academic"])),
    (["academic", "commercial"], set(["academic", "commercial"])),
    (["academic", "commercial"], set(["academic", "commercial"])),
    ("academic, industrial", set(["academic", "industrial"])),
    ("academic, academic, commercial,industrial",
     set(["academic", "commercial", "industrial"]))
])
def test_set_archetypes(character, archetypes, expected):
    character.set_archetypes(archetypes)
    assert character.archetypes == expected

@pytest.mark.parametrize("archetypes, expected", [
    ("acadaemic", set()),
    (["acadeamic", "commearcial"], set()),
    (["acaqdemic", "commercial"], set(["commercial"])),
    ("academaic, commerciaal", set()),
    ("acadeamic, academic, commercial", set(["academic", "commercial"])),
])
def test_set_bad_archetypes(character, archetypes, expected):
    character.set_archetypes(archetypes)
    assert character.archetypes == expected


@pytest.mark.parametrize("archetypes, expected", [
    ("academic", set(["academic"])),
    ("", set()),
    (None, set()),
    (1234, set()),
    (["academic", "commercial"], set(["academic", "commercial"])),
    (["academic", "commercial"], set(["academic", "commercial"])),
    ("academic, industrial", set(["academic", "industrial"])),
    ("academic, academic, commercial", set(["academic", "commercial"]))

])
def test_get_archetypes(character, archetypes, expected):
    character.set_archetypes(archetypes)
    assert character.get_archetypes() == expected


@pytest.mark.parametrize("origin, expected", [
    ("privileged", "privileged"),
    ("FRONTLER", "frontler"),
    (" CrOwDeD ", "crowded")
])
def test_set_origin(character, origin, expected):
    character.set_origin(origin)
    assert character.origin == expected


@pytest.mark.parametrize("origin", [
    ("privilegaed"),
    ("FRONTLERa"),
    (" CrOwDeDa "),
    (None),
    (1234),
    ("")
])
def test_set_bad_origin(character, origin):
    ret = character.set_origin(origin)
    assert ret == None
    assert character.origin == None


@pytest.mark.parametrize("origin, expected", [
    ("privileged", "privileged"),
    ("FRONTLER", "frontler"),
    (" CrOwDeD ", "crowded")
])
def test_get_origin(character, origin, expected):
    character.set_origin(origin)
    assert character.get_origin() == expected


def test_load_empty_character(database):
    username = "test"
    character = Character(database, username)
    character.load()
    assert character.username == username
    assert character.name == ""
    assert character.stats == {'armor': 0,
                               'expertise': 0,
                               'influence': 0,
                               'interface': 0,
                               'metlle': 0,
                               'psyque': 0}
    assert character.origin == None
    assert character.archetypes == set()

@pytest.mark.skip
def test_save_character(database):
    username = "test_complete"
    character = Character(database, username)
    character.set_origin("ADVANCED")
    character.set_archetypes("technocrat, commercial")
    character.set_stat()


@pytest.mark.skip
def test_load_created_character(database):
    pass
