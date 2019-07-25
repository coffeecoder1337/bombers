import pygame
import character
import block
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
        self.running = True
        self.clock = pygame.time.Clock()
        self.level = [
            "111111111111111111111111111111",
            "1#1000000000000000000000000001",
            "101000000000000000000000000001",
            "101111100000000000000000000001",
            "100000000000000000000000000001",
            "111111100000000000000000000001",
            "100000000000000000000000000001",
            "100000000000000000000000000001",
            "100000000000000000000000000001",
            "100000000000000000000000000001",
            "100000000000000000000000000001",
            "100000000000000000000000000001",
            "100000000000000000000000000001",
            "100000000000000000000000000001",
            "111111111111111111111111111111"
        ]

    

    def create_level(self, level):
        x = 0
        y = 0
        for row in level:
            for col in row:
                if col == '1':
                    block.Block(x, y, self.all_objects, self.platforms)
                if col == '#':
                    self.character = character.Character(x, y, self.all_objects)
                x += 30
            y += 30
            x = 0


    def handler(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.running = False
            
            if e.type == KEYDOWN:
                if e.key in (K_LEFT, K_a):
                    self.character.change_direction_x(-1)
                if e.key in (K_RIGHT, K_d):
                    self.character.change_direction_x(1)
                if e.key in (K_DOWN, K_s):
                    self.character.change_direction_y(1)
                if e.key in (K_UP, K_w):
                    self.character.change_direction_y(-1)

                if e.key in (K_SPACE, K_RETURN):
                    self.character.place_bomb(self.bombs)
            
            if e.type == KEYUP:
                if e.key in (K_LEFT, K_a, K_RIGHT, K_d):
                    self.character.change_direction_x(0)
                if e.key in (K_DOWN, K_s, K_UP, K_w):
                    self.character.change_direction_y(0)
    

    def loop(self):
        self.create_level(self.level)
        while self.running:
            self.handler()
            self.character.move(self.platforms)
            for b in self.bombs:
                b.check_to_boom()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()

    
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_objects.draw(self.screen)

    
    def run(self):
        self.loop()
    

    def close(self):
        pass
    

    def pause(self):
        pass



if __name__ == "__main__":
    g = Game().run()