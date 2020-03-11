import images
import pygame
from pygame.locals import *


class Loader(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(images.loader[0], (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(images.loader):
                self.frame = -1
            else:
                center = self.rect.center
                self.image = pygame.transform.scale(images.loader[self.frame], (100, 100))
                self.rect = self.image.get_rect()
                self.rect.center = center
