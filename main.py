import pygame
import character
import block
import socket
from select import select
import pickle
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self, ip):
        self.id = None
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
        self.level = None
        self.character = None
        self.enemy = None

        self.to_monitor = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, 5001))
        data = pickle.loads(self.sock.recv(4096))
        self.id = None
        self.parse_data(data)
        self.to_monitor.append(self.sock)
        self.sock.setblocking(0)


    def parse_data(self, data):
        if data['type'] == 'connected':
            print(data)
            self.pause = data['pause']
            self.id = data['id']
            self.level = data['level']
            self.character = character.Character(data['spawn_coords'][0], data['spawn_coords'][1], self.all_objects, self.id)
            self.enemy = character.Enemy(data['enemy_spawn_coords'][0], data['enemy_spawn_coords'][1], self.all_objects, self.id)
        
        if data['type'] == 'change_direction':
            if data['direction_x'] is not None:
                self.enemy.change_direction_x(data['direction_x'])
            if data['direction_y'] is not None:
                self.enemy.change_direction_y(data['direction_y'])
        
        if data['type'] == 'unpause':
            print(data)
            self.pause = False


    def create_level(self, level):
        x = 0
        y = 0
        for row in level:
            for col in row:
                if col == '1':
                    block.Block(x, y, self.all_objects, self.platforms)
                if col != '1':
                    block.Empty(x, y, self.empty_blocks)
                x += 30
            y += 30
            x = 0


    def handler(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.running = False
            
            if e.type == KEYDOWN:
                dirx = None
                diry = None
                if e.key in (K_LEFT, K_a):
                    self.character.change_direction_x(-1)
                    dirx = -1
                if e.key in (K_RIGHT, K_d):
                    self.character.change_direction_x(1)
                    dirx = 1
                if e.key in (K_DOWN, K_s):
                    self.character.change_direction_y(1)
                    diry = 1
                if e.key in (K_UP, K_w):
                    self.character.change_direction_y(-1)
                    diry = -1
                data = {
                    'type': 'change_direction',
                    'id': self.id,
                    'direction_x': dirx,
                    'direction_y': diry
                }
                self.sock.send(pickle.dumps(data))

                if e.key in (K_SPACE, K_RETURN):
                    self.character.place_bomb(self.bombs)
            
            if e.type == KEYUP:
                dirx = None
                diry = None
                if e.key in (K_LEFT, K_a, K_RIGHT, K_d):
                    self.character.change_direction_x(0)
                    dirx = 0
                if e.key in (K_DOWN, K_s, K_UP, K_w):
                    self.character.change_direction_y(0)
                    diry = 0
                data = {
                    'type': 'change_direction',
                    'id': self.id,
                    'direction_x': dirx,
                    'direction_y': diry
                }
                self.sock.send(pickle.dumps(data))
    

    def loop(self):
        self.create_level(self.level)
        while self.running:
            self.sock.settimeout(0.01)
            try:
                data = pickle.loads(self.sock.recv(4096))
                self.sock.settimeout(1)
            except:
                pass
            else:
                self.parse_data(data)

            self.handler()
            self.character.move(self.platforms, self.empty_blocks)
            self.enemy.move(self.platforms, self.empty_blocks)
            self.check_bombs_to_boom()
            self.check_bomb_areas_to_remove()
            self.check_lose()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()


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
        print('waiting for player')
        while self.pause:
            self.sock.settimeout(0.01)
            try:
                data = pickle.loads(self.sock.recv(4096))
                self.sock.settimeout(1)
            except:
                pass
            else:
                self.parse_data(data)
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
    g = Game('localhost').run()