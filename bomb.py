import pygame
import base_game_object
from pygame.locals import *



class Bomb(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, bombs):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30))
        self.image.fill((230, 20, 20))
        self.bombs = bombs
        self.bombs.add(self)
        pygame.time.set_timer(self.boom, 3000, once = True)
    

    def boom(self):
        self.bombs.remove(self)