from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
from rol_bot.token_telegram import get_token
from rol_bot.character.exceptions import NotExistentElementException
from rol_bot.dice import roll_dice
from rol_bot.characters import alterExperience, alterGold, alterHealth, printCharacterStats, printInventory, createCharacter, inventoryUpdate
import click

from rol_bot.character import Character
from rol_bot.database import RpgDatabase

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


game_type = None

def start(bot, update, args):
    global game_type

    games = {
        'dand':"Dungeons and Dragons",
        "uncharted": "Uncharted Worlds"
    }

    if len(args) == 0 or args[0] not in games:
        bot.sendMessage(chat_id=update.message.chat_id,
                            text="You must select one of the games: /roll {}.".format(games.keys()))
        return None
    game_type = args[0]
    # TODO: mandar un ReplyKeyboard para seleccionar el juego
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


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

class GameDriver(object):
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = RpgDatabase(db_path)

    def handler_set_gm(self, bot, update, args):
        username = update.message.from_user.username
        target_user = args[0]
        try:
            force_param = args[1] == "--force"
        except:
            force_param == False

        if self.db.get_gm() == None or self.db.is_gm(username) or force_param:
            self.db.set_gm(target_user.strip())
        else:
            text = "Error. Sólo el actual GM ({}) puede fijar otro GM".format(
                self.db.get_gm()
            )
            bot.sendMessage(chat_id=update.message.chat_id, text=text)

    def _get_character(self, update, username = None):
        if username == None:
            username = update.message.from_user.username
        character = Character(self.db, username)
        return character

    def set_name(self, bot, update, args):
        name = args[0]
        character = self._get_character()
        character.set_name(name)
        character.save()
    
    def set_origin(self, bot, update, args):
        origin = args[0]
        character = self._get_character()
        character.set_origin(origin)
        character.save()

    def set_archetypes(self, bot, update, args):
        archetypes = [args[0]]
        if len(args) > 1:
            archetypes.append(args[1])
        character = self._get_character()
        character.set_archetypes(archetypes)
        character.save()

    def set_stat(self, bot, update, args):
        stat = args[0]
        try:
            value = int(args[1])
        except:
            text = "Error. El "
            bot.sendMessage(chat_id=update.message.chat_id, text=text)
        pass


@click.command()
@click.option('--db_path', '-db', help="Path a la base de datos que consultará", type=click.Path(), default="./db.json")
def main(db_path):
    token = get_token()
    updater = Updater(token=get_token())
    dispatcher = updater.dispatcher

    # /set_dm <name>
    # /create_character name
    # /set_stat <stat> <attr>
    # /set_origin <origin>
    # /set_archetypes <archetype1> <archetype2> ...
    # /view_character [<username>]
    # /roll <num_stat> <Modificator>
    # /rolls <stat> <Modificator>

    #dispatcher.add_handler(incomingMessages)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_message)
    unknown_handler = MessageHandler(Filters.command, unknown)

    #dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    # Dice
    dice_handler = CommandHandler('roll', roll_dice, pass_args=True)
    dispatcher.add_handler(dice_handler)

    # DM
    """
    set_dm_handler = CommandHandler("set_dm", set_DM)
    dispatcher.add_handler(set_dm_handler)
    """

    # Character
    """
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
    """

    # Monsters
    """
    create_monster_handler = CommandHandler("createmonster", create_monster)
    attack_monster_handler = CommandHandler("attachmonster", attack_monster)
    dispatcher.add_handler(create_monster_handler)
    dispatcher.add_handler(attack_monster_handler)
    """

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()
