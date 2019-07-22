import pygame
from pygame.locals import *


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)