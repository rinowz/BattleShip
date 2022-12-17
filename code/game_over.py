""" Класс GameOver"""
import pygame.display
from pyvidplayer import Video
from settings import *
from button import Button


class GameOver:
    """ Сцена конца игры с результатом"""

    def __init__(self, game_result, change_game_state, localization_data):
        """
        :param game_result: Результат игры, соответственно которому нужно выводить что-то на экран
        :param change_game_state: функция изменения сцены игры
        :param localization_data: список с данными локализации
        """

        self.change_game_state = change_game_state
        self.result = game_result
        self.display_surface = pygame.display.get_surface()

        self.buttons = []
        self.loc_data = localization_data

        if game_result == 'victory':
            self.video = Video('../video/finalvideo.mp4')
            self.video.set_size((WIDTH, HEIGHT))
            self.playing_video = True
        else:
            self.playing_video = False
            self.initialize_game_over_screen()

    def run(self, mouse_click):
        if self.playing_video:
            if self.result == 'victory':
                self.video.draw(self.display_surface, (0, 0))
                if abs(self.video.get_pos() - self.video.duration) * \
                        self.video.frame_rate <= 1:
                    self.video.close()
                    self.playing_video = False
                    self.initialize_game_over_screen()
        else:
            for button in self.buttons:
                button.update(mouse_click)

    def display_game_over_text(self):
        """ Создает надпись о завершении игры"""
        game_over_font = pygame.font.SysFont('Times New Roman', 100)
        game_over_text = game_over_font.render(self.loc_data['game_over_'+self.result], True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH * 0.5, HEIGHT * 0.2))
        self.display_surface.blit(game_over_text, game_over_rect)

    def create_buttons(self):
        """ Создает кнопки на экране"""

        button_size = (WIDTH*0.3, HEIGHT*0.1)
        button_font = pygame.font.SysFont('Times New Roman', 50)

        self.buttons.append(
            Button((WIDTH*0.5, HEIGHT*0.5+0.25*button_size[1]), size=button_size,
                   text=self.loc_data['game_over_main_menu'], text_color=WHITE, font=button_font,
                   on_click=lambda: self.change_game_state('main_menu')))
        self.buttons.append(
            Button((WIDTH*0.5, HEIGHT*0.5+1.75*button_size[1]), size=button_size,
                   text=self.loc_data['game_over_restart'], text_color=WHITE, font=button_font,
                   on_click=lambda: self.change_game_state('play')))

    def initialize_game_over_screen(self):
        """ Производит создание необходимых элементов экрана после завершения видео"""
        self.display_game_over_text()
        self.create_buttons()
