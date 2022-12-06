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


