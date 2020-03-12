import block
import character
import hud
import images
import pygame
from pygame.locals import *



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


        self.gb = None
        self.grid = None
        self.pressed = False
        self.items = []
        self.slots = []
        self.level = []

        ground = hud.HudItem(images.ground, self.items, "0")
        hud.HudItem(images.block, self.items, "1")
        hud.HudItem(images.block_2, self.items, "2")
        hud.HudItem(images.ground_2, self.items, "3")
        hud.HudItem(images.blue_ground_2, self.items, "4")
        hud.HudItem(images.blue_ground, self.items, "5")
        hud.HudItem(images.red_ground_2, self.items, "6")
        hud.HudItem(images.red_ground, self.items, "7")
        hud.HudItem(images.destructible_block[0], self.items, "8")
        hud.HudItem(images.character_blue, self.items, "#")
        hud.HudItem(images.character_red, self.items, "$")
        self.hud = hud.BaseHudBar(self.items, self.all_objects, self.slots)
        self.hud.draw_items()
        self.cur_item = ground
        self.clock = pygame.time.Clock()
    

    def get_item_by_symbol(self, symbol):
        for item in self.items:
            if item.symbol == symbol:
                return item


    def place_item(self, mouse, gb):
        item = self.get_item_by_symbol(self.cur_item.symbol)
        self.level[int((gb.y)/30)][int(gb.x/30)] = self.cur_item.symbol


    def draw_grid(self, width=30, height=15):
        surf = pygame.Surface((30 * width, 30 * height))
        surf_rect = surf.get_rect()
        surf_rect.y = hud.SLOT_SIZE
        grid = []
        for y, row in enumerate(self.level):
            line = []
            for x, col in enumerate(row):
                i = self.get_item_by_symbol(col).image
                r = i.get_rect()
                r.x, r.y = x * 30, y * 30
                line.append(r)
                surf.blit(i, r)
            grid.append(line)
        return grid, surf, surf_rect


    def get_grid_block(self, mouse):
        x, y = mouse[0], mouse[1] - 60
        if self.grid is not None:
            for row in self.grid:
                for col in row:
                    if col.collidepoint(x, y):
                        # print(col.x, col.y, x, y)
                        return col


    def run(self):
        self.load_level()
        self.loop()


    def loop(self):
        while self.running:
            self.handler()
            self.draw()


    def drawing(self):
        if self.gb is not None:
            if self.pressed:
                self.place_item(self.mouse, self.gb)


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.grid, grid_surf, surf_rect = self.draw_grid()
        self.screen.blit(grid_surf, surf_rect)
        self.drawing()
        self.all_objects.update()
        self.all_objects.draw(self.screen)
        self.clock.tick(60)
        pygame.display.update()

    
    def close(self):
        self.save_level()
        self.running = False


    def handler(self):
        for event in pygame.event.get():
            self.mouse = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.close()
            
            if event.type == MOUSEMOTION:
                for slot in self.slots:
                    slot.check_intersection(self.mouse)
                self.gb = self.get_grid_block(self.mouse)
                
            
            if event.type == MOUSEBUTTONDOWN:
                self.pressed = True
                for slot in self.slots:
                    item = slot.check_intersection(self.mouse)
                    if item is not None:
                        self.cur_item = item
                

            if event.type == MOUSEBUTTONUP:
                self.pressed = False


    def load_level(self):
        try:
            with open("level.txt", "r") as f:
                level = f.readlines()
                self.level = [list(x.strip()) for x in level]
        except:
            self.level = [["0" for x in range(30)] for y in range(15)]



    def save_level(self):
        text = ""
        with open("level.txt", "w") as f:
            for row in self.level:
                for col in row:
                    text += col
                text += "\n"
            f.write(text)
        f.close()


    def convert_level_to_file(self):
        pass


    def conver_file_to_level(self):
        pass


constructor = Constructor()
constructor.run()


