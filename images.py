import pygame

try:
    block = pygame.image.load('images/blocks/block.png')
except:
    block = None

try:
    block_2 = pygame.image.load('images/blocks/wall_2.png')
except:
    block_2 = None

try:
    laser = pygame.image.load('images/bombs/bomb_laser.png')
except:
    laser = None

try:
    laser_area = pygame.image.load('images/bombs/bomb_laser_shoot.png')
except:
    laser_area = None

try:
    ground_2 = pygame.image.load('images/blocks/ground_1grey.png')
except:
    ground_2 = None

try:
    ground = pygame.image.load('images/blocks/ground.png')
except:
    ground = None

try:
    blue_ground_2 = pygame.image.load('images/blocks/ground_2.png')
except:
    blue_ground_2 = None

try:
    blue_ground = pygame.image.load('images/blocks/ground_1.png')
except:
    blue_ground = None

try:
    red_ground_2 = pygame.image.load('images/blocks/ground_2red.png')
except:
    red_ground_2 = None

try:
    red_ground = pygame.image.load('images/blocks/ground_1red.png')
except:
    red_ground = None

try:
    bomb = pygame.image.load('images/blocks/bomb.png')
except:
    bomb = None

try:
    bomb_area = pygame.image.load('images/blocks/bomb_area.png')
except:
    bomb_area = None

try:
    character_red = pygame.image.load('images/character/character_red.png')
except:
    character_red = None

try:
    character_blue = pygame.image.load('images/character/character_blue.png')
except:
    character_blue = None

try:
    destructible_block = [
        pygame.image.load('images/blocks/1.png'),
        pygame.image.load('images/blocks/2.png'),
        pygame.image.load('images/blocks/3.png'),
        pygame.image.load('images/blocks/4.png'),
        pygame.image.load('images/blocks/5.png'),
        pygame.image.load('images/blocks/6.png'),
    ]
except:
    destructible_block = None
