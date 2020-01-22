import pygame
import images
import base_game_object
from pygame.locals import *



class Block(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, platforms):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30), images.block, (100, 100, 100))
        self.platforms = platforms
        self.platforms.add(self)



class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, all_objects, ground_blocks):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30), images.ground, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ground_blocks = ground_blocks
        self.ground_blocks.add(self)