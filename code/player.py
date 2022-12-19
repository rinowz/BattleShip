""" Класс PLayer"""
import math
import random
import pygame.math
from ship_like import ShipLike
from settings import *
from support import *
from exploding_object import ExplodingObject
from player_projectile import PlayerProjectile


class Player(ShipLike):
    """ Корабль, которым управляет игрок"""

    def __init__(self, collidable_sprites, player_info, projectile_info, nuclear_rocket_info, bomb_part_group):
        """
        :param collidable_sprites: группа содержащая спрайты,
        с которыми игрок будет "сталкиваться" - не проходить насквозь
        :param player_info: начальная информация об игроке
        :param projectile_info: информация о выпускаемых при выстреле снарядах
        :param nuclear_rocket_info: информация о ядерной бомбе
        """
        super(Player, self).__init__(player_info, projectile_info)

        self.nuclear_shot = False
        self.nuclear_sound = mixer.Sound('../sound/flight.mp3')

        # изначальное изображение положением вправо
        self.angle = 0

        self.collidable_sprites = collidable_sprites

        self.nuclear_info = nuclear_rocket_info
        # Количество ядерных боеголовок
        self.nuclear_count = 0
        self.max_nuclear_count = 5
        # значение шкалы сбора ядерных боеголовок
        self.nuclear_progress = 0
        self.max_nuclear_bar = 15

        self.bomb_part_group = bomb_part_group

    def update(self, dt):
        """
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты."""
        super(Player, self).update(dt)

        bomb_part_sprites = pygame.sprite.spritecollide(self, self.bomb_part_group, False).copy()

        for sprite in bomb_part_sprites:
            if self.nuclear_count < self.max_nuclear_count:
                sprite.kill()
                self.nuclear_progress += random.uniform(3, 5)

                if self.nuclear_progress >= self.max_nuclear_bar:
                    self.nuclear_count += int(self.nuclear_progress / self.max_nuclear_bar)
                    self.nuclear_progress = self.nuclear_progress % self.max_nuclear_bar

                print(self.nuclear_count)
                print(self.nuclear_progress)

        # обработка запуска ядерной бомбы
        self.nuclear_launch()

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

    def shoot(self, info=None):
        """ Стреляет объектом типа PlayerProjectile"""

        if self.nuclear_shot:
            self.nuclear_sound.play()
        else:
            self.shot_sound.play()

        if info is None:
            info = self.projectile_info

        projectile_vel = info.speed * pygame.math.Vector2(math.cos(self.angle), -math.sin(self.angle))

        projectile = PlayerProjectile(info.get_object_info(self.pos, projectile_vel, angle=self.angle),
                                     info.collision_group)
        projectile.exclude_collision_list(self.no_hit_objects)

    def nuclear_launch(self):
        """ Проверяет и производит запуск ядерной бомбы"""
        keys = pygame.key.get_pressed()
        if keys[CONTROLS['nuclear_launch']] and self.nuclear_count > 0:
            self.nuclear_shot = True
            if self.shooting(self.nuclear_info, True):
                self.nuclear_count -= 1
            self.nuclear_shot = False

    def hit(self, hitter):
        """
        Нанесение урона игроку
        :param hitter: объект, вызвавший повреждение
        """
        self.hp -= hitter.damage

        if self.hp <= 0:
            self.destroy()
        else:
            self.hit_sound.play()
