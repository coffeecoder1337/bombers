import pygame
import base_game_object
import bomb
from pygame.locals import *


class Character(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30))
        self.speed = 3
        self.directionx = 0
        self.directiony = 0


    def collide(self, dirx, diry, group):
        for item in group:
            if pygame.sprite.collide_rect(self, item):
                if dirx > 0:
                    self.rect.right = item.rect.left
                if dirx < 0:
                    self.rect.left = item.rect.right

                if diry > 0:
                    self.rect.bottom = item.rect.top
                if diry < 0:
                    self.rect.top = item.rect.bottom


    def move(self, group):
        self.rect.y += self.speed * self.directiony
        self.collide(0, self.directiony, group)
        self.rect.x += self.speed * self.directionx
        self.collide(self.directionx, 0, group)
    

    def change_direction_x(self, change_x):
        self.directionx = change_x

    
    def change_direction_y(self, change_y):
        self.directiony = change_y


    def place_bomb(self, bombs, spawntime):
        bomb.Bomb(self.rect.x, self.rect.y, self.all_objects, bombs, spawntime)