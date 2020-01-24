import asyncio
import character
import block
import pygame
import socket
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self, host = 'localhost', port = 5005):
        pygame.display.set_caption('Bombers')
        self.screen = pygame.display.set_mode((900, 450))
        self.screen_rect = self.screen.get_rect()
        self.all_objects = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.bomb_areas = pygame.sprite.Group()
        self.empty_blocks = pygame.sprite.Group()
        self.running = True
        self.clock = pygame.time.Clock()
        self.level = [
            "111111111111111111111111111111",
            "1#0000010000000100000000100001",
            "111111010111110101111110111101",
            "100000010100000000000010000001",
            "101111010101111101011011111101",
            "101000010101000001000000000001",
            "101011110100010101011010110101",
            "100010000001000101000010100101",
            "111010110101111101111110101101",
            "101010110100000000100000000001",
            "101010110101111110111101011101",
            "101000000100000010000001010001",
            "101111101111111010111101010101",
            "100000000000000010000000000001",
            "111111111111111111111111111111"
        ]

        #network
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.connect((host, port))

        # get symb
        self.client_socket.send("connect".encode())
        self.character_symbol = self.client_socket.recv(64).decode()
        if self.character_symbol == "#":
            self.opponent_symbol = "$"
        else:
            self.opponent_symbol = "#"

    

    def create_level(self, level):
        x = 0
        y = 0
        for row in level:
            for col in row:
                if col == '1':
                    block.Block(x, y, self.all_objects, self.platforms)
                if col != '1':
                    block.Ground(x, y, self.all_objects, self.ground_blocks)
                if col == self.character_symbol:
                    cx, cy = (x, y)
                if col == self.opponent_symbol:
                    ox, oy = (x, y)
                x += 30
            y += 30
            x = 0
        self.character = character.Character(cx, cy, self.all_objects)
        self.opponent = character.Character(ox, oy, self.all_objects)




    def handler(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.running = False
            
            if e.type == KEYDOWN:
                if e.key in (K_LEFT, K_a):
                    self.character.change_direction_x(-1)
                if e.key in (K_RIGHT, K_d):
                    self.character.change_direction_x(1)
                if e.key in (K_DOWN, K_s):
                    self.character.change_direction_y(1)
                if e.key in (K_UP, K_w):
                    self.character.change_direction_y(-1)

                if e.key in (K_SPACE, K_RETURN):
                    bx, by = self.character.place_bomb(self.bombs) # ... sending bx, by
            
            if e.type == KEYUP:
                if e.key in (K_LEFT, K_a, K_RIGHT, K_d):
                    self.character.change_direction_x(0)
                if e.key in (K_DOWN, K_s, K_UP, K_w):
                    self.character.change_direction_y(0)
    
    def loop(self):
        self.create_level(self.level)
        while self.running:
            self.handler()
            # ... recieving opponent rect.x, rect.y
            coords = self.character.move(self.platforms, self.ground_blocks)
            self.client_socket.send(str(coords).encode())
            data = self.client_socket.recv(1024).decode()
            coords = self.parse_coords(data)
            self.opponent.rect.x, self.opponent.rect.y = coords[0], coords[1]
            self.check_bombs_to_boom()
            self.check_bomb_areas_to_remove()
            self.check_lose()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()

    def parse_coords(self, coords):
        coords = coords.strip("'()'").split(", ")
        return (int(coords[0]), int(coords[1]))

    def check_bombs_to_boom(self):
        for b in self.bombs:
                b.check_to_boom(self.character, self.bomb_areas, self.level)


    def check_bomb_areas_to_remove(self):
        for ba in self.bomb_areas:
            if pygame.time.get_ticks() - ba.spawntime > 500:
                self.all_objects.remove(ba)
                self.bomb_areas.remove(ba)


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_objects.draw(self.screen)

    
    def run(self):
        self.loop()
    

    def check_lose(self):
        if self.character.check_hp():
            print("You Lose")
            self.running = False


    def close(self):
        pass
    

    def pause(self):
        pass



if __name__ == "__main__":
    g = Game().run()