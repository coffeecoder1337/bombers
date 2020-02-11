import pygame
import pyganim
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
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30), images.destructible_block[0], (255, 200, 255))
        self.all_objects = all_objects
        self.platforms = platforms
        self.ground_blocks = ground_blocks
        self.destructible_blocks = destructible_blocks
        self.destructible_blocks.add(self)
        self.platforms.add(self)
    

    def destroy(self):
        expl = Explosion(self.rect.center)
        self.all_objects.add(expl)
        self.image = images.destructible_block[-1]
        self.rect = self.image.get_rect(center=self.rect.center)
        self.platforms.remove(self)
        self.ground_blocks.add(self)
        self.destructible_blocks.remove(self)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.destructible_block[0]
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
            if self.frame == len(images.destructible_block):
                self.kill()
            else:
                center = self.rect.center
                self.image = images.destructible_block[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


