from random import randint
from .utils import bad_response_rand
import re
# D4, D6, D8, D10, D12, D20

def roll_dices_results(dice):
    try:
        number_of_dices = 1
        dice_number = int(dice)
    except ValueError:
        pattern = re.compile(
            r"^(?P<number_of_dices>[0-9]+)d(?P<dice_number>[0-9])+$")
        match = pattern.search(dice)
        if match:
            number_of_dices = int(match.group('number_of_dices'))
            dice_number = int(match.group('dice_number'))
        else:
            raise ValueError("The rolled expect a parameter of the type NdM")

    return [randint(1, dice_number) for i in range(0,number_of_dices)]


def roll_dice(bot, update, args):
    """
    /roll
    /roll n
    /roll ndm
    """

    dice = "2d6"

    if len(args) == 0:
        modificator = 0
    else:
        try:
            modificator = int(args[0])
            if modificator > 10 or modificator < -10:
                update.message.reply_text(bad_response_rand(update))
                return
        except ValueError:
            update.message.reply_text(bad_response_rand(update))
            return
            #bot.sendMessage(chat_id=update.message.chat_id, text="Daniel, eres retrasado")
            #return

    try:
        dices_results = roll_dices_results(dice)
    except ValueError as e:
        bot.sendMessage(chat_id=update.message.chat_id, text=str(e))

    result = sum(dices_results)
    tot_result = result + modificator
    if modificator >= 0:
        text = "You rolled {} = {} + {} = {}".format(
            dices_results, result, modificator, tot_result)
    else:
        text = "You rolled {} = {} - {} = {}".format(
            dices_results, result, -1*modificator, tot_result)

    bot.sendMessage(chat_id=update.message.chat_id, text=text)

    if tot_result <= 6:
        resolution = "Fracaso :("
    elif tot_result <= 9:
        resolution = "Exito parcial"
    else:
        resolution = "Exito!"

    bot.sendMessage(chat_id=update.message.chat_id, text=resolution)


