import pygame
import character
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        pygame.display.set_caption('Bombers')
        self.screen = pygame.display.set_mode((500, 500))
        self.screen_rect = self.screen.get_rect()
        self.all_objects = pygame.sprite.Group()
        self.running = True
        self.clock = pygame.time.Clock()
        self.character = character.Character(self.screen_rect.centerx, self.screen_rect.centery, self.all_objects)
    

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
            
            if e.type == KEYUP:
                if e.key in (K_LEFT, K_a, K_RIGHT, K_d):
                    self.character.change_direction_x(0)
                if e.key in (K_DOWN, K_s, K_UP, K_w):
                    self.character.change_direction_y(0)
    

    def loop(self):
        while self.running:
            self.handler()
            self.character.move()
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