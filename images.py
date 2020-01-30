import pygame

try:
    block = pygame.image.load('images/blocks/block.png')
except:
    block = None

try:
    laser = pygame.image.load('images/bombs/bomb_laser.png')
except:
    laser = None

try:
    laser_area = pygame.image.load('images/bombs/bomb_laser_shoot.png')
except:
    laser_area = None

try:
    ground = pygame.image.load('images/blocks/ground.png')
except:
    ground = None

try:
    bomb = pygame.image.load('images/blocks/bomb.png')
except:
    bomb = None

try:
    bomb_area = pygame.image.load('images/blocks/bomb_area.png')
except:
    bomb_area = None

try:
    character = pygame.image.load('images/character/character.png')
except:
    character = None

