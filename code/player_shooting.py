""" Класс PlayerShooting"""
from support import *
from ship_like import ShipLike


class PlayerShooting(ShipLike):
    """ ShipLike, который стреляет по игроку"""

    def __init__(self, ship_info, projectile_info, player):
        """
        :param ship_info: Информация о создаваемом корабле
        :param projectile_info: информация о выпускаемом снаряде
        :param player: игрок, в которого нужно стрелять
        """
        super(PlayerShooting, self).__init__(ship_info, projectile_info)

        self.player = player
        self.attack_radius = ship_info.attack_radius
        self.shoot_tolerance = math.pi / 18

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
