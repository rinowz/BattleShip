import pygame
from button import Button
from settings import *
from scene import Scene
from pygame import mixer
from support import *


class MainMenu(Scene):
    def __init__(self, game):
        """
        :param game: Объект игры, из которого достаются необходимые переменные
        """
        super().__init__(game)

        self.loc_data = game.loc_values['main_menu']

        self.buttons = []

        self.button_sound = mixer.Sound(os.path.join(os.getcwd(), '..', 'sound', 'buttonclick.mp3'))
        self.button_image = load_image(os.path.join('menu', 'buttonBlue.png'))

        self.background_surf = load_image('backgrounds/background_menu.png')

    def run(self, dt, mouse_click):
        super(MainMenu, self).run(dt, mouse_click)

        for button in self.buttons:
            button.update(mouse_click)

    def toggle_pause(self):
        self.change_game_state('exit')

    def finish_initialization(self):
        """ Создает все элементы экрана"""
        self.display_surface.fill(BLUE)
        self.background_setup()

        game_name_font = pygame.font.SysFont('Times New Roman', 100)
        game_name_text = game_name_font.render(self.loc_data['game_name'], True, WHITE)
        game_name_rect = game_name_text.get_rect(center=(WIDTH * 0.5, HEIGHT * 0.15))
        self.display_surface.blit(game_name_text, game_name_rect)

        button_size = (WIDTH*0.3, HEIGHT*0.1)
        button_font = pygame.font.SysFont('Times New Roman', 50)

        first_h = HEIGHT*0.5 - 1.2*button_size[1]
        button_space = 1.2*button_size[1]

        self.buttons.append(
            Button((WIDTH*0.5, first_h), size=button_size,
                   text=self.loc_data['play'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('play'), sound=self.button_sound, image=self.button_image,
                   hover_image=self.button_image))
        self.buttons.append(
            Button((WIDTH*0.5, first_h + button_space), size=button_size,
                   text=self.loc_data['about'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('about'), sound=self.button_sound, image=self.button_image,
                   hover_image=self.button_image))
        self.buttons.append(
            Button((WIDTH*0.5, first_h + 2*button_space), size=button_size,
                   text=self.loc_data['how_to_play'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('how_to_play'), sound=self.button_sound,
                   image=self.button_image, hover_image=self.button_image))
        self.buttons.append(
            Button((WIDTH * 0.5, first_h + 3*button_space), size=button_size,
                   text=self.loc_data['settings'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('settings'), sound=self.button_sound,
                   image=self.button_image, hover_image=self.button_image))
        self.buttons.append(
            Button((WIDTH * 0.5, first_h + 4*button_space), size=button_size,
                   text=self.loc_data['exit'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('exit'), sound=self.button_sound,
                   image=self.button_image, hover_image=self.button_image))

    def background_setup(self):
        first_pos = (0, 0)

        step_x = 256
        step_y = 256

        self.background_rects = []
        for x_index in range(0, 2+WIDTH//step_x):
            for y_index in range(0, 2+WIDTH//step_y):
                self.background_rects.append(
                    self.background_surf.get_rect(topleft=add_lists(first_pos, (step_x*x_index, step_y*y_index))))

        for rect in self.background_rects:
            self.display_surface.blit(self.background_surf, rect)
