import pygame
import base_game_object
from pygame.locals import *



class Bomb(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, bombs):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30))
        self.image.fill((230, 20, 20))
        self.bombs = bombs
        self.spawntime = pygame.time.get_ticks()
        self.bombs.add(self)
    

    def boom(self):
        self.bombs.remove(self)
        self.all_objects.remove(self)

    
    def check_to_boom(self):
        if pygame.time.get_ticks() - self.spawntime > 3000:
            self.boom()
