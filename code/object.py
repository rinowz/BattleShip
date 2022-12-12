""" Класс Object"""
import pygame.sprite
from support import *


class Object(pygame.sprite.Sprite):
    """ Объект, который движется"""
    def __init__(self, object_info):
        """
        :param object_info: информация о создаваемом объекте
        """
        super().__init__(object_info.groups)
        self.image = object_info.image
        self.rect = self.image.get_rect()
        self.pos = [0, 0]
        self.set_pos(object_info.pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.layer_change = object_info.layer_change

        # Урон наносимый при атаке других объектов. Не совсем логичное место объявлять, но пусть будет на всякий случай
        self.damage = 1

        # вектор скорости объекта
        self.velocity = pygame.Vector2(object_info.vel)

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
        """ Добавляет скорость к позиции
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты."""
        self.add_to_pos(multiply_list(self.velocity, dt))

    def hit(self, damage):
        """ Что происходит, когда объекту наносится урон"""
        pass

    def change_layer(self, layer):
        """
        Меняет слой, на котором рисуется объект
        :param layer: номер слоя
        """
        self.layer_change(self, layer)
