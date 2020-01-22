import pygame
import images
from pygame.locals import *


class BaseGameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, all_objects, size, image, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawntime = pygame.time.get_ticks()
        self.all_objects = all_objects
        self.all_objects.add(self)
        if image is not None:
            self.image = image
        else:
            self.image = pygame.Surface(size)
            self.image.fill(color)
