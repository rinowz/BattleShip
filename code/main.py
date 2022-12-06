import pygame
from settings import *
from support import *
from level import Level


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

    def run(self):
        """ Основной цикл pygame"""

        while self.running:
            # обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # меняем игру и рисуем что нужно
            self.screen.fill(BLACK)
            self.update()

            # обновление
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def update(self):
        """ Внести изменения в игру в зависимости от сцены"""

        if self.state == "play":
            self.level.run()


game = Game()
game.run()
