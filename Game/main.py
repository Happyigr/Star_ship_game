import pygame
import random
from Button import *
from Menu import show_go_screen, upgrade_ships
from Images import *
from Variables import *

HEIGHT = 600
WIDTH = 450
FPS = 60

# Создание игры и окна
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The best game ever')
clock = pygame.time.Clock()

# Вывод текста
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def show_menu(all_money):
    menu = True
    while menu:
        menu = show_go_screen(all_money)


def chosen_ship():
    for ship in upgrade_ships:
        if ship.chosen:
            return ship
            break


def chosen_ship_number():
    n = 0
    for ship in upgrade_ships:
        if ship.chosen:
            break
        n += 1
    if n > (len(upgrade_ships) - 1):
        return 0
    else:
        return n


def for_ship_img_chose(n):
    return ship_imgs[n]


def ship_to_fight_chose():
    n = 0
    for ship in upgrade_ships:
        if ship.chosen:
            player = Player(for_ship_img_chose(n), upgrade_ships[n].damage,
                            upgrade_ships[n].shoot_delay, upgrade_ships[n].shield,
                            upgrade_ships[n].lives)
        else:
            player = Player(for_ship_img_chose(0), upgrade_ships[0].damage,
                            upgrade_ships[0].shoot_delay, upgrade_ships[0].shield,
                            upgrade_ships[0].lives)
        n += 1
    return player


# Игрок
class Player(pygame.sprite.Sprite):

    def __init__(self, image, damage, shoot_delay, shield, lives):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 15
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.poweruptime = 5000  # 5 sec
        # Характеристики
        self.shield_max = shield
        self.shield = shield
        self.damage = damage
        self.shoot_delay = shoot_delay
        self.last_shoot = pygame.time.get_ticks()
        self.lives = lives

    def update(self):
        POWERUP_TIME = 5000
        # Показать если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.image = for_ship_img_chose(chosen_ship_number())
            self.image.set_colorkey(BLACK)
            for i in range(8):
                newmob()
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        self.speedx = 0
        self.speedy = 0
        # Полет влево вправо
        keystate = pygame.key.get_pressed()
        left = keystate[pygame.K_LEFT]
        right = keystate[pygame.K_RIGHT]
        up = keystate[pygame.K_UP]
        down = keystate[pygame.K_DOWN]
        if not self.hidden:
            if left:
                self.speedx = -8
            if right:
                self.speedx = 8
            if up:
                self.speedy = -8
            if down:
                self.speedy = 8
            if keystate[pygame.K_e]:
                self.shoot()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # Ограничение движения экраном
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def hide(self):
        # Временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.image = invis_img_mini
        self.image.set_colorkey(WHITE)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            if self.power == 1:
                self.last_shoot = now
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                self.last_shoot = now
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()


# Баффы
class Buff(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # Убить пулю после выхода за пределы экрана
        if self.rect.top > HEIGHT:
            self.kill()


# Пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Убить пулю после выхода за пределы экрана
        if self.rect.bottom < 0:
            self.kill()


# Мобы
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #   pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.image = pygame.transform.rotate(self.image, self.rot_speed)
        self.health = int(self.radius / 3)

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + self.radius * 2 or self.rect.left < -self.radius * 2 or \
                self.rect.right > WIDTH + self.radius * 2:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            # Вращение спрайтов
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


# Взрывы
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Спрайты
player = ship_to_fight_chose()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
powerup = pygame.sprite.Group()
mobs = pygame.sprite.Group()
for i in range(8):
    newmob()
score = 0
pygame.mixer.music.play(loops=-1)

# Цикл игры
game_over = True
running = True
play = False
while running:
    if game_over:
        show_menu(all_money)
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerup = pygame.sprite.Group()
        player = ship_to_fight_chose()
        all_sprites.add(player)
        for i in range(8):
            newmob()
    # Поддерживаем правильную частоту кадров
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # Проверка закрыл ли игрок игру
        if event.type == pygame.QUIT:
            quit()

    # Обновление
    all_sprites.update()
    money = score

    # Проверка не убила ли пуля моба
    hits = pygame.sprite.groupcollide(mobs, bullets, False, True, pygame.sprite.collide_circle)
    for hit in hits:
        if hit.health - player.damage <= 0:
            hit.kill()
            score += 50 - hit.radius
            expl_sound_kill.play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                buff = Buff(hit.rect.center)
                all_sprites.add(buff)
                powerup.add(buff)
            newmob()
        else:
            hit.health -= player.damage
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            random.choice(expl_sounds).play()

    # Проверка столкновения игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerup, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= player.shield_max:
                player.shield = player.shield_max
            shield_sound.play()
        if hit.type == 'gun':
            player.powerup()
            gun_sound.play()

    # Проверка не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        hit_sound.play()
        if player.shield <= 0:
            for i in mobs.sprites():
                i.kill()
            mobs.empty()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player_death_sound.play()
            player.hide()
            player.lives -= 1
            player.shield = player.shield_max

    # Если игрок умер, игра окончена
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background_mini, background_mini_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(str(score) + ' $'), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img_lives)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()













