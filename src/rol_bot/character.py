from .database import RpgDatabase
from enum import Enum

"""
ROADMAP:
    - Añadir Skills
    - Añadir Inventario
    - Añadir Reputaciones (??)
        + Crear clase nueva de listado de reputaciones
        + Dejar al GM dar de alta reputaciones
"""

class Stats(Enum):
    METLLE = "MET"
    INFLUENCE = "INF"
    EXPERTISE = "EXP"
    PSYQUE = "PSY"
    INTERFACE = "INT"
    ARMOR = "ARM"

    @staticmethod
    def get_stat(stat):
        if type(stat) != str:
            return

        stat = stat.upper()

        for member in Stats:
            if member.name == stat:
                return member
            elif member.value == stat:
                return member

    @staticmethod
    def is_valid_stat(stat):
        stat = Stats.get_stat(stat)
        return stat != None


class Archetypes(Enum):
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

    @staticmethod
    def is_valid_archetype(archetype):
        if type(archetype) != str:
            return False

        archetype = archetype.upper()

        for member in Archetypes:
            if member.name == archetype:
                return True
        return False

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

    @staticmethod
    def is_valid_origin(origin):
        if type(origin) != str:
            return False

        origin = origin.upper()

        for member in Origin:
            if member.name == origin:
                return True
        return False

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

    def load(self):
        data = self.db.get_character(self.username)
        if data:
            for key, value in data.get("stats", {}).items():
                self.set_stat(key, value)

            if "origin" in data:
                self.set_origin(data.get("origin"))

            if "archetypes" in data:
                self.set_archetypes(data.get("archetypes"))

    def save(self):
        self.db.upsert_character(self.username, self.to_dict())

    def to_dict(self):
        dict_obj = {
            "username":self.username,
            "name":self.name,
            "description": self.description,
            "origin": self.origin,
            "archetypes": [arch for arch in self.archetypes],
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

    def set_archetypes(self, archetypes):
        if type(archetypes) == str:
            if ',' in archetypes:
                archetypes = archetypes.split(',')
            else:
                archetypes = [archetypes]

        if type(archetypes) == list:
            clean_archetypes = [
                arch.strip().lower()
                for arch in archetypes
                if type(arch) == str
                and Archetypes.is_valid_archetype(arch.strip().lower())
            ]

            self.archetypes = self.archetypes.union(clean_archetypes)
            return self.archetypes

    def get_archetypes(self):
        return self.archetypes

    def set_origin(self, origin):
        if type(origin) != str:
            return
        origin = origin.strip().lower()
        if Origin.is_valid_origin(origin):
            self.origin = origin
            return origin

    def get_origin(self):
        return self.origin

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

    def add_to_inventory(self, item, amount=1):
        raise NotImplementedError()

    def remove_from_inventory(self, position):
        raise NotImplementedError()

    def get_inventory(self):
        raise NotImplementedError()
