import pygame
from pygame.locals import *


class BaseGameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, all_objects, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.all_objects = all_objects
        self.all_objects.add(self)