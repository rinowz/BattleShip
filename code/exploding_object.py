""" Класс ExplodingObject"""
import pygame
from object import Object
from support import *


class ExplodingObject(Object):
    """ Объект, который уничтожается при столкновении с другим объектом"""

    def __init__(self, pos, groups, collision_group, image=pygame.Surface((50, 50)), vel=(0, 0)):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param collision_group: группа, при столкновении с элементами которой нужно взрываться
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        """

        super().__init__(pos, groups, image, vel)

        self.collision_group = collision_group
        self.colliding_objects = []
        self.damage = 1

    def update(self):

        # проверяем с чем может сталкиваться объект
        self.colliding_objects = pygame.sprite.spritecollide(self, self.collision_group, False)

        # убираем столкновение с собой
        if self in self.colliding_objects:
            self.colliding_objects.remove(self)

        # более точно проверяем масками
        for object in self.colliding_objects:
            if self.mask.overlap(object.mask, get_mask_offset(self, object)) is None:
                self.colliding_objects.remove(object)

        # если есть столкновение, взрываем себя
        if len(self.colliding_objects) > 0:
            self.explosion()

    def explosion(self):
        """
        Убивает себя, перед этим нанося урон тому, чего касается
        :param colliding_objects: объекты, с которыми есть столкновение
        """
        for object in self.colliding_objects:
            if self.mask.overlap(object.mask, get_mask_offset(self, object)):
                object.hit(self.damage)

        self.kill()



