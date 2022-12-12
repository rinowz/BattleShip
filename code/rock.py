""" Класс Rock"""
import pygame
from settings import *
from support import *
from object import Object


class Rock(Object):
    """ Камень, который рандомно летает и может сталкиваться с кораблями"""
    def __init__(self, pos, groups, vel=(0, 0), radius=50):
        """
        :param pos: Позиция камня
        :param groups: Группы в которые входит данный спрайт
        :param vel: Вектор скорости с которой летит камень
        :param radius: Радиус камня
        """
        self.radius = radius

        image = pygame.Surface((2*self.radius, 2*self.radius))
        image.set_colorkey(BLACK)
        pygame.draw.circle(image, GREEN, image.get_rect().center, self.radius)

        super(Rock, self).__init__(pos, groups, image, vel)

    def update(self, dt):
        """ Камень движется с постоянной скоростью"""
        self.add_vel(dt)

        if not ((BORDERS[0][0] < self.rect.centerx < BORDERS[0][1]) and
                (BORDERS[1][0] < self.rect.centery < BORDERS[1][1])):
            self.kill()
