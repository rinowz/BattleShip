""" Класс, хранящий начальные данные для снаряда"""
import pygame
from object_info import ObjectInfo
from support import *


class ProjectileInfo:
    """ Информация о снаряде, выпускаемом при выстреле в ShipLike"""

    def __init__(self, groups, collision_group, image=pygame.Surface((10, 10)), layer_change=useless,
                 damage=PLAYER_DAMAGE):
        """
        :param groups: Группы, в которые должен входить снаряд
        :param collision_group: Группа, сталкиваясь с которой, снаряд взрывается
        :param image: surface изображения снаряда
        """
        self.groups = groups
        self.collision_group = collision_group
        self.image = image
        self.layer_change = layer_change
        self.damage = damage

    def get_object_info(self, pos, vel):
        """
        Создает экземпляр класса object_info основываясь на своих и переданных данных
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        """

        return ObjectInfo(pos, self.groups, self.image, vel, self.layer_change)
