from ship import Ship
from settings import *


class Player(Ship):
    """ Корабль, которым управляет игрок"""

    def __init__(self, pos, groups, image):
        super().__init__(pos, groups, image)

    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0
