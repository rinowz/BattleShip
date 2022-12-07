import pygame
from player import Player
from settings import *
from support import *


class Level:
    """ Уровень - происходит процесс "игры" игры"""

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.background_surf = pygame.image.load("../graphics/background.jpg")

        # создание игрока
        self.player = Player(
            PLAYER_POSITION, [])

        self.visible_sprites = self.CameraGroup(self)
        self.visible_sprites.add(self.player)

    def run(self):
        """ Обновляет и рисует игру"""

        # задний фон
        background_rect = self.background_surf.get_rect()
        # достаем смещение камеры из объекта self.visible_sprites класса CameraGroup,
        # "камеру" котрой мы используем в уровне
        offset = self.visible_sprites.camera_position
        background_rect.centerx -= offset.x
        background_rect.centery -= offset.y
        self.display_surface.blit(self.background_surf, background_rect)

        # видимые объекты группы CameraGroup
        self.visible_sprites.offset_draw()
        self.visible_sprites.update()

    class CameraGroup(pygame.sprite.Group):
        """ Отражает существование камеры. Такая же фигня, как и pygame.sprite.Group,
        только имеет отклонение от положения камеры."""

        def __init__(self, outer):
            """
            :param outer: Объект класса Level, внутри которого создается данный объект
            """
            super().__init__()
            self.display_surface = pygame.display.get_surface()

            # игрок забирается из вызывающего объекта
            self.outer = outer
            self.player = self.outer.player

            # камере задается положение
            self.camera_position = pygame.math.Vector2()

            # положение, которое отвечает точке, лежащей симметрично camera_position относительно положения игрока
            # (но на самом деле не так, а точки, которые окажутся в центре экрана при расположении камер
            # в левом верхнем углу, будут симметричны)
            # используется для вычисления положения камеры,
            # где антикамера отстает от игрока при его движении и следует за ним
            self.camera_antiposition = pygame.math.Vector2()

        def offset_draw(self):
            """ Вычисляет отклонение камеры и рисует элементы группы"""

            # Вычисление положения camera_antiposition по некоторой логике
            self.antiposition_calculation()

            # Положение камеры вычисляется относиткльно положения антикамеры и является необходимым отклонением
            self.camera_position = 2 * (pygame.math.Vector2(self.player.rect.center) - PLAYER_POSITION) \
                                   - self.camera_antiposition

            # рисуем элементы группы с найденным отклонением
            sprites = self.sprites()
            for sprite in sprites:
                pos = sprite.rect.topleft - self.camera_position

                self.display_surface.blit(sprite.image, pos)

        def antiposition_calculation(self):
            """ Вычисление положения антикамеры"""

            # Расстояние от игрока. Определяется от центра экрана,
            # если предположить что антикамера находится в верхнем левом углу.
            distance = self.player.rect.center - PLAYER_POSITION - self.camera_antiposition

            # Скорость антикамеры определяется вдоль вектора расстояния, пропорционально максимальной скорости игрока.
            # Таким образом, при достижении некоторой точки, антикамера движется с такой же скоростью, как и игрок.
            camera_velocity = pygame.math.Vector2()
            if distance.magnitude() != 0:
                camera_velocity.x = distance.x * (self.player.max_speed / (WIDTH // 2))
                camera_velocity.y = distance.y * (self.player.max_speed / (HEIGHT // 2))


            # Добавляем постоянную компоненту к скорости камеры
            camera_velocity += pygame.math.Vector2(sign(camera_velocity.x), sign(camera_velocity.y))

            # Антикамера(центр экрана) должна всегда следовать за игроком. Если она обгоняет игрока, останавливаем ее
            if camera_velocity.magnitude() > distance.magnitude():
                self.camera_antiposition = pygame.math.Vector2(self.player.rect.center) - PLAYER_POSITION
            else:
                self.camera_antiposition += camera_velocity

            # округляем координаты, чтобы установить пололжение, которое было бы в пикселях
            self.camera_antiposition.x = round(self.camera_antiposition.x)
            self.camera_antiposition.y = round(self.camera_antiposition.y)
