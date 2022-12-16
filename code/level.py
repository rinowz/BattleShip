""" Уровень - создается при начатии "игры" игры и осуществляет всю работу до завершения"""
import random

import pygame
from player import Player
from settings import *
from support import *
from object_info import *
from exploding_object import ExplodingObject
from enemy_ship import EnemyShip
from ui import UI
from turret import Turret


class Level:
    """ Уровень - происходит процесс "игры" игры"""

    def __init__(self):
        # начальные присваивания
        self.initialization_start()

        # создаем игрока
        self.player_setup()

        # генерируем карту
        generator = self.MapGenerator(self.visible_sprites, BORDERS, self.images, self.layer_change, self.player)
        object_list = generator.generate(10, 10, 10)

        # UI
        self.ui = UI(self.player)

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

        self.ui.display()

    def load_images(self):
        self.images['enemy'] = load_image("ships/ship2.0.png", -90)
        self.images['meteors'] = open_image_folder("../graphics/meteors")
        self.images['turret'] = {
            'platform': pygame.transform.scale(load_image("turret/gun_platform.png"), (TURRET_SIZE, TURRET_SIZE)),
            "gun": pygame.transform.scale(load_image("turret/gun.png", -90), (TURRET_SIZE, TURRET_SIZE))}

    def initialization_start(self):
        """ Производит начальную установку уровня"""
        self.images = {}
        self.load_images()

        self.display_surface = pygame.display.get_surface()
        self.background_surf = pygame.image.load("../graphics/background.jpg")
        self.background_rect = self.background_surf.get_rect(center=BACKGROUND_POSITION)

        # группы
        self.visible_sprites = self.CameraGroup()
        self.collidable_sprites = pygame.sprite.Group()

        # функция изменения слоя
        self.layer_change = build_layer_change_function(self.visible_sprites)

    def player_setup(self):
        """ Создает игрока"""
        # Информация об игроке
        player_info = PlayerInfo(PLAYER_POSITION, [self.visible_sprites], layer_change=self.layer_change)
        projectile_radius = 10
        projectile_sprite = pygame.Surface((2*projectile_radius, 2*projectile_radius))
        projectile_sprite.set_colorkey(BLACK)
        pygame.draw.circle(projectile_sprite, WHITE, (projectile_radius, projectile_radius), projectile_radius)
        projectile_info = ProjectileInfo([self.visible_sprites], self.visible_sprites, projectile_sprite,
                                         layer_change=self.layer_change, damage=10)

        # создание игрока
        self.player = Player(self.collidable_sprites, player_info, projectile_info)
        self.visible_sprites.player = self.player

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

    class MapGenerator:
        """ Генерирует объекты на карте"""

        def __init__(self, visible_group, borders, images, layer_change, player):
            self.visible_group = visible_group
            self.borders = borders
            self.images = images
            self.layer_change = layer_change
            self.player = player

            random.seed()

            self.stage = 'initialization'

        def generate(self, enemy_count, turret_count, meteor_count):
            """
            Генерирует объекты на карте
            :param enemy_count: необходимое количество вражеских кораблей
            :param turret_count: необходимое количество турелей
            :param meteor_count: необходимое количество метеоритов
            :return: Список из списков со всеми типами созданных объектов
            """

            self.stage = 'enemy'
            enemies = generate_multiple(enemy_count, self.generate_enemy)

            self.stage = 'turret'
            turrets = generate_multiple(turret_count, self.generate_turret)

            self.stage = 'meteor'
            meteors = generate_multiple(meteor_count, self.generate_meteor)

            return [enemies, turrets, meteors]

        def generate_enemy(self):
            """ Создает объект EnemyShip и возвращает"""
            image = self.images['enemy']
            pos = self.get_pos(image.get_rect())
            groups = self.visible_group
            vel = (0, 0)
            layer_change = self.layer_change
            attack_cooldown = random.randint(1000, 5000)
            max_speed = random.randint(100, 500)
            acceleration = max_speed / random.uniform(5, 10)
            hp = random.randint(10, 30)
            attack_radius = 500
            detection_radius = 1000
            stop_radius = 300

            enemy_info = EnemyInfo(pos, groups, image, vel, layer_change, attack_cooldown, max_speed,
                      acceleration, hp, attack_radius, detection_radius, stop_radius)

            return EnemyShip(enemy_info, self.generate_projectile(), self.player)

        def generate_turret(self):
            """ Генерирует объект Turret и возвращает"""
            image = self.images['turret']['platform']
            gun_image = self.images['turret']['gun']
            pos = self.get_pos(image.get_rect().inflate(100, 100))
            groups = [self.visible_group]
            gun_offset = TURRET_OFFSET
            gun_angle = 0
            layer_change = self.layer_change
            attack_cooldown = random.randint(1000, 5000)
            acceleration = random.uniform(1.5, 4.5)
            hp = random.randint(10, 50)
            attack_radius = 500

            turret_info = TurretInfo(pos, groups, image, gun_image, gun_offset, gun_angle, layer_change,
                                     attack_cooldown, acceleration, hp, attack_radius)

            return Turret(turret_info, self.generate_projectile(), self.player)

        def generate_projectile(self):
            """
            Генерирует информацию о снаряде
            :return: Объект ProjectileInfo
            """
            groups = [self.visible_group]
            collision_group = self.visible_group

            radius = 10
            image = pygame.Surface((2 * radius, 2 * radius))
            image.set_colorkey(BLACK)
            pygame.draw.circle(image, WHITE, (radius, radius), radius)

            layer_change = self.layer_change
            damage = random.uniform(1, 10)
            speed = random.randint(500, 1500)

            return ProjectileInfo(groups, collision_group, image, layer_change, damage, speed)

        def generate_meteor(self):
            """ Генерирует метеорит и возвращает объект ExplodingObject"""

            image = random.choice(self.images['meteors'])
            pos = self.get_pos(image.get_rect())
            groups = [self.visible_group]
            layer_change = self.layer_change
            vel = (random.randint(-500, 500), random.randint(-500, 500))

            meteor_info = ObjectInfo(pos, groups, image, vel, layer_change)

            return ExplodingObject(meteor_info, self.visible_group)

        def get_pos(self, rect):
            """
            Находит место на карте, чтобы поместить rect
            :param: rect: Прямоугольник, который должен поместиться на карте. Передавать то, позицию чего не жалко
            :return: список из координат x, y - расположение центра
            """

            for i in range(100):
                x_pos = random.randint(self.borders[0][0], self.borders[0][1])
                y_pos = random.randint(self.borders[1][0], self.borders[1][1])

                pos = (x_pos, y_pos)
                rect.center = pos

                if self.check_collision(rect):
                    return pos

            print('Couldn\'t place ' + self.stage + 'in', self.borders)
            return None

        def check_collision(self, rect):
            """
            Проверяет сталкивается ли прямоугольник с чем-то из видимой группы, чтобы можно было его создать
            :param rect: прямоугольник, который проверяется
            :return: True если нет столкновений
            """

            check_sprite = pygame.sprite.Sprite()
            check_sprite.rect = rect

            if pygame.sprite.spritecollideany(check_sprite, self.visible_group):
                return False

            return True
