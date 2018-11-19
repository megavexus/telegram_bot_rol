from random import randint
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

    return [randint(1, dice_number) for i in number_of_dices]

def roll_dice(bot, update, args):
    """
    /roll
    /roll n
    /roll ndm
    """

    if len(args) == 0:
        dice = "2d6"
    else:
        dice = args[0]
    try:
        dices_results = roll_dices_results(dice)
    except ValueError as e:
        bot.sendMessage(chat_id=update.message.chat_id, text=str(e))

    result = sum(dices_results)
    text = "You rolled {} = {}".format(dices_results, result)
    bot.sendMessage(chat_id=update.message.chat_id, text=text)

