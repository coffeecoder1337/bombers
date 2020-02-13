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
        self.destructible_blocks = pygame.sprite.Group()
        self.running = True
        self.clock = pygame.time.Clock()
        self.level = None
        self.level_number = 1
        self.blocks = {
            "0": block.Ground,
            "1": block.Block,
            "2": block.Block2,
            "3": block.Ground2,
            "4": block.BlueGround2,
            "5": block.BlueGround,
            "6": block.RedGround2,
            "7": block.RedGround,
            "8": block.DestructibleBlock
        }

    
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
        ox, oy = 0, 0
        cx, cy = 0, 0
        self.level = self.read_level_file(f"levels\level{level_number}.txt")
        for row in self.level:
            for col in row:
                if col == '#':
                    cx, cy = (x, y)
                elif col == '$':
                    ox, oy = (x, y)
                else:
                    self.blocks[col](x, y, self.all_objects, platforms=self.platforms, ground_blocks=self.ground_blocks, destructible_blocks=self.destructible_blocks)
                x += 30
            y += 30
            x = 0
        block.BlueGround2(cx, cy, self.all_objects, self.ground_blocks)
        block.RedGround2(ox, oy, self.all_objects, self.ground_blocks)
        self.character = character.Character(cx, cy, self.all_objects, images.character_blue)
        self.opponent = character.Character(ox, oy, self.all_objects, images.character_red)




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
            b.check_to_boom(self.character, self.bomb_areas, self.level, 2000, 3000, self.destructible_blocks)


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
        self.all_objects.update()
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