import background
import base_game_object
import images
import loader
import pygame
from pygame.locals import *


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, buttons, screen, size, text, on_press, img):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.image = self.img[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen
        self.hover = False
        self.on_press = on_press
        buttons.add(self)
    

    def check_intersection(self, mouse):
        if self.rect.collidepoint(mouse):
            return True
        return False


    def update(self):
        if self.hover:
            self.image = self.img[1]
        else:
            self.image = self.img[0]



class HelpPage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.help_page
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Menu(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.size = game.screen_rect.width, game.screen_rect.height
        self.image = pygame.Surface(self.size)
        self.image.fill((0, 0, 0))
        self.image.set_alpha(150)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.running = True
        self.showing_help = False
        self.game = game
        self.all_objects = pygame.sprite.Group()
        self.background = background.Background(self.rect.center)
        self.all_objects.add(self.background)
        self.help_page = HelpPage(0, 0)
        self.buttons = pygame.sprite.Group()
        MenuButton(10, 100, self.buttons, self.image, (150, 50), "Играть", self.close, images.play_btn)
        MenuButton(10, 170, self.buttons, self.image, (150, 50), "Помощь", self.show_help, images.help_btn)
        MenuButton(10, 240, self.buttons, self.image, (150, 50), "Выход", self.force_close, images.quit_btn)
        
    
    def show(self):
        self.running = True
        self.loop()


    def show_help(self):
        if self.showing_help:
            self.showing_help = False
        else:
            self.showing_help = True


    def force_close(self):
        self.running = False
        self.game.running = False


    def close(self):
        self.running = False
        self.game.running = True


    def handler(self):
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.force_close()
                

            if event.type == MOUSEMOTION:
                for button in self.buttons:
                    if button.check_intersection(mouse):
                        button.hover = True
                    else:
                        button.hover = False
            

            if event.type == MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.check_intersection(mouse):
                        button.on_press()

    def loop(self):
        while self.running:
            self.handler()
            self.draw()
            self.game.clock.tick(60)
            pygame.display.update()


    def draw(self):
        self.all_objects.draw(self.game.screen)
        self.all_objects.update()
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.showing_help:
            self.game.screen.blit(self.help_page.image, (0, 0))
        self.buttons.draw(self.game.screen)
        self.buttons.update()

