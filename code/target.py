""" Класс Target"""
from object import Object


class Target(Object):
    """ Цель, уничтожение которой является целью игры"""
    def __init__(self, object_info, level_end):
        """
        :param object_info: Информация об объекте
        :param level_end: функция, завершающая игру
        """
        super().__init__(object_info)

        self.level_end = level_end
        self.layer_change(self, 20)

    def destroy(self, game_result):
        self.level_end(game_result)
        self.kill()

    def update(self, dt):
        super(Target, self).update(dt)

    def hit(self, hitter):
        if hitter.damage > 100:
            self.destroy('victory')
