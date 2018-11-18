from character.exceptions import NotExistentElementException

class Character(object):
    CLASSES = {}
    RACES = {}

    playerName = None
    characterName = None
    race = None
    _class = None

    level = 1
    health = 0
    experience = 0
    stats = {}
    skills = set()

    gold = 0
    inventory = {}


    def __init__(self, playerName, characterName):
        self.playerName = playerName
        self.characterName = characterName.lower()
        self.level = 1
        self.health = 0
        self.gold = 0
        self.experience = 0
        self.inventory = {}
        self.skills = set()

    def initialize_character(self, race, _class):
        race = race.lower()
        _class = _class.lower()

        if race not in self.RACES:
            raise NotExistentElementException(
                "The race {} is not one of the existent races: {}".format(race, self.RACES))

        if _class not in self.CLASSES:
            raise NotExistentElementException(
                "The class {} is not one of the existent classes: {}".format(_class, self.CLASSES))

        self.race = race
        self._class = _class

        self.initialize_stats()

    def modify_stats(self, stat_name: str, new_value: int):
        stat_name = stat_name.lower()
        if stat_name in self.stats:
            self.stats[stat_name] = new_value

    def add_gold(self, amount):
        self.gold += amount

    def add_experience(self, amount):
        self.experience += amount

    def add_skill(self, skill_name):
        self.skills.add(skill_name)

    def remove_skill(self, skill_name):
        self.skills.pop(skill_name)

    def get_data_sheet(self):
        raise NotImplementedError()

    def initialize_stats(self):
        raise NotImplementedError()
