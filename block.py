import pygame
import base_game_object
from pygame.locals import *



class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30))
        self.image.fill((255, 0, 255))