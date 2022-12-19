""" Класс UI"""
import pygame
from settings import *
from support import *
from button import Button


class UI:
    def __init__(self, player, loc_data, change_game_state, toggle_pause):
        self.display_surface = pygame.display.get_surface()

        self.player = player

        # данные локализации
        self.loc_data = loc_data['pause_menu']

        self.toggle_pause = toggle_pause

        self.initialize_pause_surf()
        self.paused = False

        # загружаем числа для счетчика атомных бомб
        self.numbers = open_image_folder(os.path.join(os.getcwd(), '..', 'graphics', 'numbers'), type='dict')

        self.change_game_state = change_game_state

    def display_bar(self, value, max_value, color, background_color, pos):
        """
        Выводит шкалу на экран
        :param value: текущее значение
        :param max_value: максимальное значение шкалы
        :param color: цвет шкалы
        :param background_color: цвет фона шкалы
        :param pos: позиция шкалы с левого верхнего угла
        """

        width = HEALTH_BAR_WIDTH * value / max_value
        bar = pygame.Rect(add_lists(pos, (BORDER_WIDTH, BORDER_WIDTH)), (width, HEALTH_BAR_HEIGHT))
        background_bar = pygame.Rect(pos, (HEALTH_BAR_WIDTH + 2*BORDER_WIDTH, HEALTH_BAR_HEIGHT + 2*BORDER_WIDTH))

        pygame.draw.rect(self.display_surface, background_color, background_bar)
        pygame.draw.rect(self.display_surface, color, bar)

    def initialize_pause_surf(self):
        """ Создает поверхность экрана паузы"""
        self.pause_surf = pygame.Surface((WIDTH, HEIGHT))
        self.pause_surf.fill(ALMOST_WHITE)
        self.pause_surf.set_colorkey(ALMOST_WHITE)

        paused_font = pygame.font.SysFont('Times New Roman', 80, italic=True)
        paused_text = paused_font.render(self.loc_data['paused'], True, WHITE)
        paused_text_rect = paused_text.get_rect(center=(WIDTH * 0.5, HEIGHT * 0.15))

        self.pause_surf.blit(paused_text, paused_text_rect)

        self.buttons = []

        button_size = (WIDTH*0.3, HEIGHT*0.1)
        button_font = pygame.font.SysFont('Times New Roman', 50)

        first_h = HEIGHT*0.5-1.25*button_size[1]
        button_space = 1.4*button_size[1]

        sound = mixer.Sound(os.path.join(os.getcwd(), '..', 'sound', 'buttonclick.mp3'))

        button_image = load_image(os.path.join('menu', 'ButtonBlue.png'))

        self.buttons.append(
            Button((WIDTH*0.5, first_h), size=button_size,
                   text=self.loc_data['resume'], text_color=BLUE, font=button_font,
                   on_click=self.toggle_pause, sound=sound, image=button_image,
                   hover_image=button_image))
        self.buttons.append(
            Button((WIDTH*0.5, first_h + button_space), size=button_size,
                   text=self.loc_data['main_menu'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('main_menu'), sound=sound, image=button_image,
                   hover_image=button_image))
        self.buttons.append(
            Button((WIDTH*0.5, first_h + 2*button_space), size=button_size,
                   text=self.loc_data['restart'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('play'), sound=sound, image=button_image,
                   hover_image=button_image))
        self.buttons.append(
            Button((WIDTH*0.5, first_h + 3*button_space), size=button_size,
                   text=self.loc_data['exit'], text_color=BLUE, font=button_font,
                   on_click=lambda: self.change_game_state('exit'), sound=sound, image=button_image,
                   hover_image=button_image))

    def display(self, mouse_click):
        if self.paused:
            for button in self.buttons:
                button.update(mouse_click)

            self.display_surface.blit(self.pause_surf, (0, 0))
            return

        self.display_bar(self.player.hp, self.player.max_hp, RED, BORDER_COLOR, HEALTH_BAR_POS)
        self.display_bar(self.player.nuclear_progress, self.player.max_nuclear_bar,
                         GREEN, BORDER_COLOR, NUCLEAR_BAR_POS)

        # вывести количество бомб
        if self.player.nuclear_count in range(1, 6):
            path = 'numeral'+str(int(self.player.nuclear_count))+'.png'
            self.display_surface.blit(self.numbers[path], NUCLEAR_COUNT_POS)
