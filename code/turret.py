""" Класс Turret"""
from support import *
from ship_like import ShipLike
from player_shooting import PlayerShooting
from object_info import ShipInfo
from object import Object


class Turret(Object):
    """ Турель - фигня стоящая на месте и стреляющая по игроку. Состоит из платформы, которая "является" этим объектом
    и создаваемого объекта движущейся стреляющей части"""

    def __init__(self, turret_info, projectile_info, player):
        """
        :param turret_info: информация о создаваемой турели
        :param projectile_info: информация о выпускаемых снарядах
        """

        super().__init__(turret_info)
        self.gun = self.Gun(turret_info, projectile_info, player, self)

        self.layer_change(self.gun, 15)
        self.layer_change(self, 10)

    def hit(self, hitter):
        self.gun.hit(hitter)

    class Gun(PlayerShooting):
        """ Пушка - часть турели которая вращается и производит выстрел. Ее self.pos определяет центр вращения"""
        def __init__(self, gun_info, projectile_info, player, platform):
            """
            :param gun_info: информация о создаваемой турели
            :param projectile_info: информация о выпускаемых снарядах
            :param player: игрок, в которого нужно стрелять
            :param platform: объект Turret, в котором создается данный объект
            """
            # вектор из центра изображения в центр вращения
            self.initial_pivot_vector = pygame.Vector2(gun_info.gun_offset)
            self.current_pivot_vector = self.initial_pivot_vector.copy()

            gun_info.image = gun_info.gun_image
            super().__init__(gun_info, projectile_info, player)

            self.angle = gun_info.gun_angle
            self.rotate_image()

            self.platform = platform
            self.no_hit_objects = [self, self.platform]

        def update(self, dt):
            super().update(dt, add_vel=False)

        def set_velocity(self, dt):
            """ Меняет угол на который повернута турель"""
            angle_dif_sign = sign(self.to_player_angle() - self.angle)

            self.angle += angle_dif_sign * self.acceleration * dt

            if sign(self.angle - self.to_player_angle()) != angle_dif_sign:
                self.angle = self.to_player_angle()

        def rotate_image(self):
            """ """
            self.image = pygame.transform.rotate(self.initial_image, math.degrees(self.angle))
            self.current_pivot_vector = self.initial_pivot_vector.rotate(math.degrees(self.angle))

            self.rect = self.image.get_rect()
            self.set_pos(self.pos)

        def set_pos(self, pos):
            """ Переопределяем, чтобы self.pos находилось в центре вращения и self.rect был нормальным"""
            self.pos = pos
            self.rect.center = round_list(add_lists(self.pos, minus(self.current_pivot_vector)))

        def destroy(self):
            """ Уничтожает себя вместе с платформой"""
            self.platform.kill()
            self.kill()
