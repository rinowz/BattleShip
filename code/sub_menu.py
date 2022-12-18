""" Класс SubMenu"""
from main_menu import MainMenu
from button import Button
from settings import *


class SubMenu(MainMenu):
    """ Сцена меню, в которую можно попасть из главного меню"""

    def toggle_pause(self):
        self.change_game_state('main_menu')

    def finish_initialization(self):
        """ Создает кнопку для возвращения в главное меню"""
        self.display_surface.fill(BLUE)

        button_font = pygame.font.SysFont('Times New Roman', 40)
        self.buttons.append(
            Button((WIDTH*0.02, HEIGHT*0.02), size=(WIDTH*0.13, HEIGHT*0.08),
                   text=self.loc_data['back'], text_color=WHITE, font=button_font,
                   on_click=lambda: self.change_game_state('main_menu'), pos_center=False))
