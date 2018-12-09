import re
from random import randint

def roll_dices_results(dice="2d6"):
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

    return [randint(1, dice_number) for i in range(0, number_of_dices)]

dice = "2d6"
modificator = 2

dices_results = roll_dices_results(dice)
print(dices_results)
