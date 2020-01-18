import pygame
import base_game_object
from pygame.locals import *



class Bomb(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, bombs):
        self.size = 30
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (self.size, self.size))
        self.image.fill((230, 20, 20))
        self.bombs = bombs
        self.spawntime = pygame.time.get_ticks()
        self.coords_list = [int(self.rect.x / self.size), int(self.rect.y / self.size)]
        self.areas_length = 4
        self.bombs.add(self)
    

    def boom(self):
        self.bombs.remove(self)
        self.all_objects.remove(self)

    
    def check_to_boom(self, character, bomb_areas, level):
        if pygame.time.get_ticks() - self.spawntime > 2000:
            self.place_areas(level, bomb_areas)
            for b in bomb_areas:
                b.check_collide(character)
            self.boom()


    def place_areas(self, level, bomb_areas):
        for x in range(self.areas_length):
            x = self.coords_list[0] + x
            y = self.coords_list[1]
            if level[y][x] != '1':
                bomb_areas.add(BombArea(x * self.size, y * self.size, self.all_objects, bomb_areas))
            else:
                break
        
        for x in range(1, self.areas_length):
            x = self.coords_list[0] + x * (-1)
            y = self.coords_list[1]
            if level[y][x] != '1':
                bomb_areas.add(BombArea(x * self.size, y * self.size, self.all_objects, bomb_areas))
            else:
                break
        
        for y in range(self.areas_length):
            x = self.coords_list[0]
            y = self.coords_list[1] + y
            if level[y][x] != '1':
                bomb_areas.add(BombArea(x * self.size, y * self.size, self.all_objects, bomb_areas))
            else:
                break
        
        for y in range(1, self.areas_length):
            x = self.coords_list[0]
            y = self.coords_list[1] + y * (-1)
            if level[y][x] != '1':
                bomb_areas.add(BombArea(x * self.size, y * self.size, self.all_objects, bomb_areas))
            else:
                break


class BombArea(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, bomb_areas):
        self.size = 30
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (self.size, self.size))
        self.force_damage = 100
        self.bomb_areas = bomb_areas
        self.bomb_areas.add(self)
        self.image.fill((200, 50, 50))

    def check_collide(self, character):
        if pygame.sprite.collide_rect(self, character):
            character.hp -= self.force_damage
