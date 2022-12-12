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
        self.initial_image = self.image.copy()

        self.collidable_sprites = collidable_sprites

        self.shoot_time = pygame.time.get_ticks()
        self.can_attack = True
        self.attack_cooldown = PLAYER_COOLDOWN
        self.max_speed = PLAYER_MAX_SPEED
        self.acceleration = PLAYER_ACCELERATION

    def update(self, dt):
        """
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты."""
        # Определяет и устанавливает скорость игрока
        self.set_velocity(dt)

        keys = pygame.key.get_pressed()
        if keys[CONTROLS['shoot']] and self.can_attack:
            vel = BULLET_SPEED * pygame.math.Vector2(math.cos(self.angle), -math.sin(self.angle))
            self.shoot(self.pos, vel)
            self.shoot_time = pygame.time.get_ticks()
            self.can_attack = False

        # Изменение координат игрока
        self.add_vel(dt)

        # Поворот изображения игрока в направлении движения
        self.rotate_image()

        self.cooldown()

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
            self.angle = -math.atan2(self.velocity.y, self.velocity.x)

            self.image = pygame.transform.rotate(self.initial_image, math.degrees(self.angle))
            self.rect = self.image.get_rect(center=old_center)

    def cooldown(self):
        if not self.can_attack:
            if pygame.time.get_ticks() - self.shoot_time > self.attack_cooldown:
                self.can_attack = True
