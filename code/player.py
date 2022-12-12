""" Класс PLayer"""
import math
import pygame.math
from ship import Ship
from settings import *
from support import *


class Player(Ship):
    """ Корабль, которым управляет игрок"""

    def __init__(self, pos, groups, collidable_sprites):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param collidable_sprites: группа содержащая спрайты,
        с которыми игрок будет "сталкиваться" - не проходить насквозь
        """

        # загружается изображение игрока и поворачивается в желаемое начальное положение
        loaded_image = pygame.image.load("../graphics/ship2.0.png").convert_alpha()
        self.initial_image = pygame.transform.rotate(loaded_image, -90)
        self.collidable_sprites = collidable_sprites
        super().__init__(pos, groups, self.initial_image)

    def update(self, dt):
        """
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты."""
        # Определяет и устанавливает скорость игрока
        self.set_velocity(dt)

        # Изменение координат игрока
        self.add_vel(dt)

        # Поворот изображения игрока в направлении движения
        self.rotate_image()

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

        direction_change *= self.acceleration * dt

        self.velocity = pygame.math.Vector2(add_lists(self.velocity, direction_change))

        # "Сопротивление среды" - по-компонентно уменьшает скорость
        # (на постоянную величину, но не больше величины скорости)
        resistance = 300 * dt
        if self.velocity.x > 0:
            self.velocity.x = max(self.velocity.x - resistance, 0)
        else:
            self.velocity.x = min(self.velocity.x + resistance, 0)
        if self.velocity.y > 0:
            self.velocity.y = max(self.velocity.y - resistance, 0)
        else:
            self.velocity.y = min(self.velocity.y + resistance, 0)

        # Устанавливается предел на величину получившейся скорости
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def rotate_image(self):
        """ Поворачивает начальное изображение на угол отклонения скорости от вертикального направления вверх"""
        if self.velocity.magnitude() != 0:
            old_center = self.rect.center
            angle = -180 * math.atan2(self.velocity.y, self.velocity.x) / math.pi

            self.image = pygame.transform.rotate(self.initial_image, angle)
            self.rect = self.image.get_rect(center=old_center)
