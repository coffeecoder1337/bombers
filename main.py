import pygame
from pygame.locals import *


class Game:
    def __init__(self):
        pygame.display.set_caption('Bombers')
        self.screen = pygame.display.set_mode((500, 500))
        self.running = True
    

    def handler(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.running = False
    

    def loop(self):
        while self.running:
            self.handler()
            self.draw()

    
    def draw(self):
        pass

    
    def run(self):
        self.loop()
    

    def close(self):
        pass
    

    def pause(self):
        pass

if __name__ == "__main__":
    g = Game().run()