import pygame
import base_game_object
from pygame.locals import *


class Character(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30))
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
