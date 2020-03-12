import images
import pygame
from pygame.locals import *


SLOT_SIZE = 60


class HudItem(pygame.sprite.Sprite):
    def __init__(self, image, items, symbol=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.items = items
        self.symbol = symbol
        self.items.append(self)


class HudSlot(pygame.sprite.Sprite):
    def __init__(self, color, slots):
        pygame.sprite.Sprite.__init__(self)
        self.size = SLOT_SIZE
        self.base_color = color
        self.hover_color = (100, 0, 100)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.hover = False
        self.slots = slots
        self.item = None
        self.slots.append(self)

    
    def check_intersection(self, mouse):
        if self.rect.collidepoint(mouse):
            self.hover = True
            return self.item
        else:
            self.hover = False
    

    def update(self):
        if self.hover:
            self.image.fill(self.hover_color)
        else:
            self.image.fill(self.base_color)
        self.rect = self.image.get_rect(center=self.rect.center)


        
class BaseHudBar(pygame.sprite.Sprite):
    def __init__(self, items, all_objects, slots):
        pygame.sprite.Sprite.__init__(self)
        self.slot_size = SLOT_SIZE
        self.image = pygame.Surface((self.slot_size, self.slot_size))
        self.items = items
        self.all_objects = all_objects
        self.slots = slots
        self.rect = self.image.get_rect()
        self.size = self.slot_size * len(self.items)
        self.ypos = 10
        self.width = 0
        self.count = 0


    def draw_items(self):
        for x, item in enumerate(self.items):
            hs = HudSlot((255, 100, 35), self.slots)
            hs.rect.x = x * self.slot_size
            hs.rect.y = self.rect.y
            hs.item = item
            item.rect.centerx = hs.rect.centerx
            item.rect.centery = hs.rect.centery
            self.all_objects.add(hs)
            self.all_objects.add(item)



class GameHudSlot(pygame.sprite.Sprite):
    def __init__(self, slots, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (60, 60))
        self.rect = self.image.get_rect()
        self.slots = slots
        self.item = None
        self.slots.append(self)


# text1 = f1.render(text, 1, color)
# sc.blit(text1, (10, 50))
class StatusBar(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((600, 80))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 0
        self.font_big = pygame.font.Font('fonts/Crystal.ttf', 72)
        self.font_small = pygame.font.Font('fonts/Crystal.ttf', 36)
        self.game = game
        if self.game.character_symbol == "#":
            self.blue = self.game.character
            self.red = self.game.opponent
        else:
            self.blue = self.game.opponent
            self.red = self.game.character
    
    def update(self):
        self.image.fill((0, 0, 0))
        x = self.game.timer - self.game.timer // 60 * 60
        if len(str(x)) == 1:
            x = "0" + str(x)
        self.timer = f"{self.game.timer // 60}:{x}"
        self.timer_text = self.font_big.render(self.timer, 1, (255, 255 , 255))
        self.blue_score = f"blue {self.blue.score}"
        self.red_score = f"red {self.red.score}"
        self.blue_score_text = self.font_small.render(self.blue_score, 1, (34, 53, 255))
        self.red_score_text = self.font_small.render(self.red_score, 1, (255, 30, 60))
        self.image.blit(self.timer_text, self.timer_text.get_rect(x=self.rect.x))
        self.image.blit(self.blue_score_text, self.blue_score_text.get_rect(x=self.rect.x + 150, y=0))
        self.image.blit(self.red_score_text, self.red_score_text.get_rect(x=self.rect.x + 150, y=40))
        self.hp = f"{self.game.character.hp}%"
        self.hp_text = self.font_small.render(self.hp, 1, (255, 255, 255))
        self.image.blit(self.hp_text, self.hp_text.get_rect(x=self.rect.x + 300, centery=self.rect.centery))


class GameHudBar(BaseHudBar):
    def __init__(self, items, all_objects, slots, game):
        BaseHudBar.__init__(self, items, all_objects, slots)
        self.slots = slots
        self.items = items
        self.sb = StatusBar(game)
        self.all_objects = all_objects
        self.all_objects.add(self.sb)
    

    def draw_items(self):
        for item in self.items:
            if self.count == 0:
                img = images.item_holder1
                gutter = 0
            else:
                img = images.item_holder2
                gutter = 3
            hs = GameHudSlot(self.slots, img)
            hs.rect.x = self.width + hs.rect.width
            hs.rect.y = self.ypos
            self.width += hs.rect.width - 5
            hs.item = item
            item.rect.centerx = hs.rect.centerx + gutter
            item.rect.centery = hs.rect.centery
            self.count += 1
            self.all_objects.add(hs)
            self.all_objects.add(item)



