""" Класс UI"""
import pygame
from settings import *
from support import *


class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()

        self.player = player

        self.pause_surf = pygame.Surface((WIDTH, HEIGHT))
        self.pause_surf.fill(ALMOST_WHITE)
        self.pause_surf.set_colorkey(ALMOST_WHITE)
        self.paused = False

        # загружаем числа для счетчика атомных бомб
        self.numbers = open_image_folder('../graphics/numbers', type='dict')

    def display_bar(self, value, max_value, color, background_color, pos):
        """
        Выводит шкалу на экран
        :param value: текущее значение
        :param max_value: максимальное значение шкалы
        :param color: цвет шкалы
        :param background_color: цвет фона шкалы
        :param pos: позиция шкалы с левого верхнего угла
        """

        width = HEALTH_BAR_WIDTH * value / max_value
        bar = pygame.Rect(add_lists(pos, (BORDER_WIDTH, BORDER_WIDTH)), (width, HEALTH_BAR_HEIGHT))
        background_bar = pygame.Rect(pos, (HEALTH_BAR_WIDTH + 2*BORDER_WIDTH, HEALTH_BAR_HEIGHT + 2*BORDER_WIDTH))

        pygame.draw.rect(self.display_surface, background_color, background_bar)
        pygame.draw.rect(self.display_surface, color, bar)

    def display(self):
        if self.paused:
            self.display_surface.blit(self.pause_surf, (0, 0))
            return

        self.display_bar(self.player.hp, self.player.max_hp, RED, BORDER_COLOR, HEALTH_BAR_POS)
        self.display_bar(self.player.nuclear_progress, self.player.max_nuclear_bar,
                         GREEN, BORDER_COLOR, NUCLEAR_BAR_POS)

        # вывести количество бомб
        if self.player.nuclear_count in range(1, 6):
            path = 'numeral'+str(int(self.player.nuclear_count))+'.png'
            self.display_surface.blit(self.numbers[path], NUCLEAR_COUNT_POS)
