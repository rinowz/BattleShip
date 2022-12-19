""" Дополнительные функции, которые упрощают работу"""
import json
import math
from settings import *
import os
from pygame import mixer


def get_loc_values():
    """
    Возвращает значения из файла локализации.
    :return: словарь на языке, который установлен в данный момент
    """

    with open("../localization/" + LANGUAGE + ".json", "r") as loc_file:
        values = json.load(loc_file)

    return values


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


def get_mask_offset(obj1, obj2):
    """
    Возвращает расстояние между левыми верхними углами масок(на самом деле rect).
    :param obj1: объект, из которого выходит расстояние
    :param obj2: объект, в который входит расстояние
    :return: список из координат x и y
    """

    return add_lists(obj2.rect.topleft, minus(obj1.rect.topleft))


def build_layer_change_function(layer_group):
    """
    Создает функцию, которая меняет слой в группе
    :param layer_group: группа LayeredUpdates в которой нужно изменить слой
    :return: Функция, которая принимает объект и номер слой и меняет слой объекта в layer_group
    """

    def change_layer(sprite, layer):
        """
        Меняет слой объекта
        :param sprite: объект, слой которого нужно изменить
        :param layer: номер слоя
        :return: None
        """
        if sprite in layer_group:
            layer_group.change_layer(sprite, layer)

    return change_layer


def useless(_, __):
    """ Функция, которая принимает два аргумента и ничего не делает. Используется при отсутствии функции layer_change"""
    pass


def get_angle(direction):
    """
    Находит угол, который направление составляет с горизонтом
    :param direction: итерируемый из двух элементов - направление по x и y
    :return: угол в радианах
    """
    if direction[0] == 0:
        return -sign(direction[1]) * math.pi / 2

    return -math.atan2(direction[1], direction[0])


def get_direction(angle):
    """
    Находит вектор направления от угла с горизонтом
    :param angle: угол отклонения от нуля, который справа, против часовой стрелки при выводе изображения
    :return: единичный вектор в направлении, заданном углом
    """
    return pygame.math.Vector2(math.cos(angle), -math.sin(angle))


def open_image_folder(path, type='list'):
    """
    Загружает изображения из папки
    :param path:
    :type: тип возвращаемого значения - list или dict
    :return: массив из Surface изображений
    """
    if type == 'list':
        images = []
    else:
        images = {}

    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            image = pygame.image.load(os.path.join(dirpath, filename)).convert_alpha()

            if type == 'list':
                images.append(image)
            else:
                images[filename] = image

    return images


def load_image(path, angle=0):
    """
    Сокращает вызов загрузки изображения
    :param path: путь к изображению относительно папки graphics
    :param angle: угол, на который нужно повернуть изображение в градусах
    :return: surface изображения
    """

    image_surf = pygame.image.load("../graphics/"+path)
    if ".png" in path:
        image_surf = image_surf.convert_alpha()

    if angle != 0:
        image_surf = pygame.transform.rotate(image_surf, angle)

    return image_surf


def generate_multiple(number, generating_function):
    """
    Создает необходимое количество объектов
    :param number: количество объектов которые нужно создать
    :param generating_function: функция создающая необходимые объекты
    :return: список из объектов
    """
    generated_objects = []

    for i in range(number):
        generated_object = generating_function()
        if generated_object:
            generated_objects.append(generated_object)

    return generated_objects


def change_cursor(colored=False):
    if colored:
        pygame.mouse.set_cursor(COLORED_CURSOR)
    elif not colored:
        pygame.mouse.set_cursor(GRAY_CURSOR)
