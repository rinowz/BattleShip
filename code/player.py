""" Класс PLayer"""
import math
import pygame.math
from ship_like import ShipLike
from settings import *
from support import *


class Player(ShipLike):
    """ Корабль, которым управляет игрок"""

    def __init__(self, collidable_sprites, player_info, projectile_info):
        """
        :param collidable_sprites: группа содержащая спрайты,
        с которыми игрок будет "сталкиваться" - не проходить насквозь
        :param player_info: начальная информация об игроке
        :param projectile_info: информация о выпускаемых при выстреле снарядах
        """
        super(Player, self).__init__(player_info, projectile_info)

        # изначальное изображение положением вправо
        self.angle = -math.pi

        self.collidable_sprites = collidable_sprites

    def update(self, dt):
        """
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты."""

        super(Player, self).update(dt)

    def set_velocity(self, dt):
        """ Определяет какая скорость должна быть у игрока в данный момент
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты."""

        # Определяется изменение к вектору скорости, которое пользователь задает нажатием клавиш
        keys = pygame.key.get_pressed()
        direction_change = pygame.math.Vector2()

        if keys[CONTROLS['up']]:
            direction_change.y = -1
        elif keys[CONTROLS['down']]:
            direction_change.y = 1

        if keys[CONTROLS['left']]:
            direction_change.x = -1
        elif keys[CONTROLS['right']]:
            direction_change.x = 1

        if direction_change.magnitude() != 0:
            direction_change = direction_change.normalize()

        self.velocity_change = direction_change * self.acceleration * dt

        super().set_velocity(dt)

    def to_shoot(self):
        """
        Определяет нужно ли выстрелить
        :return: True или False
        """
        keys = pygame.key.get_pressed()

        if keys[CONTROLS['shoot']]:
            return True

        return False

