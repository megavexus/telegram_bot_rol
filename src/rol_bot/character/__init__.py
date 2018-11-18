from .character_dd import CharacterDAndD
from .character_uncharted_worlds import CharacterUnchartedWorlds

def character_factory(game):
    if game == "dandd":
        return CharacterDAndD
    elif game == "unchartedworlds":
        return CharacterUnchartedWorlds