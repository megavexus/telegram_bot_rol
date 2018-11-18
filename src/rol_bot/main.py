from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
from token_telegram import TOKEN

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

from dice import roll_dice
from dm import set_DM
from characters import alterExperience, alterGold, alterHealth, printCharacterStats, printInventory, createCharacter,inventoryUpdate
from monsters import create_monster, attack_monster

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher



def start(bot, update):
    #Displays "Welcome to Dungeons and Dragons.")
    bot.sendMessage(chat_id = update.message.chat_id, text = "Welcome to Dungeons and Dragons.")


def help_message(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I am the Dungeons and Dragons bot, and I can help to automate a few processes in your game of D&D to make it easier for everyone to play on Telegram." +
                    "\n Here are a list of commands that I can execute!" +
                    "\n \n Player Commands:" +
                    "\n /start - starts the DnD bot" +
                    "\n /createcharacter [character name] - Use this command and follow the prompts to create a new character" +
                    "\n /printcharacterstats [character name] - Prints a character's stats, add the name of the chharacter after the command" +
                    "\n /help - Open this help message" +
                    "\n /roll[int] - Rolls a dice with the customisable maximum value"
                    "\n \n Dungeon Master Commands:" +
                    "\n /createmonster [monster name] [health points] - Creates a monster." +
                    "\n /attackmonster [monster name] [damage] - Reduces health of the monster by a given number." +
                    "\n /changexp [character name] +/- X - Adds or subtracts a certain amount of health from a character." +
                    "\n /changegold [character name] +/- X - Adds or subtracts a certain amount of gold from a character." +
                    "\n /changehealth [character name] +/- X - Adds or subtacts a certain amount of health from a character."
                    "\n /inventoryupdate [character name] add/remove [item] [no. of item] - Adds or removes a certain amount of a specific item from a character's inventory."
                    "\n /printinventory - Current state of the inventory.")


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry, I didn't understand that command.")


if __name__ == "__main__":
    #dispatcher.add_handler(incomingMessages)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_message)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    # Dice
    dice_handler = CommandHandler('roll', roll_dice)
    dispatcher.add_handler(dice_handler)

    # DM
    set_dm_handler = CommandHandler("set_dm", set_DM)
    dispatcher.add_handler(set_dm_handler)

    # Character
    change_health_handler = CommandHandler('changehealth', alterHealth)
    create_character_handler = CommandHandler('createcharacter', createCharacter)
    print_character_handler = CommandHandler('printcharacterstats', printCharacterStats)
    update_inventory_handler = CommandHandler('updateinventory', inventoryUpdate)
    print_inventory_handler = CommandHandler('printinventory', printInventory)
    change_gold_handler = CommandHandler('changegold', alterGold)
    change_exp_handler = CommandHandler('changexp', alterExperience)

    dispatcher.add_handler(change_health_handler)
    dispatcher.add_handler(create_character_handler)
    dispatcher.add_handler(print_character_handler)
    dispatcher.add_handler(update_inventory_handler)
    dispatcher.add_handler(print_inventory_handler)
    dispatcher.add_handler(change_gold_handler)
    dispatcher.add_handler(change_exp_handler)

    # Monsters
    create_monster_handler = CommandHandler("createmonster", create_monster)
    attack_monster_handler = CommandHandler("attachmonster", attack_monster)

    dispatcher.add_handler(create_monster_handler)
    dispatcher.add_handler(attack_monster_handler)

    updater.start_polling()
