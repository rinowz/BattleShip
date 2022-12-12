""" Класс ShipLike"""
import pygame
from support import *
from object import Object
from exploding_object import ExplodingObject


class ShipLike(Object):
    """ Объект, похожий на корабль - то что может стрелять"""

    def __init__(self, object_info, projectile_info, hp=100):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param projectile_info: информация о выпускаемых при выстреле снарядах
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов
        """
        super().__init__(object_info)

        self.projectile_info = projectile_info

        # максимальное значение модуля скорости
        self.max_speed = 1000
        # модуль ускорения при попытке корабля изменить скорость в некотором направлении
        self.acceleration = 1200

        self.hp = hp

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

    def shoot(self, position, velocity):
        """ Стреляет объектом типа ExplodingObject"""
        projectile = ExplodingObject(self.projectile_info.get_object_info(position, velocity),
                                     self.projectile_info.collision_group)
        projectile.exclude_collision(self)
