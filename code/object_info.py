""" Класс, хранящий начальные данные для объекта. А также отдельно для игрока с загрузкой изображения игрока"""
import pygame
from settings import *
from support import *


class ObjectInfo:
    """ Информация о создаваемом объекте"""

    def __init__(self, pos, groups, image=pygame.Surface((50, 50)), vel=(0, 0), layer_change=useless):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        :param layer_change: - функция изменения слоя объекта
        """
        self.pos = pos
        self.groups = groups
        self.image = image
        self.vel = vel
        self.layer_change = layer_change


class PlayerInfo(ObjectInfo):
    """ Информация о создаваемом игроке"""

    def __init__(self, pos, groups, vel=(0, 0), layer_change=useless):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        """
        loaded_image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        image = pygame.transform.rotate(loaded_image, -90)

        super(PlayerInfo, self).__init__(pos, groups, image, vel, layer_change)
