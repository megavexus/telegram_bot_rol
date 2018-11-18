monsterList = [] #list storing all monsters
monsterIndex = 0 #number of monsters

class Monster(object):
    def __init__(self, name, health):
        self.name = name
        self.health = health


def find_monster_index(name):  # returns index of character using player name
    for i in range(len(monsterList)):
        if name == monsterList[i].name:
            return i

def create_monster(bot, update):
    global monsterIndex
    input = update.message.text #input: /createmonster NAME HEALTH
    input = input.split() #split the input into the 3 parts
    monsterName = input[1]
    health = int(input[2])
    monsterList.append(Monster(monsterName, health)) #add to list
    bot.sendMessage(chat_id = update.message.chat_id, text = monsterList[monsterIndex].name + " has been created with %d health" % (monsterList[monsterIndex].health))
    monsterIndex += 1

def attack_monster(bot, update):
    input = update.message.text #input: /attackmonster NAME DAMAGE
    input = input.split() #split into the parts
    i = find_monster_index(input[1])
    damage = int(input[2])
    monsterList[i].health -= damage
    bot.sendMessage(chat_id = update.message.chat_id, text = monsterList[i].name + "'s health has reduced by " + str(damage) + " to " + str(monsterList[i].health))

