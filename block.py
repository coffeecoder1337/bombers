import pygame
import images
import base_game_object
from pygame.locals import *



class Block(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, platforms):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30), images.block, (100, 100, 100))
        self.platforms = platforms
        self.platforms.add(self)



class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, all_objects, ground_blocks):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30), images.ground, (255, 255, 255))
        self.ground_blocks = ground_blocks
        self.ground_blocks.add(self)



class DestructibleBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, all_objects, platforms, ground_blocks, destructible_blocks):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30), images.destructible_block, (255, 200, 255))
        self.all_objects = all_objects
        self.platforms = platforms
        self.ground_blocks = ground_blocks
        self.destructible_blocks = destructible_blocks
        self.destructible_blocks.add(self)
        self.platforms.add(self)
    

    def destroy(self):
        self.image = images.destructible_block_2
        self.rect = self.image.get_rect(center=self.rect.center)
        self.platforms.remove(self)
        self.ground_blocks.add(self)


