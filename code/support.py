import json
from settings import *


def get_loc_value(key):
    """
    Возвращает значение, соответствующее строке, на используемом языке.
    Например, для "game_name" - название игры

    :param key: строка, значение которой нужно получить
    :return: значение в переводе на язык, который установлен в данный момент
    """

    with open("../localization/" + LANGUAGE + ".json", "r") as loc_file:
        value = json.load(loc_file).get(key, str(key)+' value not found in ' + LANGUAGE + ' localization')

    return value


def sign(x):
    """
    Возвращает знак числа x: 1 для положительных чисел, -1 для отрицательных, 0 для 0
    :param x: число
    :return: 1, -1, или 0
    """

    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

