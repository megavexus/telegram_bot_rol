from random import randint
from .utils import bad_response_rand
import re
# D4, D6, D8, D10, D12, D20

def roll_dices_results(dice="6"):
    try:
        number_of_dices = 1
        dice_number = int(dice)
    except ValueError:
        pattern = re.compile(
            r"^(?P<number_of_dices>[0-9]+)d(?P<dice_number>[0-9]+)+$")
        match = pattern.search(dice)
        if match:
            number_of_dices = int(match.group('number_of_dices'))
            dice_number = int(match.group('dice_number'))
        else:
            raise ValueError("The rolled expect a parameter of the type NdM")
    try:
        return [randint(1, dice_number) for i in range(0,number_of_dices)]
    except:
        raise Exception(dice_number)


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
            corrector = int(args[1])
        except:
            corrector = 0
    try:
        dices_results = roll_dices_results(dice)
    except ValueError as e:
        bot.sendMessage(chat_id=update.message.chat_id, text=str(e))

    result = sum(dices_results)
    tot_result = result + modificator + corrector
    username = update.message.from_user.username

    msg_result = get_message_result(username, tot_result, modificator, corrector)
    #update.message.reply_text(text)
    #bot.sendMessage(chat_id=update.message.chat_id, text=text)

    resolution = evaluate_result(tot_result)
    update.message.reply_text(text + "\n" + resolution)
    #bot.sendMessage(chat_id=update.message.chat_id, text=resolution)


def get_message_result(username, tot_result, modificator, corrector):
    if modificator >= 0:
        text = "@{} rolled {} = {} + {}".format(
            username, dices_results, result, modificator)
    else:
        text = "@{} rolled {} = {} - {}".format(
            username, dices_results, result, -1*modificator)

    if corrector > 0:
        text += " + {}".format(corrector)
    elif corrector < 0:
        text += " - {}".format(-1*corrector)

    text += " = {}".format(tot_result)
    return text


def evaluate_result(tot_result):
    if tot_result <= 6:
        resolution = "Fracaso :("
    elif tot_result <= 9:
        resolution = "Exito parcial"
    else:
        resolution = "Exito!"
    return resolution
