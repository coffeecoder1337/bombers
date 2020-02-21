import pygame
from pygame.locals import *



class Menu(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.size = (900, 450)
        self.image = pygame.Surface(self.size)
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.running = True
        self.font = pygame.font.SysFont('Arial', 21)
        self.main_text = self.font.render('Чтобы играть нажмите Enter. Чтобы выйти нажмите Escape', 1, (255, 255, 255))
        self.game = game

    
    def show(self):
        self.running = True
        self.loop()


    def force_close(self):
        self.running = False
        self.game.running = False


    def close(self):
        self.running = False


    def handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.force_close()
            
            if event.type == KEYDOWN:
                if event.key in [K_RETURN]:
                    self.close()

                if event.key in [K_ESCAPE]:
                    self.force_close()

    def loop(self):
        while self.running:
            self.handler()
            self.game.clock.tick(60)
            self.draw()
            pygame.display.update()


    def draw(self):
        self.game.screen.blit(self.image, (0, 0))
        self.game.screen.blit(self.main_text, self.main_text.get_rect(center=self.game.screen_rect.center))






