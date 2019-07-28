import pygame
import base_game_object
from pygame.locals import *



class Block(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, platforms):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30))
        self.platforms = platforms
        self.platforms.add(self)
        self.image.fill((100, 100, 100))



class Empty(pygame.sprite.Sprite):
    def __init__(self, x, y, empty_blocks):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.empty_blocks = empty_blocks
        self.empty_blocks.add(self)