import math
import pygame.math
from ship import Ship
from settings import *


class Player(Ship):
    """ Корабль, которым управляет игрок"""

    def __init__(self, pos, groups):
        # загружается изображение игрока и поворачивается в желаемое начальное положение
        loaded_image = pygame.image.load("../graphics/playerShip1_orange.png").convert_alpha()
        self.initial_image = pygame.transform.rotate(loaded_image, -90)
        super().__init__(pos, groups, self.initial_image)


    def update(self):

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

        direction_change *= self.acceleration

        self.velocity += direction_change

        # Устанавливается предел на величину получившейся скорости
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # "Сопротивление среды" - по-компонентно уменьшает скорость
        # (на постоянную величину, но не больше величины скорости)
        if self.velocity.x > 0:
            self.velocity.x = max(self.velocity.x - 0.1, 0)
        else:
            self.velocity.x = min(self.velocity.x + 0.1, 0)
        if self.velocity.y > 0:
            self.velocity.y = max(self.velocity.y - 0.1, 0)
        else:
            self.velocity.y = min(self.velocity.y + 0.1, 0)

        # Изменение координат игрока
        self.rect.centerx += round(self.velocity.x)
        self.rect.centery += round(self.velocity.y)

        # Поворот изображения игрока в направлении движения
        if self.velocity.magnitude() != 0:
            old_center = self.rect.center
            angle = -180 * math.atan2(self.velocity.y, self.velocity.x) / math.pi

            self.image = pygame.transform.rotate(self.initial_image, angle)
            self.rect = self.image.get_rect(center=old_center)
