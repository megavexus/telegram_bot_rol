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
    ("M", 3, "metlle"),
    ("METLLE", 3, "metlle"),
    ("metlle", 3, "metlle"),
    ("Influence", 2, "influence"),
    ("I", 2, "influence"),
    ("PSYQUE", 2, "psyque"),
    ("P", "2", "psyque"),
    ("interface", 2, "interface"),
    ("IN", 2, "interface"),
    ("A", "3", "armor"),
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
    ("M", 3, "metlle"),
    ("METLLE", 3, "metlle"),
    ("metlle", 3, "metlle"),
    ("Influence", 2, "influence"),
    ("I", 2, "influence"),
    ("PSYQUE", 2, "psyque"),
    ("P", "2", "psyque"),
    ("interface", 2, "interface"),
    ("IN", 2, "interface"),
    ("A", "3", "armor"),
    ("armor", -1, "armor")
])
def test_get_stats(character, check_stat, value, stat):
    character.set_stat(stat, value)
    value_saved = character.get_stat(check_stat)
    assert value_saved == int(value)

@pytest.mark.skip()
def test_set_archetypes(character, archetypes, expected):
    pass


@pytest.mark.skip()
def test_get_archetypes(character, archetypes, expected):
    pass


@pytest.mark.skip
def test_load_empty_character(database):
    username = "test"
    character = Character(database, username)
    character.load()
    assert character.username == username


@pytest.mark.skip
def test_save_character(database):
    pass


@pytest.mark.skip
def test_load_created_character(database):
    pass
