""" Класс ShipLike"""
import pygame
from support import *
from object import Object
from exploding_object import ExplodingObject
import math


class ShipLike(Object):
    """ Объект, похожий на корабль - то что может стрелять"""

    def __init__(self, ship_info, projectile_info):
        """
        :param ship_info: информация о создаваемом корабле
        :param projectile_info: информация о выпускаемых при выстреле снарядах
        """
        super().__init__(ship_info)

        # для поворота объекта
        self.angle = get_angle(self.velocity)
        self.initial_image = self.image.copy()

        self.projectile_info = projectile_info

        # максимальное значение модуля скорости
        self.max_speed = ship_info.max_speed
        # модуль ускорения при попытке корабля изменить скорость в некотором направлении
        self.acceleration = ship_info.acceleration
        # Текущее значение, на которое меняется скорость
        self.velocity_change = pygame.math.Vector2()

        self.max_hp = ship_info.hp
        self.hp = self.max_hp

        # кулдаун стрельбы
        self.shoot_time = pygame.time.get_ticks()
        self.can_attack = True
        self.attack_cooldown = ship_info.attack_cooldown

        self.damage += projectile_info.damage

        # Объекты, которые игнорируются выпускаемыми снарядами
        self.no_hit_objects = [self]

    def update(self, dt, change_vel=True, add_vel=True, shoot_check=True, rotate=True, cooldown=True):
        """
        :param dt: Время между кадрами
        :param change_vel: нужно ли определять скорость
        :param add_vel: нужно ли добавлять скорость к позиции
        :param shoot_check: нужно ли обрабатывать выстрел
        :param rotate: нужно ли поворачивать изображение
        :param cooldown: нужно лит следить за кулдауном
        """
        # Определяет и устанавливает скорость корабля
        if change_vel:
            self.set_velocity(dt)

        # Изменение координат корабля
        if add_vel:
            self.add_vel(dt)

        # Обработка выстрела
        if shoot_check:
            self.shooting()

        # Поворот изображения игрока в направлении движения
        if rotate:
            self.rotate_image()

        if cooldown:
            self.cooldown()

    def add_vel(self, dt):
        super().add_vel(dt)

        if self.pos[0] < BORDERS[0][0]:
            self.set_pos((BORDERS[0][0], self.pos[1]))
        if self.pos[0] > BORDERS[0][1]:
            self.set_pos((BORDERS[0][1], self.pos[1]))
        if self.pos[1] < BORDERS[1][0]:
            self.set_pos((self.pos[0], BORDERS[1][0]))
        if self.pos[1] > BORDERS[1][1]:
            self.set_pos((self.pos[0], BORDERS[1][1]))

    def hit(self, hitter):
        """
        Нанесение урона объекту
        :param hitter: объект, вызвавший повреждение
        """
        self.hp -= hitter.damage

        if self.hp <= 0:
            self.destroy()

    def destroy(self):
        """ Уничтожение объекта"""
        self.kill()

    def shoot(self, info=None):
        """ Стреляет объектом типа ExplodingObject"""

        if info is None:
            info = self.projectile_info

        projectile_vel = info.speed * pygame.math.Vector2(math.cos(self.angle), -math.sin(self.angle))

        projectile = ExplodingObject(info.get_object_info(self.pos, projectile_vel),
                                     info.collision_group)
        projectile.exclude_collision_list(self.no_hit_objects)

    def shooting(self, info=None, ignore_to_shoot=False):
        """
        Вызывается для произведения выстрела
        :return: True если выстрел произведен
        """
        if self.can_attack and (self.to_shoot() or ignore_to_shoot):
            self.shoot(info)

            # устанавливаем кулдаун
            self.shoot_time = pygame.time.get_ticks()
            self.can_attack = False

            return True
        return False

    def rotate_image(self):
        """ Поворачивает начальное изображение на угол отклонения скорости от вертикального направления вверх"""
        if self.velocity.magnitude() != 0:
            old_center = self.pos
            self.angle = get_angle(self.velocity)

            self.image = pygame.transform.rotate(self.initial_image, math.degrees(self.angle))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.set_pos(old_center)

    def cooldown(self):
        """ Дает возможность атаковать по прошествии кулдауна"""
        if not self.can_attack:
            if pygame.time.get_ticks() - self.shoot_time > self.attack_cooldown:
                self.can_attack = True

    # Должно определяться наследниками
    def to_shoot(self):
        """
        Определяет нужно ли выстрелить
        :return: True или False
        """
        return False

    def set_velocity(self, dt):
        """ Устанавливает необходимую скорость корабля"""

        self.velocity = pygame.math.Vector2(add_lists(self.velocity, self.velocity_change))

        # "Сопротивление среды" - по-компонентно уменьшает скорость
        # (на постоянную величину, но не больше величины скорости)
        if self.velocity.magnitude() != 0:
            resistance = self.velocity.normalize() * 300 * dt

            if self.velocity.x > 0:
                self.velocity.x = max(self.velocity.x - resistance.x, 0)
            else:
                self.velocity.x = min(self.velocity.x - resistance.x, 0)
            if self.velocity.y > 0:
                self.velocity.y = max(self.velocity.y - resistance.y, 0)
            else:
                self.velocity.y = min(self.velocity.y - resistance.y, 0)

        # Устанавливается предел на величину скорости
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
