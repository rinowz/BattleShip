"""
Класс, хранящий начальные данные для разных типов объектов
"""
import pygame
from settings import *
from support import *


class ObjectInfo:
    """ Информация о создаваемом объекте"""

    def __init__(self, pos, groups, image=pygame.Surface((50, 50)), vel=(0, 0), layer_change=useless, damage=1):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        :param layer_change: - функция изменения слоя объекта
        :param damage: Урон, который объект может(?) нанести
        """
        self.pos = pos
        self.groups = groups
        self.image = image
        self.vel = vel
        self.layer_change = layer_change
        self.damage = damage


class ProjectileInfo:
    """ Информация о снаряде, выпускаемом при выстреле в ShipLike"""

    def __init__(self, groups, collision_group, image=pygame.Surface((10, 10)), layer_change=useless,
                 damage=PLAYER_DAMAGE, speed=BULLET_SPEED):
        """
        :param groups: Группы, в которые должен входить снаряд
        :param collision_group: Группа, сталкиваясь с которой, снаряд взрывается
        :param image: surface изображения снаряда
        :param layer_change: функция изменения слоя объекта
        :param damage: урон, наносимый снарядом
        :param speed: скорость снаряда
        """
        self.groups = groups
        self.collision_group = collision_group
        self.image = image
        self.layer_change = layer_change
        self.damage = damage
        self.speed = speed

    def get_object_info(self, pos, vel, angle):
        """
        Создает экземпляр класса object_info основываясь на своих и переданных данных
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        :param angle: угол под которым запускается снаряд
        """

        image = pygame.transform.rotate(self.image, math.degrees(angle))

        return ObjectInfo(pos, self.groups, image, vel, self.layer_change, self.damage)


class ShipInfo(ObjectInfo):
    """ Информация об объекте ShipLike"""
    def __init__(self, pos, groups, image=pygame.Surface((50, 50)), vel=(0, 0), layer_change=useless,
                 attack_cooldown=PLAYER_COOLDOWN, max_speed=PLAYER_MAX_SPEED, acceleration=PLAYER_ACCELERATION, hp=100,
                 damage=5, hit_sound=None, shot_sound=None):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        :param layer_change: - функция изменения слоя объекта
        :param attack_cooldown: время, которое занимает кулдаун при атаке
        :param max_speed: максимальная скорость
        :param acceleration: насколько меняется скорость, когда корабль пытается ее изменить
        :param hp: количество здоровья
        :param damage: урон, наносимый при столкновении
        :param hit_sound: звук, играемый при получении урона
        :param shot_sound: звук, играемый при выстреле
        """
        super().__init__(pos, groups, image, vel, layer_change, damage)

        self.attack_cooldown = attack_cooldown
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.hp = hp

        if hit_sound is None:
            hit_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), '..', 'sound', 'hit.mp3'))

        if shot_sound is None:
            shot_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), '..', 'sound', 'shot.mp3'))

        self.hit_sound = hit_sound
        self.shot_sound = shot_sound


class PlayerInfo(ShipInfo):
    """ Информация о создаваемом игроке"""

    def __init__(self, pos, groups, vel=(0, 0), layer_change=useless):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        :param layer_change: - функция изменения слоя объекта
        """
        loaded_image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        image = pygame.transform.rotate(loaded_image, -90)

        hit_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), '..', 'sound/hit.mp3'))

        shot_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), '..', 'sound', 'shot.mp3'))

        super(PlayerInfo, self).__init__(pos, groups, image, vel, layer_change,
                                         hit_sound=hit_sound, shot_sound=shot_sound)


class EnemyInfo(ShipInfo):
    """ Информация о вражеском корабле"""
    def __init__(self, pos, groups, image=pygame.Surface((50, 50)), vel=(0, 0), layer_change=useless,
                 attack_cooldown=PLAYER_COOLDOWN, max_speed=PLAYER_MAX_SPEED, acceleration=PLAYER_ACCELERATION, hp=100,
                 attack_radius=400, detection_radius=1000, stop_radius=200, damage=5, hit_sound=None, shot_sound=None):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param image: surface изображения объекта
        :param vel: начальная скорость - итерируемый из 2 элементов, который превращается в Vector2
        :param layer_change: - функция изменения слоя объекта
        :param attack_cooldown: время, которое занимает кулдаун при атаке
        :param max_speed: максимальная скорость
        :param acceleration: насколько меняется скорость, когда корабль пытается ее изменить
        :param hp: количество здоровья
        :param attack_radius: расстояние начиная с которого противник начинает стрелять по игроку
        :param detection_radius: расстояние начиная с которого противник начинает приближаться к игроку
        :param stop_radius: расстояние, на котором противник останавливается
        :param damage: урон, наносимый при столкновении
        :param hit_sound: звук, играемый при получении урона
        :param shot_sound: звук, играемый при выстреле
        """
        super().__init__(pos, groups, image, vel, layer_change, attack_cooldown, max_speed, acceleration, hp, damage,
                         hit_sound, shot_sound)

        self.attack_radius = attack_radius
        self.detection_radius = detection_radius
        self.stop_radius = stop_radius


class TurretInfo(ShipInfo):
    """ Информация о создаваемой турели"""

    def __init__(self, pos, groups, image=pygame.Surface((50, 50)), gun_image=pygame.Surface((30, 40)),
                 gun_offset=(0, 0), gun_angle=0, layer_change=useless, attack_cooldown=PLAYER_COOLDOWN,
                 acceleration=math.pi, hp=100, attack_radius=500):
        """
        :param pos: Позиция объекта - итерируемый со значениями для x и y
        :param groups: группы, в которые нужно включить спрайт
        :param image: surface изображения основания турели
        :param gun_image: изображение вращающейся части
        :param gun_offset: отклонение оси вращения от центра
        :param gun_angle: начальный угол поворота
        :param layer_change: - функция изменения слоя объекта
        :param attack_cooldown: время, которое занимает кулдаун при атаке
        :param acceleration: насколько меняется угол, когда турель пытается ее изменить
        :param hp: количество здоровья
        :param attack_radius: максимальное расстояние, с которого турель будет атаковать игрока
        """
        super().__init__(pos, groups, image, (0, 0), layer_change,
                         attack_cooldown, 0, acceleration, hp)

        self.gun_image = gun_image
        self.gun_offset = gun_offset
        self.gun_angle = gun_angle
        self.attack_radius = attack_radius
