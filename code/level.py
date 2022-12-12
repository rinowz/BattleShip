""" Уровень - создается при начатии "игры" игры и осуществляет всю работу до завершения"""
import pygame
from player import Player
from settings import *
from support import *
from rock import Rock


class Level:
    """ Уровень - происходит процесс "игры" игры"""

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.background_surf = pygame.image.load("../graphics/background.jpg")
        self.background_rect = self.background_surf.get_rect(center=BACKGROUND_POSITION)

        self.collidable_sprites = pygame.sprite.Group()

        # создание игрока
        self.player = Player(
            PLAYER_POSITION, [], self.collidable_sprites)

        self.visible_sprites = self.CameraGroup(self)
        self.visible_sprites.add(self.player)

        # создаем камень
        rock = Rock([0, 0], [self.visible_sprites, self.collidable_sprites], (30, 30))
        self.visible_sprites.change_layer(rock, -1)

    def run(self, dt):
        """ Обновляет и рисует игру"""

        # достаем смещение камеры из объекта self.visible_sprites класса CameraGroup,
        # "камеру" котрой мы используем в уровне
        offset = minus(self.visible_sprites.camera_position)
        self.background_rect.center = round_list(add_lists(offset, BACKGROUND_POSITION))
        self.display_surface.blit(self.background_surf, self.background_rect)

        # видимые объекты группы CameraGroup
        self.visible_sprites.update(dt)
        self.visible_sprites.offset_draw(dt)

    class CameraGroup(pygame.sprite.LayeredUpdates):
        """ Отражает существование камеры. Такая же фигня, как и pygame.sprite.LayeredUpdates,
        только имеет отклонение от положения камеры."""

        def __init__(self, outer):
            """
            :param outer: Объект класса Level, внутри которого создается данный объект
            """
            super().__init__(default_layer=0)
            self.display_surface = pygame.display.get_surface()

            # игрок забирается из вызывающего объекта
            self.outer = outer
            self.player = self.outer.player

            # камере задается положение
            self.camera_position = [0, 0]

            # положение, которое отвечает точке, лежащей симметрично camera_position относительно положения игрока
            # (но на самом деле не так, а точки, которые окажутся в центре экрана при расположении камер
            # в левом верхнем углу, будут симметричны)
            # используется для вычисления положения камеры,
            # где антикамера отстает от игрока при его движении и следует за ним
            self.camera_antiposition = [0, 0]

        def offset_draw(self, dt):
            """ Вычисляет отклонение камеры и рисует элементы группы"""

            # Вычисление положения camera_antiposition по некоторой логике
            self.antiposition_calculation(dt)

            # Положение камеры вычисляется относиткльно положения антикамеры и является необходимым отклонением
            player_offset = add_lists(self.player.pos, minus(PLAYER_POSITION))
            self.camera_position = add_lists(multiply_list(player_offset, 2), minus(self.camera_antiposition))

            # Нужно исправить ошибку с округлением. Расстояние между округлениями не равно округленному расстоянию
            rerounded_camera_position = add_lists(self.player.rect.center,
                                                  round_list(add_lists(self.camera_position, minus(self.player.pos))))
            offset = minus(rerounded_camera_position)

            # рисуем элементы группы с найденным отклонением
            sprites = self.sprites()
            for sprite in sprites:
                pos = round_list(add_lists(sprite.rect.center, offset))

                rect = sprite.image.get_rect(center=pos)
                self.display_surface.blit(sprite.image, rect)

        def antiposition_calculation(self, dt):
            """ Вычисление положения антикамеры"""

            # Расстояние от игрока. Определяется от центра экрана,
            # если предположить что антикамера находится в верхнем левом углу.
            distance = pygame.math.Vector2(
                add_lists(add_lists(self.player.pos, minus(PLAYER_POSITION)), minus(self.camera_antiposition)))

            # Скорость антикамеры определяется вдоль вектора расстояния, пропорционально максимальной скорости игрока.
            # Таким образом, при достижении некоторой точки, антикамера движется с такой же скоростью, как и игрок.
            camera_velocity = pygame.math.Vector2()

            # Минимальная скорость камеры
            camera_min_speed = self.player.max_speed * 0.1

            # Добавляем минимальную скорость к камере
            if distance.magnitude() != 0:
                camera_velocity.x = sign(distance.x) * \
                                    (abs(distance.x * self.player.max_speed / ((WIDTH // 2) - 50)) + camera_min_speed)
                camera_velocity.y = sign(distance.y) * \
                                    (abs(distance.y * self.player.max_speed / ((HEIGHT // 2) - 50)) + camera_min_speed)

            # Устанавливаем позицию антикамеры
            self.camera_antiposition = add_lists(self.camera_antiposition, camera_velocity * dt)

            # Позиция антикамеры, при которой игрок находится в центре
            center_pos = add_lists(self.player.pos, minus((PLAYER_POSITION)))

            # Антикамера(центр экрана) должна всегда следовать за игроком. Если она обгоняет игрока, останавливаем ее
            if abs(camera_velocity.x * dt) > abs(distance.x) and abs(camera_velocity.x) > abs(self.player.velocity.x):
                self.camera_antiposition[0] = center_pos[0]
            if abs(camera_velocity.y * dt) > abs(distance.y) and abs(camera_velocity.y) > abs(self.player.velocity.y):
                self.camera_antiposition[1] = center_pos[1]
