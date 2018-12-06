from .database import RpgDatabase
from enum import Enum


class Stats(Enum):
    METLLE = "M"
    INFLUENCE = "I"
    EXPERTISE = "E"
    PSYQUE = "P"
    INTERFACE = "IN"
    ARMOR = "A"

    @staticmethod
    def get_stat(stat):
        if type(stat) != str:
            return

        stat = stat.upper()

        for member in Stats:
            compare_member = member
            if member.name == stat:
                return member
            elif member.value == stat:
                return member

    @staticmethod
    def is_valid_stat(stat):
        stat = Stats.get_stat(stat)
        return stat != None

class Archetipes(Enum):
    ACADEMIC = 1
    CLANDESTINE = 2
    COMMERCIAL = 3
    EXPLORER = 4
    INDUSTRIAL = 5
    MILITARY = 6
    PERSONALITY = 7
    SCOUNDRED = 8
    STARFARER = 9
    TECHNOCRAT = 10

class Origin(Enum):
    ADVANCED = 1
    COLONIST = 2
    CROWDED = 3
    FRONTLER = 4
    IMPOVERISHED = 5
    PRIVILEGED = 6
    PRODUCTIVE = 7
    REGIMENTED = 8
    SPACER = 9
    VIOLENT = 10

class NotExistentStatException(Exception):
    """ Excepcion cuando no existe un stat """

class Character(object):
    def __init__(self, database, username = ""):
        self.db = database
        self.stats = {
            'metlle': 0,
            'influence': 0,
            'expertise': 0,
            "psyque": 0,
            "interface": 0,
            "armor": 0
        }

        self.username = username
        self.name = ""
        self.description = ""
        self.origin = ""
        # rol, xp.
        self.archetypes = set()
        self.inventory = dict()
        self.skills = set()
        self.origin = None
        self.factions = dict()

    def load(self, username):
        self.username = username
        data = self.db.get_character(username)
        for key, value in data.get("stats", {}):
            self.set_stat(key, value)

        self.archetypes = data.get("archetypes")

    def save(self):
        self.db.upsert_character(self.username, self.to_dict())

    def to_dict(self):
        dict_obj = {
            "username":self.username,
            "name":self.name,
            "description": self.description,
            "origin": self.origin,
            "archetypes": self.archetypes,
            "stats":self.stats,
            "inventory":self.inventory,
            "factions": self.factions
        }
        return dict_obj

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_stat(self, stat, value):
        stat_elem = Stats.get_stat(stat)
        if stat_elem:
            try:
                self.stats[stat_elem.name.lower()] = int(value)
            except TypeError as e:
                raise ValueError(str(e))
        else:
            raise NotExistentStatException(stat)

    def get_stat(self, stat):
        stat_elem = Stats.get_stat(stat)
        if stat_elem:
            return self.stats[stat_elem.name.lower()]

    def get_data_sheet(self):
        data_sheet = """
        **{name}**
        - __Created by: `{username}`__
        - Archetypes: `{archetypes}`
        - Origin: `{origin}`
        --------------------
        - Metlle: `{metlle}`
        - Expertise: `{expertise}`
        - Influence: `{influence}`
        - Psyque: `{psyque}`
        - Interface: `{interface}`
        --------------------
        - Armor: `{armor}`
        """
        #- Inventory: `{inventory}`
        #inventory = "\n\t+"+"\n\t+".join(self.inventory)
        dict_data = {
            "name": self.name,
            "username": self.username,
            "archetypes": ", ".join(self.archetypes),
            "origin": self.origin,
            #"inventory": inventory
        }
        for key, value in self.stats:
            dict_data[key] = value
        data_sheet = data_sheet.format(dict_data)
        return data_sheet

    def get_xp(self, archetype):
        raise NotImplementedError()

    def set_xp(self, archetype, value):
        raise NotImplementedError()

    def get_origin(self, origin):
        raise NotImplementedError()

    def set_origin(self, origin):
        raise NotImplementedError()

    def add_to_inventory(self, item, amount=1):
        raise NotImplementedError()

    def remove_from_inventory(self, position):
        raise NotImplementedError()

    def get_inventory(self):
        raise NotImplementedError()

"""
ROADMAP:
    - Añadir Skills
    - Añadir Inventario
    - Añadir Reputaciones
        + Opción de doble reputación? Mejor no.

"""
