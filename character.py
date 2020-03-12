import pygame
import images
import base_game_object
import bomb
from pygame.locals import *


class Character(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, image=None):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30), image, (0, 0, 0))
        self.start_pos = (x, y)
        self.speed = 3
        self.hp = 100
        self.score = 0
        self.original_image = self.image
        self.current_empty = None
        self.right = 0
        self.left = 0
        self.up = 0
        self.down = 0

    def get_current_empty(self, ground_blocks):
        for eb in ground_blocks:
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
                    

    def move(self, group, ground_blocks):
        prev_coords = self.rect.x, self.rect.y
        self.rect.y += self.speed * (self.down - self.up)
        self.collide(0, (self.down - self.up), group)
        self.rect.x += self.speed * (self.right - self.left)
        self.collide((self.right - self.left), 0, group)
        self.get_current_empty(ground_blocks)
        return prev_coords
    

    def check_hp(self):
        if self.hp <= 0:
            # self.die()
            return True
        return False


    def die(self):
        self.kill()


    def place_bomb(self, bombs, bomb):
        b = bomb(self.current_empty.rect.x, self.current_empty.rect.y, self.all_objects, bombs)
        return (b.rect.x, b.rect.y, b)

