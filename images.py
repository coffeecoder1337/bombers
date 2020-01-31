import pygame

try:
    block = pygame.image.load('images/blocks/block.png')
except:
    block = None

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
