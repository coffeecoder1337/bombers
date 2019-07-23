import pygame
import base_game_object
from pygame.locals import *



class Block(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, platforms):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30))
        self.platforms = platforms
        self.platforms.add(self)
        self.image.fill((100, 100, 100))