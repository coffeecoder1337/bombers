import pygame
from pygame.locals import *


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, all_objects):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.all_objects = all_objects
        self.all_objects.add(self)
