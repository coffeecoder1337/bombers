import pygame
import base_game_object
from pygame.locals import *



class Bomb(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, bombs):
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (30, 30))
        self.image.fill((230, 20, 20))
        self.bombs = bombs
        self.spawntime = pygame.time.get_ticks()
        self.bombs.add(self)
    

    def boom(self):
        self.bombs.remove(self)
        self.all_objects.remove(self)

    
    def check_to_boom(self, character, bomb_areas):
        if pygame.time.get_ticks() - self.spawntime > 2000:
            b = BombArea(self.rect.centerx, self.rect.centery, self.all_objects, bomb_areas)
            b.check_collide(character)
            self.boom()



class BombArea(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, bomb_areas):
        size = (w, h) = (100, 100)
        base_game_object.BaseGameObject.__init__(self, x - w/2, y - h/2, all_objects, size)
        self.force_damage = 100
        self.bomb_areas = bomb_areas
        self.bomb_areas.add(self)
        self.image.fill((200, 50, 50))

    def check_collide(self, character):
        if pygame.sprite.collide_rect(self, character):
            character.hp -= self.force_damage
