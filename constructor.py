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

        self.grid = None
        self.items = []
        self.slots = []
        self.level = []

        hud.HudItem(images.ground, self.items, "0")
        hud.HudItem(images.block, self.items, "1")
        hud.HudItem(images.block_2, self.items, "2")
        hud.HudItem(images.ground_2, self.items, "3")
        hud.HudItem(images.blue_ground_2, self.items, "4")
        hud.HudItem(images.blue_ground, self.items, "5")
        hud.HudItem(images.red_ground_2, self.items, "6")
        hud.HudItem(images.red_ground, self.items, "7")
        hud.HudItem(images.character_red, self.items, "#")
        hud.HudItem(images.character_blue, self.items, "$")
        self.hud = hud.BaseHudBar(self.items, self.all_objects, self.slots)
        self.clock = pygame.time.Clock()
    

    def draw_grid(self, width=30, height=15):
        surf = pygame.Surface((30 * width, 30 * height))
        surf_rect = surf.get_rect()
        surf_rect.y = hud.SLOT_SIZE
        grid = []
        for y in range(height):
            line = []
            for x in range(width):
                i = images.ground
                r = i.get_rect()
                r.x, r.y = x * 30, y * 30
                line.append(r)
                surf.blit(images.ground, r)
            grid.append(line)
        return grid, surf, surf_rect


    def get_grid_block(self, mouse):
        if self.grid is not None:
            for row in self.grid:
                for col in row:
                    if col.collidepoint(mouse):
                        return col.x, col.y


    def run(self):
        self.loop()


    def loop(self):
        while self.running:
            self.handler()
            self.draw()


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.grid, grid_surf, surf_rect = self.draw_grid()
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
                self.cur_grid_block = self.get_grid_block(mouse)


    def save_level(self):
        pass


    def convert_level_to_file(self):
        pass


    def conver_file_to_level(self):
        pass


constructor = Constructor()
constructor.run()


