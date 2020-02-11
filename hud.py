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

        
        
class BaseHudBar(pygame.sprite.Sprite):
    def __init__(self, items, all_objects):
        pygame.sprite.Sprite.__init__(self)
        self.slot_size = 60
        self.start = 0, 0
        self.items = items
        self.all_objects = all_objects
        self.size = self.slot_size * len(self.items)
        self.image = pygame.Surface((self.size, 60))
        self.image.fill((0, 0, 0))
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.draw_items()
        self.all_objects.add(self)


    def draw_items(self):
        for x, item in enumerate(self.items):
            item.rect.centerx = (x + 1) * self.slot_size - self.slot_size / 2
            item.rect.centery = self.rect.centery
            self.all_objects.add(item)
            print(self.items)






