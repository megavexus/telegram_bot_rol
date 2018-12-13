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

def help_message(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=\
        "I am the Uncharted Worlds bot, and I can help to automate a few processes for make it easier for everyone to play on Telegram!." +
        "\n Here are a list of commands that I can execute!" +
        "\n /help - Open this help message" +
        "\n /roll <Number(int)> [<Modificator(int)>] - Rolls a 2d6 dice with + Number + Modificator" +
        "\n \n Player Commands:" +
        "\n /start - starts the DnD bot" +
        "\n /createcharacter [character name] - Use this command and follow the prompts to create a new character" +
        "\n /printcharacterstats [character name] - Prints a character's stats, add the name of the chharacter after the command" +
        "\n /roll[int] - Rolls a dice with the customisable maximum value"
        "\n \n Game Master Commands:" +
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
        if len(args) != 2:
            text = "Error! El comando tiene la forma /set_stat <STAT> <VALUE>"
            bot.sendMessage(chat_id=update.message.chat_id, text=text)
            return

        stat = args[0]
        try:
            value = int(args[1])
            character = self._get_character()
            character.set_stat(stat, value)
            character.save()
            text = "Stats actualizados!"
        except ValueError:
            text = "Error. El segundo parámetro debe de ser un número."
        except Exception:
            text = "Error. El stat {} no existe. Pruebe con uno de los siguientes: \n".format(stat)
            text += "\t - metlle (met)\n"
            text += "\t - influence (imf)\n"
            text += "\t - expertise (exp)\n"
            text += "\t - psyque (psy)\n"
            text += "\t - interface (int)\n"
            text += "\t - armor (arm)"

        bot.sendMessage(chat_id=update.message.chat_id, text=text)
        
    def show_character_sheet(self, bot, update, args):
        #Mira si es GM
        username = update.message.from_user.username
        if self.db.is_gm(username):
            character_user = args[0].replace('@','')
        else:
            character_user = username
        
        character = self._get_character(character_user)
        text = character.get_data_sheet()
        bot.sendMessage('@{}'.format(username), text)

@click.command()
@click.option('--db_path', '-db', help="Path a la base de datos que consultará", type=click.Path(), default="./db.json")
def main(db_path):
    token = get_token()
    updater = Updater(token=get_token())
    dispatcher = updater.dispatcher

    driver = GameDriver(db_path)

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
    set_dm_handler = CommandHandler("set_dm", driver.set_dm_handler)
    dispatcher.add_handler(set_dm_handler)

    # setters - Character
    naming_handler = CommandHandler("set_name", driver.set_name)
    set_origin_handler = CommandHandler("set_origin", driver.set_origin)
    set_archetypes_handler = CommandHandler("set_arch", driver.set_archetypes)
    set_stats_handler = CommandHandler("set_stat", driver.set_stat)
    dispatcher.add_handler(naming_handler)
    dispatcher.add_handler(set_origin_handler)
    dispatcher.add_handler(set_archetypes_handler)
    dispatcher.add_handler(set_stats_handler)

    # setters - Character
    get_sheet_handler = CommandHandler("view_character", driver.get_data_sheet)
    dispatcher.add_handler(get_sheet_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
