import pygame
import images
import base_game_object
from pygame.locals import *



class Bomb(base_game_object.BaseGameObject):
    def __init__(self, x, y, all_objects, bombs):
        self.size = 30
        base_game_object.BaseGameObject.__init__(self, x, y, all_objects, (self.size, self.size), images.laser, color = (200, 50, 50))
        self.bombs = bombs
        self.spawntime = pygame.time.get_ticks()
        self.coords_list = [int(self.rect.x / self.size), int(self.rect.y / self.size)]
        self.areas_length = 100
        self.area_image = images.laser_area
        self.rotate_area = True
        self.areas_placed = False
        self.bombs.add(self)
    

    def boom(self):
        self.bombs.remove(self)
        self.all_objects.remove(self)

    def check_to_boom(self, character, bomb_areas, level, delay_before_areas, bomb_lifetime, db):
        if pygame.time.get_ticks() - self.spawntime > delay_before_areas and not self.areas_placed:
            self.place_areas(level, bomb_areas, db)
            self.areas_placed = True
        if pygame.time.get_ticks() - self.spawntime > bomb_lifetime:
            self.boom()


    def place_areas(self, level, bomb_areas, db):
        rotate_image = self.area_image
        ignored_blocks = ['1', '2']
        if self.rotate_area:
            rotate_image = pygame.transform.rotate(rotate_image, 90)
        
        area_image = {0: rotate_image, 1: self.area_image}

        for xy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, self.areas_length):
                x = self.coords_list[0] + i * xy[0]
                y = self.coords_list[1] + i * xy[1]
                try:
                    if level[y][x] not in ignored_blocks:
                        ba = BombArea(x * self.size, y * self.size, self.all_objects, bomb_areas, area_image.get(abs(xy[1])))
                        dblock = pygame.sprite.spritecollideany(ba, db)
                        if dblock is not None:
                            dblock.destroy()
                        bomb_areas.add(ba)
                    else:
                        break
                except:
                    pass


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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, all_objects, bullets, character, dirx, diry, platforms, opponent):
        pygame.sprite.Sprite.__init__(self)
        if diry == -1:
            self.image = images.bullet
        if diry == 1:
            self.image = pygame.transform.rotate(images.bullet, 180)
        if diry == 0:
            self.image = pygame.transform.rotate(images.bullet, 90 * dirx)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.platforms = platforms
        self.bullets = bullets
        self.dirx = dirx
        self.diry = diry
        self.speed = 5
        self.force_damage = 50
        self.character = character
        self.opponent = opponent
        self.all_objects =  all_objects
        self.bullets.add(self)
        self.all_objects.add(self)


    def move(self):
        self.rect.x += self.speed * self.dirx
        self.rect.y += self.speed * self.diry
    

    def update(self):
        self.move()
        if pygame.sprite.collide_rect(self, self.character):
            self.character.hp -= self.force_damage
        if pygame.sprite.collide_rect(self, self.character) or pygame.sprite.collide_rect(self, self.opponent):
            self.bullets.remove(self)
            self.all_objects.remove(self)
        if pygame.sprite.spritecollide(self, self.platforms, False):
            self.bullets.remove(self)
            self.all_objects.remove(self)



class ShootingBomb(pygame.sprite.Sprite):
    def __init__(self, x, y, all_objects, shooting_bombs):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.shooting_bomb
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawntime = pygame.time.get_ticks()
        self.all_objects =  all_objects
        self.shooting_bombs =  shooting_bombs
        self.shooting_bombs.add(self)
        self.shooted = False
        self.all_objects.add(self)


    def boom(self):
        self.shooting_bombs.remove(self)
        self.all_objects.remove(self)


    def check_to_boom(self, character, bomb_areas, level, delay_before_areas, bomb_lifetime, db, bullets, platforms, opponent):
        if pygame.time.get_ticks() - self.spawntime > delay_before_areas and not self.shooted:
            self.shoot(bullets, character, platforms, opponent)
            self.shooted = True
        if pygame.time.get_ticks() - self.spawntime > bomb_lifetime:
            self.boom()


    def shoot(self, bullets, character, platforms, opponent):
        for x in [1, -1]:
            b = Bullet(self.rect.centerx, self.rect.centery, self.all_objects, bullets, character, x, 0, platforms, opponent)
        
        for y in [1, -1]:
            b = Bullet(self.rect.centerx, self.rect.centery, self.all_objects, bullets, character, 0, y, platforms, opponent)
