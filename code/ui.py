""" Класс UI"""
import pygame
from settings import *


class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()

        self.player = player
        self.health_bar_rect = pygame.Rect(HEALTH_BAR_POS[0], HEALTH_BAR_POS[1], HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)

    def display(self):
        width = HEALTH_BAR_WIDTH * self.player.hp / self.player.max_hp
        health_bar = self.health_bar_rect.copy()
        health_bar.width = width

        border = self.health_bar_rect.copy()
        border.width += 2*BORDER_WIDTH
        border.height += 2*BORDER_WIDTH
        border.center = self.health_bar_rect.center

        pygame.draw.rect(self.display_surface, BORDER_COLOR, border)
        pygame.draw.rect(self.display_surface, HEALTH_BAR_COLOR, health_bar)
