import character
import block
import bomb
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
        self.ground_blocks = pygame.sprite.Group()
        self.running = True
        self.clock = pygame.time.Clock()
        self.level = None
        self.level_number = 1

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

    
    def read_level_file(self, filename):
        with open(filename, "r") as level:
            l = level.readlines()
        level.close()
        for line in range(len(l)):
            l[line] = l[line].strip()
        return l


    def create_level(self, level_number):
        x = 0
        y = 0
        cx, cy = (0, 0)
        self.level = self.read_level_file(f"levels\level{level_number}.txt")
        for row in self.level:
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
                    self.client_socket.send(f"bomb ({str(bx)}, {str(by)})".encode())
            
            if e.type == KEYUP:
                if e.key in (K_LEFT, K_a, K_RIGHT, K_d):
                    self.character.change_direction_x(0)
                if e.key in (K_DOWN, K_s, K_UP, K_w):
                    self.character.change_direction_y(0)
    
    def loop(self):
        self.create_level(self.level_number)
        while self.running:
            self.handler()
            # ... recieving opponent rect.x, rect.y
            coords = self.character.move(self.platforms, self.ground_blocks)
            self.client_socket.send(f"move {str(coords)}".encode())
            data = self.client_socket.recv(1024).decode()
            self.parse_data(data)
            self.check_bombs_to_boom()
            self.check_bomb_areas_to_remove()
            self.check_lose()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()

    def parse_data(self, data): # 'bomb (34, 434)'
        data = data.strip("'").split()
        coords = data[1].strip("(,"), data[2].strip(")")
        cx, cy = int(coords[0]), int(coords[1])
        if data[0] == 'bomb':
            bomb.Bomb(cx, cy, self.all_objects, self.bombs)
        if data[0] == 'move':
            self.opponent.rect.x, self.opponent.rect.y = cx, cy

    def check_bombs_to_boom(self):
        for b in self.bombs:
            b.check_to_boom(self.character, self.bomb_areas, self.level)


    def check_bomb_areas_to_remove(self):
        for ba in self.bomb_areas:
            if pygame.time.get_ticks() - ba.spawntime > 500:
                self.all_objects.remove(ba)
                self.bomb_areas.remove(ba)
            else:
                ba.check_collide(self.character)


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