import block
import character
import images
import pygame
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        pygame.display.set_caption('Bombers')
        self.screen = pygame.display.set_mode((900, 450))
        self.screen_rect = self.screen.get_rect()
        self.all_objects = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.bomb_areas = pygame.sprite.Group()
        self.ground_blocks = pygame.sprite.Group()
        self.running = True
        self.clock = pygame.time.Clock()
        self.level = None
        self.level_number = 1

    
    def read_level_file(self, filename):
        with open(filename, "r") as level:
            l = level.readlines()
        level.close()
        for line in range(len(l)):
            l[line] = l[line].strip()
        return l


    def create_level(self, level_number):
        x = 0
        y = 0
        cx, cy = (0, 0)
        self.level = self.read_level_file(f"levels\level{level_number}.txt")
        for row in self.level:
            for col in row:
                if col == '1':
                    block.Block(x, y, self.all_objects, self.platforms)
                if col != '1':
                    block.Ground(x, y, self.all_objects, self.ground_blocks)
                if col == '#':
                    cx, cy = (x, y)
                x += 30
            y += 30
            x = 0
        self.character = character.Character(cx, cy, self.all_objects, images.character_blue)




    def handler(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.running = False

            if e.type == KEYDOWN:
                if e.key in (K_LEFT, K_a):
                    self.character.left = 1
                if e.key in (K_RIGHT, K_d):
                    self.character.right = 1
                if e.key in (K_DOWN, K_s):
                    self.character.down = 1
                if e.key in (K_UP, K_w):
                    self.character.up = 1

                if e.key in (K_SPACE, K_RETURN):
                    bx, by = self.character.place_bomb(self.bombs, 100, images.laser, images.laser_area, True)
            
            if e.type == KEYUP:
                if e.key in (K_LEFT, K_a):
                    self.character.left = 0
                if e.key in (K_RIGHT, K_d):
                    self.character.right = 0
                if e.key in (K_DOWN, K_s):
                    self.character.down = 0
                if e.key in (K_UP, K_w):
                    self.character.up = 0
    

    def loop(self):
        self.create_level(self.level_number)
        while self.running:
            self.handler()
            prev_coords = self.character.move(self.platforms, self.ground_blocks)
            self.rotate_character(self.character, prev_coords)
            self.check_bombs_to_boom()
            self.check_bomb_areas_to_remove()
            self.check_lose()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()


    def check_bombs_to_boom(self):
        for b in self.bombs:
            b.check_to_boom(self.character, self.bomb_areas, self.level, 2000, 3000)


    def rotate_character(self, character, prev_coords):
        if character.rect.x > prev_coords[0]:
            character.image = pygame.transform.rotate(character.original_image, 90)
        if character.rect.x < prev_coords[0]:
            character.image = pygame.transform.rotate(character.original_image, -90)
        if character.rect.y > prev_coords[1]:
            character.image = pygame.transform.rotate(character.original_image, 0)
        if character.rect.y < prev_coords[1]:
            character.image = pygame.transform.rotate(character.original_image, 180)
        character.rect = character.image.get_rect(center=character.rect.center)


    def check_bomb_areas_to_remove(self):
        for ba in self.bomb_areas:
            if pygame.time.get_ticks() - ba.spawntime > 500:
                self.all_objects.remove(ba)
                self.bomb_areas.remove(ba)
            else:
                ba.check_collide(self.character)


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_objects.draw(self.screen)

    
    def run(self):
        self.loop()
    

    def check_lose(self):
        if self.character.check_hp():
            print("You Lose")
            self.running = False


    def close(self):
        pass
    

    def pause(self):
        pass



if __name__ == "__main__":
    g = Game().run()