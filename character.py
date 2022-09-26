import pygame
import base_game_object
import bomb
from pygame.locals import *


class BaseCharacter(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, id):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30))
        self.speed = 3
        self.directionx = 0
        self.directiony = 0
        self.hp = 100
        self.current_empty = None
    
    def get_current_empty(self, empty_blocks):
        for eb in empty_blocks:
            if pygame.sprite.collide_rect(self, eb):
                if eb.rect.x < self.rect.centerx < eb.rect.right and eb.rect.top < self.rect.centery < eb.rect.bottom:
                    self.current_empty = eb


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


    def move(self, group, empty_blocks):
        self.rect.y += self.speed * self.directiony
        self.collide(0, self.directiony, group)
        self.rect.x += self.speed * self.directionx
        self.collide(self.directionx, 0, group)
        self.get_current_empty(empty_blocks)
    

    def check_hp(self):
        if self.hp <= 0:
            self.die()
            return True
        return False


    def die(self):
        self.kill()


    def change_direction_x(self, change_x):
        self.directionx = change_x

    
    def change_direction_y(self, change_y):
        self.directiony = change_y


    def place_bomb(self, bombs):
        bomb.Bomb(self.current_empty.rect.x, self.current_empty.rect.y, self.all_objects, bombs)



class Character(BaseCharacter):
    def __init__(self, x, y, all_objects, id):
        BaseCharacter.__init__(self, x, y, all_objects, id)
        self.id = id
        if self.id % 2 == 1:
            color = (19, 127, 240)
        else:
            color = (240, 19, 69)
        self.image.fill(color)

    



class Enemy(BaseCharacter):
    def __init__(self, x, y, all_objects, id):
        BaseCharacter.__init__(self, x, y, all_objects, id)
        self.id = id
        if self.id % 2 == 1:
            color = (240, 19, 69)
        else:
            color = (19, 127, 240)
        self.image.fill(color)
        