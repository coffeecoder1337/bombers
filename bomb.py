import pygame
import images
import base_game_object
from pygame.locals import *



class Bomb(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, bombs, areas_length=4, image=None, area_image=None, rotate_area=False):
        self.size = 30
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (self.size, self.size), image, color = (200, 50, 50))
        self.bombs = bombs
        self.spawntime = pygame.time.get_ticks()
        self.coords_list = [int(self.rect.x / self.size), int(self.rect.y / self.size)]
        self.areas_length = areas_length
        self.area_image = area_image
        self.rotate_area = rotate_area
        self.areas_placed = False
        self.bombs.add(self)
    

    def boom(self):
        self.bombs.remove(self)
        self.all_objects.remove(self)

    def check_to_boom(self, character, bomb_areas, level, delay_before_areas, bomb_lifetime, db):
        if pygame.time.get_ticks() - self.spawntime > delay_before_areas  and not self.areas_placed:
            self.place_areas(level, bomb_areas, db)
            self.areas_placed = True
        if pygame.time.get_ticks() - self.spawntime > bomb_lifetime:
            self.boom()


    def place_areas(self, level, bomb_areas, db):
        rotate_image = self.area_image
        ignored_blocks = ['1']
        if self.rotate_area:
            rotate_image = pygame.transform.rotate(rotate_image, 90)
        
        area_image = {0: rotate_image, 1: self.area_image}

        for xy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, self.areas_length):
                x = self.coords_list[0] + i * xy[0]
                y = self.coords_list[1] + i * xy[1]
                if level[y][x] not in ignored_blocks:
                    ba = BombArea(x * self.size, y * self.size, self.all_objects, bomb_areas, area_image.get(xy[1]))
                    dblock = pygame.sprite.spritecollideany(ba, db)
                    if dblock is not None:
                        dblock.destroy()
                    bomb_areas.add(ba)
                else:
                    break



class BombArea(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, bomb_areas, area_image):
        self.size = 30
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (self.size, self.size), area_image, color = (200, 50, 50))
        self.force_damage = 100
        self.bomb_areas = bomb_areas
        self.bomb_areas.add(self)

    def check_collide(self, character):
        if pygame.sprite.collide_rect(self, character):
            character.hp -= self.force_damage
