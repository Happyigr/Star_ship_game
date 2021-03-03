# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# <http://creativecommons.org/licenses/by/3.0/>
# Art by Kenny, fakigame
import pygame
import random
from os import path

# Цвета
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
INVISIBLE_COLOR = (120, 120, 120)

HEIGHT = 600
WIDTH = 450
FPS = 60

# Создание игры и окна
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The best game ever')
clock = pygame.time.Clock()

# Путь к папке с картинками
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Загрузка игровой графики
meteor_list = ["meteorGrey_big4.png", "meteorGrey_med1.png", "meteorGrey_med2.png",
               "meteorGrey_small1.png", "meteorGrey_small2.png", "meteorGrey_tiny1.png",
               "meteorGrey_tiny2.png"]
meteor_images = []
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
background = pygame.image.load(path.join(img_dir, "star_background.png")).convert()
background_mini = pygame.transform.scale(background, (450, 600))
background_mini_rect = background_mini.get_rect()
ship_imgs = []
ship_1_img = pygame.image.load(path.join(img_dir, "playerShip3_green.png")).convert()
ship_1_mini_img = pygame.transform.scale(ship_1_img, (50, 30))
ship_2_img = pygame.image.load(path.join(img_dir, "playerShip3_blue.png")).convert()
ship_2_mini_img = pygame.transform.scale(ship_2_img, (50, 30))
ship_3_img = pygame.image.load(path.join(img_dir, "playerShip3_orange.png")).convert()
ship_3_mini_img = pygame.transform.scale(ship_3_img, (50, 30))
ship_4_img = pygame.image.load(path.join(img_dir, "playerShip3_red.png")).convert()
ship_4_mini_img = pygame.transform.scale(ship_4_img, (50, 30))
ship_imgs.append(ship_1_mini_img)
ship_imgs.append(ship_2_mini_img)
ship_imgs.append(ship_3_mini_img)
ship_imgs.append(ship_4_mini_img)
player_img_lives = pygame.image.load(path.join(img_dir, 'playerShip1_red.png')).convert()
player_mini_img_lives = pygame.transform.scale(player_img_lives, (25, 19))
player_mini_img_lives.set_colorkey(BLACK)
laser_img = pygame.image.load(path.join(img_dir, "laserRed05.png")).convert()
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
invis_img = pygame.image.load(path.join(img_dir, 'white_cube.jpg'))
invis_img_mini = pygame.transform.scale(invis_img, (50, 50))
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

# Загрузка графики для меню
arrow_right_img = pygame.image.load(path.join(img_dir, 'arrow_right.png')).convert()
arrow_left_img = pygame.image.load(path.join(img_dir, "arrow_left.png")).convert()
buy_button_green = pygame.image.load(path.join(img_dir, 'buy_button_green.png')).convert()
buy_button_red = pygame.image.load(path.join(img_dir, 'buy_button_red.png')).convert()
buy_button_green_mini_img = pygame.transform.scale(buy_button_green, (50, 50))
buy_button_red_mini_img = pygame.transform.scale(buy_button_red, (50, 50))
chose_button_red_img = pygame.image.load(path.join(img_dir, 'chose_button_red.png'))
chose_button_green_img = pygame.image.load(path.join(img_dir, 'chose_button_green.png'))
chose_button_red_mini_img = pygame.transform.scale(chose_button_red_img, (50, 50))
chose_button_green_mini_img = pygame.transform.scale(chose_button_green_img, (50, 50))

# Загрузка звуков
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
expl_sounds = []
for exp in ['Explosion.wav', 'Explosion3.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, exp)))
expl_sound_kill = pygame.mixer.Sound(path.join(snd_dir, 'Explosion12.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'Hit_Hurt9.wav'))
player_death_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'powerup_shield.wav'))
gun_sound = pygame.mixer.Sound(path.join(snd_dir, 'powerup_gun.wav'))

