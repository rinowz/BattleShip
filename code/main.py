"""
Главный файл, который нужно запускать, чтобы запустить игру.

"""
import pygame
from settings import *
from support import *
from level import Level
import time


class Game:
    """ Класс содержащий в себе всю работу игры"""

    def __init__(self):
        """ Запускается pygame и устанавливаются необходимые переменные"""

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(get_loc_value("game_name"))

        self.clock = pygame.time.Clock()
        self.running = True
        # состояние игры - сцена, которая должна отображаться
        self.state = DEFAULT_STATE
        self.level = Level()
        self.prev_time = time.time()

    def run(self):
        """ Основной цикл pygame"""

        while self.running:
            # обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # меняем игру и рисуем что нужно
            dt = time.time() - self.prev_time
            self.prev_time = time.time()

            self.screen.fill(BLACK)
            self.update(dt)

            # обновление
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def update(self, dt):
        """ Внести изменения в игру в зависимости от сцены
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты.
        """

        if self.state == "play":
            self.level.run(dt)


game = Game()
game.run()
