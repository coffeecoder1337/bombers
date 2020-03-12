import block
import bomb
import character
import hud
import images
import loader
import NetworkObject
import pickle
import pygame
import socket
import threading
import time
import menu
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self, host = 'localhost', port = 5005):
        pygame.display.set_caption('Bombers')
        self.rt = None
        self.screen = pygame.display.set_mode((900, 530))
        self.screen_rect = self.screen.get_rect()
        self.all_objects = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bomb_areas = pygame.sprite.Group()
        self.ground_blocks = pygame.sprite.Group()
        self.destructible_blocks = pygame.sprite.Group()
        self.running = True
        self.clock = pygame.time.Clock()
        self.level = None
        self.level_number = 1


        self.bomb_items = {
            K_1: bomb.Bomb,
            K_2: bomb.ShootingBomb
        }

        self.bomb_place_delay = {
            K_1: 5000,
            K_2: 2000
        }

        self.last_place = {
            K_1: 0,
            K_2: 0
        }

        self.current_bomb = K_1

        self.slots = []
        self.items = []
        hud.HudItem(images.laser, self.items)
        hud.HudItem(images.shooting_bomb, self.items)

        self.blocks = {
            "0": block.Ground,
            "1": block.Block,
            "2": block.Block2,
            "3": block.Ground2,
            "4": block.BlueGround2,
            "5": block.BlueGround,
            "6": block.RedGround2,
            "7": block.RedGround,
            "8": block.DestructibleBlock
        }
        self.menu = menu.Menu(self)
        self.timer = 5 * 60
        self.host = host
        self.port = port
        self.data = None


    def empty_groups(self):
        self.all_objects.empty()
        self.platforms.empty()
        self.bombs.empty()
        self.bullets.empty()
        self.bomb_areas.empty()
        self.ground_blocks.empty()
        self.destructible_blocks.empty()

    
    def read_level_file(self, filename):
        with open(filename, "r") as level:
            l = level.readlines()
        level.close()
        for line in range(len(l)):
            l[line] = l[line].strip()
        return l


    def create_level(self, level_number):
        x = 0
        y = 80
        ox, oy = 0, 0
        cx, cy = 0, 0
        self.level = self.read_level_file(f"levels\level{level_number}.txt")
        for row in self.level:
            for col in row:
                if col == self.character_symbol:
                    cx, cy = (x, y)
                elif col == self.opponent_symbol:
                    ox, oy = (x, y)
                else:
                    self.blocks[col](x, y, self.all_objects, platforms=self.platforms, ground_blocks=self.ground_blocks, destructible_blocks=self.destructible_blocks)
                x += 30
            y += 30
            x = 0
        block.Ground(cx, cy, self.all_objects, self.ground_blocks)
        block.Ground(ox, oy, self.all_objects, self.ground_blocks)
        self.character = character.Character(cx, cy, self.all_objects, self.character_image)
        self.opponent = character.Character(ox, oy, self.all_objects, self.opponent_image)
        self.hud = hud.GameHudBar(self.items, self.all_objects, self.slots, self)

    def disconnect(self):
        NetworkObject.NetworkObject(event="left", game_id=self.game_id).send_to_server(self.client_socket)
        self.client_socket.close()
        self.running = False


    def close(self):
        self.empty_groups()
        self.disconnect()
        self.run()
    

    def force_close(self):
        self.disconnect()


    def handler(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.force_close()

            if e.type == KEYDOWN:
                if e.key in (K_LEFT, K_a):
                    self.character.left = 1
                if e.key in (K_RIGHT, K_d):
                    self.character.right = 1
                if e.key in (K_DOWN, K_s):
                    self.character.down = 1
                if e.key in (K_UP, K_w):
                    self.character.up = 1
                
                if e.key in (K_1, K_2):
                    self.current_bomb = e.key

                if e.key in (K_SPACE, K_RETURN):
                    now = pygame.time.get_ticks()
                    if now - self.bomb_place_delay[self.current_bomb] > self.last_place[self.current_bomb]:
                        self.last_place[self.current_bomb] = now
                        bx, by, b = self.character.place_bomb(self.bombs, self.bomb_items[self.current_bomb])
                        NetworkObject.NetworkObject(event="bomb", coords=(bx, by), bomb=self.bomb_items[self.current_bomb], hp=self.character.hp, game_id=self.game_id).send_to_server(self.client_socket)
            
            if e.type == KEYUP:
                if e.key in (K_LEFT, K_a):
                    self.character.left = 0
                if e.key in (K_RIGHT, K_d):
                    self.character.right = 0
                if e.key in (K_DOWN, K_s):
                    self.character.down = 0
                if e.key in (K_UP, K_w):
                    self.character.up = 0

    def loop(self):
        self.create_level(self.level_number)
        self.hud.draw_items()
        if self.character_symbol == "#":
            l = loader.Loader(self.screen_rect.center)
            objcts = pygame.sprite.Group()
            objcts.add(l)
            while self.running:
                self.screen.fill((0, 0, 0))
                objcts.draw(self.screen)
                objcts.update()
                self.handler()
                self.clock.tick(60)
                pygame.display.update()
                if self.data.event == "opponent":
                    break

        # self.last_update = pygame.time.get_ticks()
        self.last_update = time.time()
        while self.running:
            self.handler()
            self.draw()
            if self.timer > 0:
                coords = self.character.move(self.platforms, self.ground_blocks)
                self.rotate_character(self.character, coords)
                if coords != (self.character.rect.x, self.character.rect.y):
                    try:
                        NetworkObject.NetworkObject(event="move", coords=coords, hp=self.character.hp, game_id=self.game_id).send_to_server(self.client_socket)
                    except Exception as e:
                        print(e)
                        print("opponent left the game. exit...")
                        raise SystemExit
                try:
                    self.rotate_character(self.opponent, self.opponent_prev_coords)
                except:
                    pass
                self.check_bombs_to_boom()
                self.check_bomb_areas_to_remove()
                self.check_lose()

                now = time.time()
                if now - self.last_update > 1:
                    x = int(now - self.last_update)
                    self.timer -= x
                    self.last_update = now
            else:
                font = pygame.font.Font('fonts/Crystal.ttf', 72)
                result = ""
                if self.character.score > self.opponent.score:
                    result = "You won!"
                if self.character.score < self.opponent.score:
                    result = "You lose!"
                if self.character.score == self.opponent.score:
                    result = "Tie"
                text = font.render(result, 1, (255, 255, 255))
                self.screen.blit(text, text.get_rect(center=self.screen_rect.center))
            self.clock.tick(75)
            pygame.display.update()


    def parse_data(self, data):
        if data is not None:
            if data.event == 'left':
                self.force_close()

            self.opponent.hp = data.hp
            if data.event == 'bomb':
                data.bomb(data.coords[0], data.coords[1], self.all_objects, self.bombs)
            if data.event == 'move':
                self.opponent_prev_coords = self.opponent.rect.x, self.opponent.rect.y
                self.opponent.rect.x, self.opponent.rect.y = data.coords
            if data.event == 'restart':
                self.restart()
                self.character.score += 1
                NetworkObject.NetworkObject(event="move", coords=(self.character.rect.x, self.character.rect.y), hp=self.character.hp, game_id=self.game_id).send_to_server(self.client_socket)
                self.opponent.rect.x, self.opponent.rect.y = data.coords
            if data.event == 'connect':
                self.game_id = data.game_id


    def check_bombs_to_boom(self):
        for b in self.bombs:
            b.check_to_boom(self.character, self.bomb_areas, self.level, 2000, 3000, self.destructible_blocks, self.bullets, self.platforms, self.opponent)


    def rotate_character(self, character, prev_coords):
        if character.rect.x > prev_coords[0]:
            character.image = pygame.transform.rotate(character.original_image, 90)
        if character.rect.x < prev_coords[0]:
            character.image = pygame.transform.rotate(character.original_image, -90)
        if character.rect.y > prev_coords[1]:
            character.image = pygame.transform.rotate(character.original_image, 0)
        if character.rect.y < prev_coords[1]:
            character.image = pygame.transform.rotate(character.original_image, 180)
        character.rect = character.image.get_rect(center=character.rect.center)


    def check_bomb_areas_to_remove(self):
        for ba in self.bomb_areas:
            if pygame.time.get_ticks() - ba.spawntime > 500:
                self.all_objects.remove(ba)
                self.bomb_areas.remove(ba)
            else:
                ba.check_collide(self.character)


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_objects.update()
        self.all_objects.draw(self.screen)

    
    def run(self):
        self.menu.show()

        if self.running:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client_socket.connect((self.host, self.port))

            NetworkObject.NetworkObject(event="connect").send_to_server(self.client_socket)
            while True:
                if self.data is not None:
                    break

            self.game_id = self.data.game_id
            if self.data.symbol == "#":
                self.opponent_symbol = "$"
                self.opponent_image = images.character_red
                self.character_image = images.character_blue
                self.character_symbol = "#"
            else:
                self.opponent_symbol = "#"
                self.character_symbol = "$"
                self.opponent_image = images.character_blue
                self.character_image = images.character_red
                NetworkObject.NetworkObject(event="opponent", game_id=self.game_id).send_to_server(self.client_socket)
            
            self.loop()
    

    def restart(self):
        self.character.rect.x, self.character.rect.y = self.character.start_pos
        self.all_objects.remove(self.bombs, self.bullets, self.bomb_areas)
        self.bombs.empty()
        self.bullets.empty()
        self.bomb_areas.empty()
        self.character.hp = 100


    def check_lose(self):
        if self.character.check_hp():
            self.restart()
            self.opponent.score += 1
            NetworkObject.NetworkObject(event="restart", coords=(self.character.rect.x, self.character.rect.y), hp=self.character.hp, game_id=self.game_id).send_to_server(self.client_socket)


    def pause(self):
        pass


def receiving (game, name):
    while game.running:
        try:
            while True:
                data = pickle.loads(game.client_socket.recv(2048))
                game.data = data
                game.parse_data(data)
        except:
            pass


if __name__ == "__main__":
    g = Game() # host="172.105.78.215"
    rT = threading.Thread(target = receiving, args = (g, "RecvThread"))
    rT.start()
    g.run()
    rT.join()
