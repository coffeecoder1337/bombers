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

try:
    loader = [
        pygame.image.load('images/loader/1.png'),
        pygame.image.load('images/loader/2.png'),
        pygame.image.load('images/loader/3.png'),
        pygame.image.load('images/loader/4.png'),
        pygame.image.load('images/loader/5.png'),
        pygame.image.load('images/loader/6.png'),
        pygame.image.load('images/loader/7.png'),
    ]
except:
    loader = None

try:
    shooting_bomb = pygame.image.load('images/bombs/bomb2.png')
except:
    shooting_bomb = None

try:
    bullet = pygame.image.load('images/bombs/bullet.png')
except:
    bullet = None

try:
    item_holder1 = pygame.image.load('images/hud/item_holder1.png')
except:
    item_holder1 = None

try:
    item_holder2 = pygame.image.load('images/hud/item_holder2.png')
except:
    item_holder2 = None

try:
    background = [
        pygame.image.load('images/menu/background/0.gif'),
        pygame.image.load('images/menu/background/1.gif'),
        pygame.image.load('images/menu/background/2.gif'),
        pygame.image.load('images/menu/background/3.gif'),
        pygame.image.load('images/menu/background/4.gif'),
        pygame.image.load('images/menu/background/5.gif'),
        pygame.image.load('images/menu/background/6.gif'),
        pygame.image.load('images/menu/background/7.gif'),
        pygame.image.load('images/menu/background/8.gif'),
        pygame.image.load('images/menu/background/9.gif'),
        pygame.image.load('images/menu/background/10.gif'),
        pygame.image.load('images/menu/background/11.gif'),
        pygame.image.load('images/menu/background/12.gif'),
        pygame.image.load('images/menu/background/13.gif'),
        pygame.image.load('images/menu/background/14.gif'),
        pygame.image.load('images/menu/background/15.gif'),
        pygame.image.load('images/menu/background/16.gif'),
        pygame.image.load('images/menu/background/17.gif'),
        pygame.image.load('images/menu/background/18.gif'),
        pygame.image.load('images/menu/background/19.gif'),
        pygame.image.load('images/menu/background/20.gif'),
        pygame.image.load('images/menu/background/21.gif'),
        pygame.image.load('images/menu/background/22.gif'),
        pygame.image.load('images/menu/background/23.gif'),
        pygame.image.load('images/menu/background/24.gif'),
        pygame.image.load('images/menu/background/25.gif'),
        pygame.image.load('images/menu/background/26.gif'),
        pygame.image.load('images/menu/background/27.gif'),
        pygame.image.load('images/menu/background/28.gif'),
        pygame.image.load('images/menu/background/29.gif'),
        pygame.image.load('images/menu/background/30.gif'),
        pygame.image.load('images/menu/background/31.gif'),
        pygame.image.load('images/menu/background/32.gif'),
        pygame.image.load('images/menu/background/33.gif'),
        pygame.image.load('images/menu/background/34.gif'),
        pygame.image.load('images/menu/background/35.gif'),
        pygame.image.load('images/menu/background/36.gif'),
        pygame.image.load('images/menu/background/37.gif'),
        pygame.image.load('images/menu/background/38.gif'),
        pygame.image.load('images/menu/background/39.gif'),
    ]
except:
    background = None

try:
    play_btn = [
        pygame.image.load('images/menu/buttons/play1.png'),
        pygame.image.load('images/menu/buttons/play2.png'),
    ]
except:
    play_btn = None

try:
    help_btn = [
        pygame.image.load('images/menu/buttons/help1.png'),
        pygame.image.load('images/menu/buttons/help2.png'),
    ]
except:
    help_btn = None

try:
    quit_btn = [
        pygame.image.load('images/menu/buttons/quit1.png'),
        pygame.image.load('images/menu/buttons/quit2.png'),
    ]
except:
    quit_btn = None

try:
    help_page = pygame.image.load('images/menu/help_page/help.png')
except:
    help_page = None

try:
    spawn_blue = pygame.image.load('images/blocks/spawn_blue.png')
except:
    spawn_blue = None

try:
    spawn_red = pygame.image.load('images/blocks/spawn_red.png')
except:
    spawn_red = None