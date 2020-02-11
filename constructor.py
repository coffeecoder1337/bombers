import block
import character
import hud
import images
import pygame
from pygame.locals import *


class GridRect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))


class Constructor:
    def __init__(self):
        pygame.display.set_caption("Bomber | Level Constructor")
        self.screen = pygame.display.set_mode((900, 510))
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
        hud.HudItem(images.block, self.items)
        hud.HudItem(images.block_2, self.items)
        hud.HudItem(images.ground_2, self.items)
        hud.HudItem(images.blue_ground_2, self.items)
        hud.HudItem(images.blue_ground, self.items)
        hud.HudItem(images.red_ground_2, self.items)
        hud.HudItem(images.red_ground, self.items)
        hud.HudItem(images.character_red, self.items)
        hud.HudItem(images.character_blue, self.items)
        self.hud = hud.BaseHudBar(self.items, self.all_objects, self.slots)
        self.clock = pygame.time.Clock()
    

    def draw_grid(self, width=30, height=15):
        surf = pygame.Surface((30 * width, 30 * height))
        surf_rect = surf.get_rect()
        surf_rect.y = hud.SLOT_SIZE
        surf.set_colorkey((2, 2, 2))
        surf.fill((100, 0, 100))
        grid = []
        for y in range(height):
            line = []
            for x in range(width):
                r = pygame.Rect(x * 30, y * 30, 30, 30)
                line.append(r)
                pygame.draw.rect(surf, pygame.Color('grey'), r, 1)
            grid.append(line)

        return grid, surf, surf_rect


    def run(self):
        self.loop()


    def loop(self):
        while self.running:
            self.handler()
            self.draw()


    def draw(self):
        self.screen.fill((255, 255, 255))
        grid, grid_surf, surf_rect = self.draw_grid()
        self.screen.blit(grid_surf, surf_rect)
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


