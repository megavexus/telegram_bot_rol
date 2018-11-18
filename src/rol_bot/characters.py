from utils import parseInput
from characters.character_base import NotExistentElementException

characterList = []
playerIndex = 0
attributes = False

def createCharacter(bot, update):
    global playerIndex
    if findCharacterIndex(update.message.from_user.first_name) != -1:
        bot.sendMessage(chat_id=update.message.chat_id, text="@" +
                        update.message.from_user.first_name + " already has a character")
        return None
    characterName = update.message.text[17:].lower()
    playerName = update.message.from_user.first_name
    characterList.append(Character(playerName, characterName))
    #Displays "Character [Character] has been created [Player]"
    bot.sendMessage(chat_id=update.message.chat_id, text="Character " +
                    characterList[playerIndex].characterName + " has been created by " + characterList[playerIndex].playerName)
    playerIndex += 1
    #Displays "@[Player] Please enter your character's attributes in the format of [Race] [Class]"
    bot.sendMessage(chat_id=update.message.chat_id, text="@" + playerName +
                    " Please enter your character's Race & Class in the format: [Race] [Class]")
    global attributes
    attributes = True

def get_character_list(bot, update):
    global characterList

    if len(characterList) == 0:
        text = "There are no characters"
        bot.sendMessage(chat_id=update.message.chat_id, text=text)
    else:
        text = []
        for character in characterList:
            character_string = "{} level {} {} {} [player:{}]".format(
                character.characterName,
                character.level,
                character._class,
                character.race,
                character.playerName
            )
            text.append(character_string)
        bot.sendMessage(chat_id=update.message.chat_id, text="\n".join(text))


def incomingMessages(bot, update):
    global attributes, characterList

    if attributes == True:
        attributesInput = update.message.text.lower()
        attributesInput = attributesInput.split()
        i = findCharacterIndex(update.message.from_user.first_name)
        characterList[i].race = attributesInput[0]
        characterList[i]._class = attributesInput[1]
        #Display "@[Player] [Character]'s race is [Race] and [Character]'s class is [Class]
        try:
            bot.sendMessage(chat_id=update.message.chat_id, text="@" + characterList[i].playerName + " " + characterList[i].characterName +
                            "'s race is " + characterList[i].race + " and " + characterList[i].characterName + "'s class is " + characterList[i]._class + ".")
            characterList[i].initialize_character(
                characterList[i].race, characterList[i]._class)
            statsheet = characterList[i].get_data_sheet()

            bot.sendMessage(chat_id=update.message.chat_id, text=statsheet)
            attributes = False
        except NotExistentElementException as e:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=str(e.message))


def printCharacterStats(bot, update):
    # /printcharacterstats CHARACTER_NAME
    userInput = parseInput(update.message.text, 2)
    i = getIndexFromCharacter(userInput[1])
    statsheet = (str(characterList[i].characterName) + "\n Created by: "
                 + str(characterList[i].playerName)
                 + "\n ----------------------------"
                 + "\n Strength: " + str(characterList[i].stats['strength'])
                 + "\n Dexterity: " + str(characterList[i].stats['dexterity'])
                 + "\n Wisdom: " + str(characterList[i].stats['wisdom'])
                 + "\n Intelligence: " +
                 str(characterList[i].stats['intelligence'])
                 + "\n Constitution: " +
                 str(characterList[i].stats['constitution'])
                 + "\n Charisma: " + str(characterList[i].stats['charisma'])
                 + "\n ----------------------------"
                 + "\n Health: " + str(characterList[i].health)
                 + "\n Gold: " + str(characterList[i].gold)
                 + "\n Experience: " + str(characterList[i].experience))
    bot.sendMessage(chat_id=update.message.chat_id, text=statsheet)


def findCharacterIndex(first_name):
    for i in range(len(characterList)):
        if characterList[i].playerName == first_name:
            return i
    return -1


def alterHealth(bot, update):
    global DM
    #/changehealth charactername value
    user = update.message.from_user.first_name
    if user != DM:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="You're not authorised to use this command!")
    else:
        userInput = parseInput(update.message.text, 3)
        i = getIndexFromCharacter(userInput[1])
        value = int(userInput[2])
        characterList[i].health += value
        bot.sendMessage(chat_id=update.message.chat_id, text=characterList[i].characterName +
                        "'s health has been changed " + userInput[2] + " to " + str(characterList[i].health))


def inventoryUpdate(bot, update):
    global DM
    user = update.message.from_user.first_name
    if user != DM:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="You're not authorised to use this command!")
    else:
        inventoryInput = parseInput(update.message.text, 5)
        i = getIndexFromCharacter(inventoryInput[1])
        print(inventoryInput[1] + characterList[i].playerName)
        if inventoryInput[2] == "remove":
            if inventoryInput[3] not in characterList[i].inventory:
                bot.sendMessage(chat_id=update.message.chat_id, text="@" +
                                characterList[i].playerName + " You don't have %s in your inventory!" % (inventoryInput[3]))
            elif inventoryInput[3] in characterList[i].inventory:
                if int(inventoryInput[4]) > characterList[i].inventory[inventoryInput[3]]:
                    bot.sendMessage(chat_id=update.message.chat_id, text="@" +
                                    characterList[i].playerName + " You don't have enough " + inventoryInput[3] + "!")
                elif int(inventoryInput[4]) == characterList[i].inventory[inventoryInput[3]]:
                    del characterList[i].inventory[inventoryInput[3]]
                elif int(inventoryInput[4]) < characterList[i].inventory[inventoryInput[3]]:
                    characterList[i].inventory[inventoryInput[3]
                                               ] = characterList[i].inventory[inventoryInput[3]] - int(inventoryInput[4])
        elif inventoryInput[2] == "add":
            if inventoryInput[3] not in characterList[i].inventory:
                characterList[i].inventory[inventoryInput[3]] = int(
                    inventoryInput[4])
            elif inventoryInput[3] in characterList[i].inventory:
                characterList[i].inventory[inventoryInput[3]
                                           ] = characterList[i].inventory[inventoryInput[3]] + int(inventoryInput[4])
        print(characterList[i].inventory)
        items = characterList[i].inventory.items()
        text = characterList[i].characterName + "'s Inventory \n"
        for item in items:
            text += item[0] + ": " + str(item[1]) + "\n"
        bot.sendMessage(chat_id=update.message.chat_id, text=text)


def printInventory(bot, update):
    inventoryInput = update.message.text
    inventoryInput = inventoryInput.split()
    name = inventoryInput[1]
    i = getIndexFromCharacter(name)
    items = characterList[i].inventory.items()
    text = characterList[i].characterName + "'s Inventory \n"
    for item in items:
        text += item[0] + ": " + str(item[1]) + "\n"
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def alterGold(bot, update):
    global DM
    #/changehealth charactername value
    user = update.message.from_user.first_name
    if user != DM:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="You're not authorised to use this command!")
    else:
        userInput = parseInput(update.message.text, 3)
        characterName = userInput[1]
        value = int(userInput[2])
        i = getIndexFromCharacter(characterName)
        characterList[i].gold += value
        bot.sendMessage(chat_id=update.message.chat_id, text=characterList[i].characterName +
                        "'s gold has been changed by" + userInput[2] + " to " + str(characterList[i].gold))


def alterExperience(bot, update):
    global DM
    #/changeXP characterName value
    user = update.message.from_user.first_name
    if user != DM:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="You're not authorised to use this command!")
    else:
        userInput = parseInput(update.message.text, 3)
        characterName = userInput[1]
        value = int(userInput[2])
        i = getIndexFromCharacter(characterName)
        characterList[i].experience += value
        bot.sendMessage(chat_id=update.message.chat_id, text=characterList[i].characterName +
                        "'s XP has been changed by" + userInput[2] + " to " + str(characterList[i].experience))


def getIndexFromCharacter(name):
    global characterList
    for i in range(len(characterList)):
        if characterList[i].characterName == name:
            return i
