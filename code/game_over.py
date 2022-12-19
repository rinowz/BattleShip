""" Класс GameOver"""
import pygame.display
from pyvidplayer import Video
from settings import *
from button import Button
from scene import Scene
from pygame import mixer
from support import *
import os


class GameOver(Scene):
    """ Сцена конца игры с результатом"""

    def __init__(self, game):
        """
        :param game: Объект игры, из которого достаются необходимые переменные
        """
        super(GameOver, self).__init__(game)

        self.result = game.game_result

        self.loc_data = game.loc_values['game_over']

        self.buttons = []
        self.create_buttons()
        self.display_buttons = False

        game_over_font = pygame.font.SysFont('Times New Roman', 100)
        self.game_over_text = game_over_font.render(self.loc_data[self.result], True, WHITE)
        self.game_over_rect = self.game_over_text.get_rect(center=(WIDTH * 0.5, HEIGHT * 0.2))

        if self.result == 'victory':
            self.video = Video(os.path.join(os.getcwd(), '..', 'video', 'final.mp4'))
            self.video.set_size((WIDTH, HEIGHT))
            self.playing_video = True
            self.finished_initialization = True
        else:
            self.playing_video = False

        pygame.mouse.set_visible(False)

        # используемая музыка
        self.music = {
            "victory": os.path.join(os.getcwd(), '..', 'sound', 'endgame.mp3'),
            "loss": os.path.join(os.getcwd(), '..', 'sound', 'gameover.mp3')}

    def run(self, dt, mouse_click):
        super(GameOver, self).run(dt, mouse_click)

        if self.playing_video and self.video:
            if self.result == 'victory' and not self.video.get_paused():
                self.video.draw(self.display_surface, (0, 0))
                if abs(self.video.get_pos() - self.video.duration) * \
                        self.video.frame_rate <= 1:
                    self.video.close()
                    self.playing_video = False
                    self.finished_initialization = False

        if self.display_buttons:
            for button in self.buttons:
                button.update(mouse_click)

    def toggle_pause(self):
        if self.playing_video and self.video:
            self.video.toggle_pause()

            if self.video.get_paused():
                self.finished_initialization = False
            else:
                pygame.mixer.music.stop()
                self.display_buttons = False
                pygame.mouse.set_visible(False)

    def display_game_over_text(self):
        """ Выводит надпись о завершении игры"""
        self.display_surface.blit(self.game_over_text, self.game_over_rect)

    def create_buttons(self):
        """ Создает кнопки на экране"""

        button_size = (WIDTH*0.3, HEIGHT*0.1)
        button_font = pygame.font.SysFont('Times New Roman', 50)

        first_h = HEIGHT*0.5-0.25*button_size[1]
        button_space = 1.4*button_size[1]

        sound = mixer.Sound(os.path.join(os.getcwd(), '..', 'sound', 'buttonclick.mp3'))

        button_image = load_image(os.path.join('menu', 'ButtonBlue.png'))

        self.buttons.append(
            Button((WIDTH*0.5, first_h), size=button_size,
                   text=self.loc_data['main_menu'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('main_menu'), sound=sound, image=button_image,
                   hover_image=button_image))
        self.buttons.append(
            Button((WIDTH*0.5, first_h + button_space), size=button_size,
                   text=self.loc_data['restart'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('play'), sound=sound, image=button_image,
                   hover_image=button_image))
        self.buttons.append(
            Button((WIDTH*0.5, first_h + 2*button_space), size=button_size,
                   text=self.loc_data['exit'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('exit'), sound=sound, image=button_image,
                   hover_image=button_image))

    def finish_initialization(self):
        """ Производит создание необходимых элементов экрана после завершения видео"""
        pygame.mixer.music.load(self.music[self.result])
        pygame.mixer.music.play()

        self.display_game_over_text()
        self.display_buttons = True
        pygame.mouse.set_visible(True)
