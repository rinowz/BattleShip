""" Уровень - создается при начатии "игры" игры и осуществляет всю работу до завершения"""
import pygame
from player import Player
from settings import *
from support import *
from object_info import ObjectInfo, PlayerInfo
from projectile_info import ProjectileInfo
from exploding_object import ExplodingObject


class Level:
    """ Уровень - происходит процесс "игры" игры"""

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.background_surf = pygame.image.load("../graphics/background.jpg")
        self.background_rect = self.background_surf.get_rect(center=BACKGROUND_POSITION)

        # группы
        self.visible_sprites = self.CameraGroup()
        self.collidable_sprites = pygame.sprite.Group()

        # функция изменения слоя
        self.layer_change = build_layer_change_function(self.visible_sprites)

        # Информация об игроке
        player_info = PlayerInfo(PLAYER_POSITION, [self.visible_sprites], layer_change=self.layer_change)
        projectile_radius = 10
        projectile_sprite = pygame.Surface((2*projectile_radius, 2*projectile_radius))
        projectile_sprite.set_colorkey(BLACK)
        pygame.draw.circle(projectile_sprite, WHITE, (projectile_radius, projectile_radius), projectile_radius)
        projectile_info = ProjectileInfo([self.visible_sprites], self.visible_sprites, projectile_sprite,
                                         layer_change=self.layer_change)

        # создание игрока
        self.player = Player(self.collidable_sprites, player_info, projectile_info)
        self.visible_sprites.player = self.player

        self.rocks = []
        # создаем камень
        rock_radius = 50
        rock_image = pygame.Surface((2*rock_radius, 2*rock_radius))
        rock_image.set_colorkey(BLACK)
        pygame.draw.circle(rock_image, GREEN, (rock_radius, rock_radius), rock_radius)

        rock_info = ObjectInfo([0, 0], [self.visible_sprites], rock_image, (30, 30))
        self.rocks.append(ExplodingObject(rock_info, self.visible_sprites))

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

        def __init__(self):
            """ !установить self.player до того как рисовать"""
            self.player = None

            super().__init__(default_layer=0)
            self.display_surface = pygame.display.get_surface()

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
