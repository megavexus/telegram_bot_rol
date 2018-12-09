import pytest
from rol_bot.database import RpgDatabase

@pytest.fixture
def database(tmpdir):
    path = tmpdir.mkdir('test').join('test.json').realpath()
    database = RpgDatabase(path)
    return database


def test_get_dm_no_set(database):
    username = "bernal"
    gm = database.get_gm(username)
    assert gm == None

def test_set_dm(database):
    username = "bernal"
    ok = database.set_gm(username)
    assert ok == [1]


def test_get_dm(database):
    username = "bernal"
    ok = database.set_gm(username)

    gm = database.get_gm(username)
    assert gm == username

characters = [
    ("player1", {
        "name": "PEPE",
        "roles":{"Carpintero":0, "Herrero":0},
        "stats":{
            "metlle":2,
            "interface":-1
        }}),
    ("player2", {
        "name":"PEDRO",
        "roles":{"Medico":2},
        "stats":{"Inteligencia":3}
    })
]
@pytest.mark.parametrize("username, data", characters)
def test_create_character(database, username, data):
    ret = database.upsert_character(username, data)
    assert ret == [1]


@pytest.mark.parametrize("username, data", characters)
def test_get_character(database, username, data):
    ret = database.upsert_character(username, data)
    character_data = database.get_character(username)
    assert character_data == data


@pytest.mark.parametrize("username, data", characters)
def test_update_character(database, username, data):
    ret = database.upsert_character(username, data)
    data["updated"] = True
    ret = database.upsert_character(username, data)
    data_ret = database.get_character(username)
    assert data_ret == data


@pytest.mark.parametrize("username, data", characters)
def test_update_character_partial(database, username, data):
    ret = database.upsert_character(username, data)
    update = {"perro_chico":"Si"}
    ret = database.upsert_character(username, update)
    data_ret = database.get_character(username)
    assert len(data_ret) > 1
    assert data_ret["perro_chico"] == "Si"


@pytest.mark.parametrize("username, data", characters)
def test_update_character_partial_content(database, username, data):
    ret = database.upsert_character(username, data)
    update = {"roles": {"Bombero":3}}
    ret = database.upsert_character(username, update)
    data_ret = database.get_character(username)
    assert data_ret['roles'] == {"Bombero":3}


def test_get_character_no_exists(database):
    username = "404"
    data = database.get_character(username)
    assert data == None
