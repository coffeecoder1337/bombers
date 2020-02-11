import block
import character
import hud
import images
import pygame
from pygame.locals import *


class Constructor:
    def __init__(self):
        pygame.display.set_caption("Bomber | Level Constructor")
        self.screen = pygame.display.set_mode((900, 450))
        self.screen_rect = self.screen.get_rect()
        self.all_objects = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.bomb_areas = pygame.sprite.Group()
        self.ground_blocks = pygame.sprite.Group()
        self.destructible_blocks = pygame.sprite.Group()
        self.character = None
        self.opponent = None
        self.running = True

        self.items = []
        self.slots = []

        hud.HudItem(images.ground, self.items)
        hud.HudItem(images.laser, self.items)
        self.hud = hud.BaseHudBar(self.items, self.all_objects, self.slots)
        
        self.clock = pygame.time.Clock()
    

    def run(self):
        self.loop()


    def loop(self):
        while self.running:
            self.handler()
            self.draw()


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_objects.update()
        self.all_objects.draw(self.screen)
        self.clock.tick(60)
        pygame.display.update()

    
    def close(self):
        self.save_level()
        self.running = False


    def handler(self):
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.close()
            
            if event.type == MOUSEMOTION:
                for slot in self.slots:
                    slot.check_intersection(mouse)


    def save_level(self):
        pass


    def convert_level_to_file(self):
        pass


    def conver_file_to_level(self):
        pass


constructor = Constructor()
constructor.run()


