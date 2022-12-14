import pygame
from ship_like import ShipLike
from support import *


class EnemyShip(ShipLike):
    """ Вражеский корабль"""

    def __init__(self, object_info, projectile_info, player):
        """
        :param object_info: информация о создаваемом корабле
        :param projectile_info: информация о выпускаемых при выстреле снарядах
        :param hp: количество здоровья корабля
        """

        super(EnemyShip, self).__init__(object_info, projectile_info)

        self.player = player
        self.shoot_tolerance = math.pi / 18
        self.detection_radius = 1000
        self.attack_radius = 400
        self.real_max_speed = self.max_speed
        self.stop_distance = 200
        self.projectile_speed = BULLET_SPEED/2

    def update(self, dt):
        """
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты."""
        # расстояние до игрока
        distance_magn = self.to_player_distance().magnitude()
        if distance_magn < self.detection_radius:
            # Когда игрок слишком близко, останавливается
            to_move = True
            if distance_magn < self.stop_distance:
                self.velocity = self.to_player_distance()
                to_move = False

            super().update(dt, add_vel=to_move, change_vel=to_move)

        if pygame.sprite.collide_rect(self, self.player):
            if self.mask.overlap(self.player.mask, get_mask_offset(self, self.player)):
                self.player.hit(self)
                self.destroy()

    def set_velocity(self, dt):
        """ Определяет какая скорость должна быть у корабля в данный момент
        :param dt: время между кадрами,
        которое используется, чтобы установить с какой скоростью должны двигаться спрайты."""
        angle = self.to_player_angle()

        change_direction = pygame.math.Vector2(math.cos(angle), -math.sin(angle))
        distance_factor = self.to_player_distance().magnitude() - self.stop_distance
        self.velocity_change = change_direction * distance_factor * self.acceleration

        super(EnemyShip, self).set_velocity(dt)

    def to_shoot(self):
        """
        Определяет нужно ли выстрелить
        :return: True или False
        """
        if self.to_player_distance().magnitude() < self.attack_radius:
            return abs(self.to_player_angle() - self.angle) < self.shoot_tolerance

        return False

    def to_player_angle(self):
        """
        Возвращает угол расстояния до игрока
        :return Угол в радианах
        """
        return get_angle(self.to_player_distance())

    def to_player_distance(self):
        """
        Возвращает расстояние до игрока
        :return расстояние, Vector2
        """
        return pygame.math.Vector2(add_lists(self.player.pos, minus(self.pos)))
