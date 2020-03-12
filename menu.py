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



class Menu(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.size = game.screen_rect.width, game.screen_rect.height
        self.image = pygame.Surface(self.size)
        # self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.running = True
        self.game = game
        self.background = background.Background(self.rect.center)
        self.all_objects = pygame.sprite.Group()
        self.all_objects.add(self.background)
        self.buttons = pygame.sprite.Group()
        MenuButton(10, 100, self.buttons, self.image, (150, 50), "Играть", self.close, images.play_btn)
        MenuButton(10, 170, self.buttons, self.image, (150, 50), "Помощь", self.show_help, images.help_btn)
        MenuButton(10, 240, self.buttons, self.image, (150, 50), "Выход", self.force_close, images.quit_btn)
        
    
    def show(self):
        self.running = True
        self.loop()


    def show_help(self):
        pass


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
            
            if event.type == KEYDOWN:
                if event.key in [K_RETURN]:
                    self.close()

                if event.key in [K_ESCAPE]:
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
        self.game.screen.blit(self.image, (0, 0))
        self.all_objects.draw(self.image)
        self.buttons.draw(self.image)
        self.all_objects.update()
        self.buttons.update()






