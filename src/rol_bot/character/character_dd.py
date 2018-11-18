from character.character_base import Character

class CharacterDAndD(Character):
    def __init__(self, *args, **kwargs):
        self.skills = {
            'strength': 0,
            'dexterity': 0,
            'wisdom': 0,
            "intelligence": 0,
            "constitution": 0,
            "charisma": 0
        }
        self.RACES = {
            "human",
            "dwarf",
            "elf",
            "ogre",
            "merman"
        }

        self.CLASSES = {
            "fighter",
            "mage",
            "priest",
            "thief",
            "ranger"
        }
        super(CharacterDAndD, self).__init__(*args, **kwargs)

    def get_data_sheet(self):
        return (str(self.characterName) + "\n Created by: " + str(self.playerName)
                + "\n ----------------------------"
                + "\n Strength: " +
                str(self.stats['strength'])
                + "\n Dexterity: " +
                str(self.stats['dexterity'])
                + "\n Wisdom: " + str(self.stats['wisdom'])
                + "\n Intelligence: " +
                str(self.stats['intelligence'])
                + "\n Constitution: " +
                str(self.stats['constitution'])
                + "\n Charisma: " +
                str(self.stats['charisma'])
                + "\n ----------------------------"
                + "\n Health: " + str(self.health)
                + "\n Gold: " + str(self.gold)
                + "\n Experience: " + str(self.experience))

    def initialize_stats(self):
        if self.race == 'human':
            self.stats['strength'] = 5
            self.stats['dexterity'] = 5
            self.stats['wisdom'] = 5
            self.stats['intelligence'] = 5
            self.stats['constitution'] = 5
            self.stats['charisma'] = 5
            if self.stats['constitution'] == 5:
                self.health = 18
        #Race Stats for Dwarf
        elif self.race == 'dwarf':
            self.stats['strength'] = 6
            self.stats['dexterity'] = 3
            self.stats['wisdom'] = 3
            self.stats['intelligence'] = 3
            self.stats['constitution'] = 7
            self.stats['charisma'] = 3
            if self.stats['constitution'] == 7:
                self.health = 20
        #Race Stats for Elf
        elif self.race == 'elf':
            self.stats['strength'] = 3
            self.stats['dexterity'] = 3
            self.stats['wisdom'] = 8
            self.stats['intelligence'] = 7
            self.stats['constitution'] = 3
            self.stats['charisma'] = 6
            if self.stats['constitution'] == 3:
                self.health = 16
        #Race Stats for Ogre
        elif self.race == 'ogre':
            self.stats['strength'] = 10
            self.stats['dexterity'] = 3
            self.stats['wisdom'] = 3
            self.stats['intelligence'] = 3
            self.stats['constitution'] = 8
            self.stats['charisma'] = 3
            if self.stats['constitution'] == 8:
                self.health = 21
        #Race Stats for Merman
        elif self.race == 'merman':
            self.stats['strength'] = 7
            self.stats['dexterity'] = 5
            self.stats['wisdom'] = 6
            self.stats['intelligence'] = 5
            self.stats['constitution'] = 4
            self.stats['charisma'] = 3
            if self.stats['constitution'] == 4:
                self.health = 17
        #Class Stats for Fighter
        if self._class == 'fighter':
            self.stats['strength'] = self.stats['strength'] + 2
            self.stats['dexterity'] = self.stats['dexterity']
            self.stats['wisdom'] = self.stats['wisdom'] - 1
            self.stats['intelligence'] = self.stats['intelligence'] - 2
            self.stats['constitution'] = self.stats['constitution'] + 2
            self.stats['charisma'] = self.stats['charisma'] - 1
            self.gold = 50
            self.experience = 0

        #Class Stats for Mage
        elif self._class == 'mage':
            self.stats['strength'] = self.stats['strength'] - 2
            self.stats['dexterity'] = self.stats['dexterity']
            self.stats['wisdom'] = self.stats['wisdom'] + 2
            self.stats['intelligence'] = self.stats['intelligence'] + 2
            self.stats['constitution'] = self.stats['constitution'] - 1
            self.stats['charisma'] = self.stats['charisma'] - 1
            self.gold = 100
        #Class Stats for Priest
        elif self._class == 'priest':
            self.stats['strength'] = self.stats['strength'] - 2
            self.stats['dexterity'] = self.stats['dexterity']
            self.stats['wisdom'] = self.stats['wisdom'] + 3
            self.stats['intelligence'] = self.stats['intelligence'] + 1
            self.stats['constitution'] = self.stats['constitution'] - 1
            self.stats['charisma'] = self.stats['charisma'] - 1
            self.gold = 250
            self.experience = 0
        #Class Stats for Thief
        elif self._class == 'thief':
            self.stats['strength'] = self.stats['strength'] - 1
            self.stats['dexterity'] = self.stats['dexterity'] + 2
            self.stats['wisdom'] = self.stats['wisdom'] - 2
            self.stats['intelligence'] = self.stats['intelligence']
            self.stats['constitution'] = self.stats['constitution'] - 1
            self.stats['charisma'] = self.stats['charisma'] + 2
            self.gold = 200
            self.experience = 0
        #Class Stats for Ranger
        elif self._class == 'ranger':
            self.stats['strength'] = self.stats['strength'] - 1
            self.stats['dexterity'] = self.stats['dexterity'] + 3
            self.stats['wisdom'] = self.stats['wisdom'] - 1
            self.stats['intelligence'] = self.stats['intelligence']
            self.stats['constitution'] = self.stats['constitution'] - 2
            self.stats['charisma'] = self.stats['charisma'] + 1
            self.gold = 200
            self.experience = 0




