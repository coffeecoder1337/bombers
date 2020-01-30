import character
import block
import bomb
import NetworkObject
import pickle
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
        self.host = host
        self.port = port

    
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
                NetworkObject.NetworkObject(event="left").send_to_server(self.client_socket)
                self.client_socket.close()
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
                    NetworkObject.NetworkObject(event="bomb", coords=(bx, by), hp=self.character.hp, game_id=self.game_id).send_to_server(self.client_socket)
                    data = pickle.loads(self.client_socket.recv(2048))
                    print(data.event)
                    # self.client_socket.send(f"bomb ({str(bx)}, {str(by)}) {self.character.hp}".encode())
            
            if e.type == KEYUP:
                if e.key in (K_LEFT, K_a, K_RIGHT, K_d):
                    self.character.change_direction_x(0)
                if e.key in (K_DOWN, K_s, K_UP, K_w):
                    self.character.change_direction_y(0)
    
    def loop(self):
        self.create_level(self.level_number)
        if self.character_symbol == "#":
            while True:
                data = pickle.loads(self.client_socket.recv(2048))
                print(data.event)
                if data.event == "opponent":
                    break

        while self.running:
            self.handler()
            # ... recieving opponent rect.x, rect.y
            coords = self.character.move(self.platforms, self.ground_blocks)
            try:
                NetworkObject.NetworkObject(event="move", coords=coords, hp=self.character.hp, game_id=self.game_id).send_to_server(self.client_socket)
                # self.client_socket.send(f"move {str(coords)} {self.character.hp}".encode())
                data = pickle.loads(self.client_socket.recv(2048))
                print(data)
            except Exception as e:
                print(e)
                print("opponent left the game. exit...")
                raise SystemExit
            else:
                self.parse_data(data)
                self.check_bombs_to_boom()
                self.check_bomb_areas_to_remove()
                self.check_lose()
                self.draw()
                self.clock.tick(60)
                pygame.display.update()

    def parse_data(self, data):
        print(data.event)
        if data.event == 'left':
            self.running = False
            NetworkObject.NetworkObject(event="left").send_to_server(self.client_socket)
            self.client_socket.close()
            print("opponent left the game")
            return

        self.opponent.hp = data.hp
        if data.event == 'bomb':
            bomb.Bomb(data.coords[0], data.coords[1], self.all_objects, self.bombs)
            NetworkObject.NetworkObject(event="bomb_ok").send_to_server(self.client_socket)
        if data.event == 'move':
            self.opponent.rect.x, self.opponent.rect.y = data.coords
        if data.event == 'restart':
            self.restart()

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
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.connect((self.host, self.port))

        NetworkObject.NetworkObject(event="connect").send_to_server(self.client_socket)
        # self.client_socket.send("connect".encode())
        data = pickle.loads(self.client_socket.recv(2048))
        print(data)
        print(data.event, data.symbol, data.game_id)

        self.game_id = data.game_id
        if data.symbol == "#":
            self.opponent_symbol = "$"
            self.character_symbol = "#"
        else:
            self.opponent_symbol = "#"
            self.character_symbol = "$"
            NetworkObject.NetworkObject(event="opponent").send_to_server(self.client_socket)

        self.loop()
    

    def restart(self):
        self.character.rect.x, self.character.rect.y = self.character.start_pos
        self.character.hp = 100


    def check_lose(self):
        if self.character.check_hp():
            self.restart()
            NetworkObject.NetworkObject(event="restart", coords=(self.character.rect.x, self.character.rect.y), hp=self.character.hp, game_id=self.game_id).send_to_server(self.client_socket)
            # self.client_socket.send(f"restart ({str(self.character.rect.x)}, {str(self.character.rect.y)}) {self.character.hp}".encode())


    def close(self):
        pass
    

    def pause(self):
        pass



if __name__ == "__main__":
    g = Game().run() # host="172.105.78.215"