""" Главный файл, который нужно запускать, чтобы запустить игру."""
import pygame
from settings import *
from support import *
from level import Level
import time
from game_over import GameOver
from main_menu import MainMenu
from menu_about import About
from menu_how_to_play import HowToPlay
from menu_settings import Settings


class Game:
    """ Класс содержащий в себе всю работу игры"""

    def __init__(self):
        """ Запускается pygame и устанавливаются необходимые переменные"""

        self.loc_values = get_loc_values()

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(self.loc_values["game_name"])

        self.clock = pygame.time.Clock()
        self.running = True
        # состояние игры - сцена, которая должна отображаться
        self.change_game_state(DEFAULT_STATE)

        self.prev_time = time.time()
        # self.game_over = GameOver('victory', self.change_game_state, self.loc_values)

    def run(self):
        """ Основной цикл pygame"""

        while self.running:
            # обработка событий
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.scene.toggle_pause()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True

            # задаем время между кадрами
            dt = time.time() - self.prev_time
            self.prev_time = time.time()

            # меняем игру и рисуем что нужно
            self.scene.run(dt, mouse_click)

            # обновление
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def change_game_state(self, state):
        """ Меняет состояние игры"""
        self.state = state

        if self.state == 'exit':
            self.running = False
        elif self.state == 'play':
            self.scene = Level(self)
        elif self.state == 'game_over':
            self.game_result = self.scene.game_result
            self.scene = GameOver(self)
        elif self.state == 'main_menu':
            self.scene = MainMenu(self)
        elif self.state == 'about':
            self.scene = About(self)
        elif self.state == 'how_to_play':
            self.scene = HowToPlay(self)
        elif self.state == 'settings':
            self.scene = Settings(self)


game = Game()
game.run()
