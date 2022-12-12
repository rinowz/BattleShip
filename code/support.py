""" Дополнительные функции, которые упрощают работу"""
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
    Возвращает знак числа: 1 для положительных чисел, -1 для отрицательных, 0 для 0
    :param x: число
    :return: 1, -1, или 0
    """
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def round_list(input_values):
    """
    Округляет поэлементно элементы массива.
    :param input_values: список или что-то итерируемое с элементами, на которые действует round()
    :return: список из округленных элементов входных данных
    """
    rounded_values = []

    for item in input_values:
        rounded_values.append(round(item))

    return rounded_values


def add_lists(array1, array2):
    """
    Поэлементно применяет сложение к элементам двух итерируемых с одинаковыми индексами
    :param array1: первый массив
    :param array2: второй массив
    :return: список являющийся суммой двух массивов
    """
    n = min(len(array1), len(array2))

    sum_array = []

    for i in range(n):
        sum_array.append(array1[i] + array2[i])

    return sum_array


def multiply_list(input_array, number):
    """
    Умножает каждый элемент итерируемого на число.
    :param input_array: массив
    :param number: число
    :return: список из элементов массива умноженных на число
    """
    multiplied_array = []

    for item in input_array:
        multiplied_array.append(item * number)

    return multiplied_array


def minus(input_array):
    """
    Умножает на -1
    :param input_array: итерируемый, который нужно умножить
    :return: смотрите двумя строками ниже
    """
    return multiply_list(input_array, -1)
