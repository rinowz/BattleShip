""" Класс Ship"""
import pygame
from support import *
from object import Object


class Ship(Object):
    """ Корабль - объект игрока или противника"""

    def __init__(self, pos, groups, image=pygame.Surface((50, 50)), vel=(0, 0)):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов
        """
        super().__init__(pos, groups, image, vel)

        # максимальное значение модуля скорости
        self.max_speed = 1000
        # модуль ускорения при попытке корабля изменить скорость в некотором направлении
        self.acceleration = 1200

