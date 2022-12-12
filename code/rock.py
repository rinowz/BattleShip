""" Класс Rock"""
import pygame
from settings import *
from support import *
from exploding_object import ExplodingObject


class Rock(ExplodingObject):
    """ Камень, который рандомно летает и может сталкиваться с кораблями"""
    def __init__(self, pos, groups, collision_group, vel=(0, 0), radius=50):
        """
        :param pos: Позиция камня
        :param groups: Группы в которые входит данный спрайт
        :param collision_group: группа, при столкновении с элементами которой нужно взрываться
        :param vel: Вектор скорости с которой летит камень
        :param radius: Радиус камня
        """
        self.radius = radius

        image = pygame.Surface((2*self.radius, 2*self.radius))
        image.set_colorkey(BLACK)
        pygame.draw.circle(image, GREEN, image.get_rect().center, self.radius)

        super().__init__(pos, groups, collision_group, image, vel)

    def update(self, dt):
        """ Камень движется с постоянной скоростью
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты."""
        self.add_vel(dt)

        super(Rock, self).update()

        if not ((BORDERS[0][0] < self.rect.centerx < BORDERS[0][1]) and
                (BORDERS[1][0] < self.rect.centery < BORDERS[1][1])):
            self.explosion()
