import pytest
from rol_bot.dice import roll_dices_results

@pytest.mark.parametrize("dice, num_dices, dice_num", [
    ("2d6", 2, 6),
    ("1d10", 1, 10),
    ("10", 1, 10),
    ("30d6", 30, 6)
])
def test_roll_dices(dice, num_dices, dice_num):
    results = roll_dices_results(dice)
    assert len(results) == num_dices
    for dice_res in results:
        assert dice_res < dice_num