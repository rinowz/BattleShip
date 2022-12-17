"""
Главный файл, который нужно запускать, чтобы запустить игру.

"""
import pygame
from settings import *
from support import *
from level import Level
import time
from game_over import GameOver


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
        self.state = DEFAULT_STATE
        self.level = Level(self.change_game_state)
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
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True

            # меняем игру и рисуем что нужно
            dt = time.time() - self.prev_time
            self.prev_time = time.time()

            self.update(dt, mouse_click)

            # обновление
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def update(self, dt, mouse_click):
        """ Внести изменения в игру в зависимости от сцены
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты.
        """

        if self.state == "play":
            self.level.run(dt)
        elif self.state == "game_over":
            self.game_over.run(mouse_click)

    def change_game_state(self, state):
        """ Меняет состояние игры"""
        self.state = state

        if self.state == 'play':
            self.level = Level(self.change_game_state)
        elif self.state == 'game_over':
            self.game_result = self.level.game_result
            self.game_over = GameOver(self.game_result, self.change_game_state, self.loc_values)


game = Game()
game.run()
