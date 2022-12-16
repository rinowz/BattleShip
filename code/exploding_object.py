""" Класс ExplodingObject"""
import pygame
from object import Object
from support import *


class ExplodingObject(Object):
    """ Объект, который уничтожается при столкновении с другим объектом"""

    def __init__(self, object_info, collision_group):
        """
        :param object_info: информация о создаваемом объекте
        :param collision_group: группа, при столкновении с элементами которой нужно взрываться
        """
        super().__init__(object_info)

        self.collision_group = collision_group
        self.colliding_objects = []
        self.ignored_objects = {self}

        self.change_layer(-1)

    def update(self, dt):

        # Обновляем позицию объекта
        self.update_position(dt)

        # Находим столкновения
        self.find_collision()

        # если есть столкновение, взрываем себя
        if len(self.colliding_objects) > 0:
            self.explosion()

        # уничтожается при выходе за рамки игры
        if not ((BORDERS[0][0] < self.rect.centerx < BORDERS[0][1]) and
                (BORDERS[1][0] < self.rect.centery < BORDERS[1][1])):
            self.explosion()

    def find_collision(self):
        """ Меняет self.colliding_objects на объекты, с которыми есть столкновение"""

        # проверяем с чем может сталкиваться объект
        self.colliding_objects = pygame.sprite.spritecollide(self, self.collision_group, False)

        # убираем столкновение с игнорируемыми объектами
        ignored_objects = self.ignored_objects.copy()
        for ignored_object in ignored_objects:
            if ignored_object in self.colliding_objects:
                self.colliding_objects.remove(ignored_object)

        # более точно проверяем масками
        colliding_objects = self.colliding_objects.copy()
        for colliding_object in colliding_objects:
            if self.mask.overlap(colliding_object.mask, get_mask_offset(self, colliding_object)) is None:
                self.colliding_objects.remove(colliding_object)

    def explosion(self):
        """
        Убивает себя, перед этим нанося урон тому, чего касается
        """
        colliding_objects = self.colliding_objects.copy()
        for colliding_object in colliding_objects:
            if self.mask.overlap(colliding_object.mask, get_mask_offset(self, colliding_object)):
                colliding_object.hit(self)

        self.kill()

    def exclude_collision(self, object):
        """ Не проверяет столкновение с данным объектом"""
        self.ignored_objects.add(object)

    def exclude_collision_list(self, object_list):
        """
        Убирает столкновение с объектами из списка
        :param object_list: список игнорируемых объектов
        """
        for object in object_list:
            self.exclude_collision(object)

    def update_position(self, dt):
        """ Логика обновления координат. По умолчанию - прибавление скорости"""
        self.add_vel(dt)

    def hit(self, hitter):
        """
        Вызывается когда что-то сталкивается с объектом
        :param hitter: Объект, который вызывает столкновение
        """
        self.exclude_collision(hitter)
        self.find_collision()
        self.explosion()
