import pygame
from settings import *


class Button:
    def __init__(self, pos, image=None, hover_image=None, size=None, text='', font=None,
                 text_color=BLACK, text_hover_color=BLACK, on_click=lambda: 1+1):
        """
        :param pos: Позиция центра кнопки
        :param image: Sufrace изображения кнопки
        :param hover_image: изображение при наведение курсора
        :param size: Размер кнопки
        :param text: Текст, который пишется на кнопке
        :param font: шрифт текста
        :param text_color: цвет текста
        :param text_hover_color: цвет текста при наведении курсором на кнопку
        :param on_click: функция, вызываемая при нажатии на кнопку
        """

        # дефолтные значения
        if image is None:
            image = pygame.Surface((300, 50))
        if hover_image is None:
            hover_image = pygame.Surface((300, 50))
            hover_image.fill(WHITE)

        if size is not None:
            image = pygame.transform.scale(image, size)
            hover_image = pygame.transform.scale(hover_image, size)
        if font is None:
            font = pygame.font.SysFont('New Times Roman', 20)

        # кнопка
        self.image = image
        self.hover_image = hover_image
        self.rect = self.image.get_rect(center=pos)
        self.hover_rect = self.hover_image.get_rect(center=self.rect.center)

        # текст
        self.text = text
        self.font = font
        self.text_surf = self.font.render(self.text, True, text_color)
        self.text_hover_surf = self.font.render(self.text, True, text_hover_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        self.display_surface = pygame.display.get_surface()

        self.hover = False

        self.on_click = on_click

    def update(self, mouse_click):
        self.set_hover()

        if self.hover:
            self.display_surface.blit(self.hover_image, self.hover_rect)
            self.display_surface.blit(self.text_hover_surf, self.text_rect)
        else:
            self.display_surface.blit(self.image, self.rect)
            self.display_surface.blit(self.text_surf, self.text_rect)

        if mouse_click and self.hover:
            self.on_click()

    def set_hover(self):
        self.hover = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.hover = True
