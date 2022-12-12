""" Класс Object"""
import pygame.sprite
from support import *


class Object(pygame.sprite.Sprite):
    """ Объект, который движется"""
    def __init__(self, pos, groups, image=pygame.Surface((50, 50)), vel=(0, 0)):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        """
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = [0, 0]
        self.set_pos(pos)
        self.mask = pygame.mask.from_surface(self.image)

        # вектор скорости объекта
        self.velocity = pygame.Vector2(vel)

    def set_pos(self, pos):
        """
        Меняет значение self.pos на предоставляемое с изменением положения self.rect
        :param pos: Позиция которую нужно присвоить объекту
        :return: None
        """
        self.pos = pos
        self.rect.center = round_list(self.pos)

    def add_to_pos(self, increment):
        """
        Меняет значение позиции на вектор
        :param increment: итерируемый из двух элементов - сдвиг по осям x и y
        :return: None
        """
        self.set_pos(add_lists(self.pos, increment))

    def add_vel(self, dt):
        """ Добавляет скорость к позиции"""
        self.add_to_pos(multiply_list(self.velocity, dt))

    def hit(self, damage):
        """ Что происходит, когда объекту наносится урон"""
        pass
