import pygame


class Scene:
    """ Сцена игры"""

    def __init__(self, game):
        # функция смены сцены
        self.change_game_state = game.change_game_state
        # устанавливаем поверхность, на которой отображается сцена
        self.display_surface = pygame.display.get_surface()

        self.finished_initialization = False

    def run(self, dt, mouse_click):
        """
        Обновляет сцену
        :param dt: время между кадрами
        :param mouse_click: нажата ли мышь
        """
        if not self.finished_initialization:
            self.finish_initialization()
            self.finished_initialization = True

    def toggle_pause(self):
        pass

    def finish_initialization(self):
        """ Заканчивает создание сцены в момент обновления"""
        pass
