"""
Класс, хранящий начальные данные для объекта.
А также для кораблей и отдельно для игрока с загрузкой изображения игрока.
"""
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


class ShipInfo(ObjectInfo):
    """ Информация об объекте ShipLike"""
    def __init__(self, pos, groups, image=pygame.Surface((50, 50)), vel=(0, 0), layer_change=useless,
                 attack_cooldown=PLAYER_COOLDOWN, max_speed=PLAYER_MAX_SPEED, acceleration=PLAYER_ACCELERATION, hp=100):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        :param layer_change: - функция изменения слоя объекта
        :param attack_cooldown: время, которое занимает кулдаун при атаке
        :param max_speed: максимальная скорость
        :param acceleration: насколько меняется скорость, когда корабль пытается ее изменить
        """
        super().__init__(pos, groups, image, vel, layer_change)

        self.attack_cooldown = attack_cooldown
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.hp = hp


class PlayerInfo(ShipInfo):
    """ Информация о создаваемом игроке"""

    def __init__(self, pos, groups, vel=(0, 0), layer_change=useless):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        :param layer_change: - функция изменения слоя объекта
        """
        loaded_image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        image = pygame.transform.rotate(loaded_image, -90)

        super(PlayerInfo, self).__init__(pos, groups, image, vel, layer_change)
