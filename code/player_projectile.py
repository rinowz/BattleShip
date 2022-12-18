""" Класс PlayerProjectile"""
from exploding_object import ExplodingObject
from support import *
from enemy_ship import EnemyShip
from turret import *


class PlayerProjectile(ExplodingObject):
    def explosion(self):
        colliding_objects = self.colliding_objects.copy()
        for colliding_object in colliding_objects:
            if self.mask.overlap(colliding_object.mask, get_mask_offset(self, colliding_object)):
                if isinstance(colliding_object, EnemyShip) or isinstance(colliding_object, Turret) or \
                        isinstance(colliding_object, Gun):
                    colliding_object.hit_sound.play()

                colliding_object.hit(self)

        self.kill()
