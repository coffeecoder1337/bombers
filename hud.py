import images
import pygame
from pygame.locals import *



class HudItem(pygame.sprite.Sprite):
    def __init__(self, image, items):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.items = items
        self.items.append(self)


class HudSlot(pygame.sprite.Sprite):
    def __init__(self, color, slots):
        pygame.sprite.Sprite.__init__(self)
        self.base_color = color
        self.hover_color = (100, 0, 100)
        self.image = pygame.Surface((60, 60))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.hover = False
        self.slots = slots
        self.slots.append(self)

    
    def check_intersection(self, mouse):
        if self.rect.x < mouse[0] < self.rect.x + self.rect.width and self.rect.y < mouse[1] < self.rect.y + self.rect.height:
            self.hover = True
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
        self.slot_size = 60
        self.start = 0, 0
        self.items = items
        self.all_objects = all_objects
        self.slots = slots
        self.size = self.slot_size * len(self.items)
        self.image = pygame.Surface((self.size, 60))
        self.image.fill((0, 0, 0))
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.draw_items()
        self.all_objects.add(self)


    def draw_items(self):
        for x, item in enumerate(self.items):
            hs = HudSlot((255, 100, 35), self.slots)
            hs.rect.x = x * self.slot_size
            hs.rect.y = self.rect.y
            item.rect.centerx = hs.rect.centerx
            item.rect.centery = hs.rect.centery
            self.all_objects.add(hs)
            self.all_objects.add(item)






