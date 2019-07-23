import pygame
from pygame.locals import *


class Character(pygame.sprite.Sprite):
    def __init__(self, center, all_objects):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.all_objects = all_objects
        self.all_objects.add(self)
        self.speed = 3
        self.directionx = 0
        self.directiony = 0
    

    def move(self):
        self.rect.x += self.speed * self.directionx
        self.rect.y += self.speed * self.directiony
    

    def change_direction_x(self, change_x):
        self.directionx = change_x

    
    def change_direction_y(self, change_y):
        self.directiony = change_y
