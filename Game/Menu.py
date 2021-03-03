import pygame
from Button import *
from Images import *
from Variables import *


# Вывод текста
font_name = pygame.font.match_font('arial')


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


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


def draw_waiting_buttons():
    for button in waiting_buttons:
        button.draw(screen)


def draw_upgrade_buttons():
    for button in upgrade_buttons:
        button.draw(screen)


def check_button(button_name):
    if button_name in upgrade_buttons:
        return True


def button_remove(button_name):
    if check_button(button_name):
        upgrade_buttons.remove(button_name)


def buy_button_chose(ship_number, all_money):
    if upgrade_ships[ship_number].owned and upgrade_ships[ship_number].chosen:
        print('1')
        upgrade_buttons.append(chose_button_green)
        button_remove(chose_button_red)
        button_remove(buy_button_red)
        button_remove(buy_button_green)
    if upgrade_ships[ship_number].owned and not upgrade_ships[ship_number].chosen:
        print('2')
        upgrade_buttons.append(chose_button_red)
        button_remove(chose_button_green)
        button_remove(buy_button_red)
        button_remove(buy_button_green)
    if not upgrade_ships[ship_number].owned and not upgrade_ships[ship_number].chosen and\
            all_money >= upgrade_ships[ship_number].cost:
        print('3')
        upgrade_buttons.append(buy_button_green)
        button_remove(buy_button_red)
        button_remove(chose_button_red)
        button_remove(chose_button_green)
    if not upgrade_ships[ship_number].owned and not upgrade_ships[ship_number].chosen and\
            all_money < upgrade_ships[ship_number].cost:
        print('4')
        upgrade_buttons.append(buy_button_red)
        button_remove(buy_button_green)
        button_remove(chose_button_red)
        button_remove(chose_button_green)


def show_upgrade_screen(all_money):
    upgrade = True
    ship_number = 0
    upgrade_sprites.add(ship_1)
    buy_button_chose(ship_number, all_money)
    while upgrade:
        screen.blit(background_mini, background_mini_rect)
        draw_text(screen, 'Улучшения', 64, WIDTH / 2, 100)
        draw_text(screen, 'Урон', 15, 100, 400)
        draw_text(screen, 'Скоростерльность', 15, 100, 430)
        draw_text(screen, 'Щит', 15, 100, 460)
        draw_text(screen, 'Жизней', 15, 100, 490)
        draw_text(screen, ('Денег: ' + str(all_money)), 15, WIDTH / 2, 50)
        draw_upgrade_buttons()
        upgrade_sprites.draw(screen)
        upgrade_ships[ship_number].draw_characteristics()
        pos = pygame.mouse.get_pos()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.isOver(pos):
                upgrade = False
                return all_money
            if event.type == pygame.MOUSEBUTTONDOWN and left_arrow.isOver(pos):
                upgrade_sprites.remove(upgrade_ships[ship_number])
                if ship_number == 0:
                    ship_number = len(upgrade_ships) - 1
                else:
                    ship_number -= 1
                upgrade_sprites.add(upgrade_ships[ship_number])
                buy_button_chose(ship_number, all_money)
            if event.type == pygame.MOUSEBUTTONDOWN and right_arrow.isOver(pos):
                upgrade_sprites.remove(upgrade_ships[ship_number])
                if ship_number == len(upgrade_ships) - 1:
                    ship_number = 0
                else:
                    ship_number += 1
                upgrade_sprites.add(upgrade_ships[ship_number])
                buy_button_chose(ship_number, all_money)
            if event.type == pygame.MOUSEBUTTONDOWN and buy_button_red.isOver(pos) and \
                    check_button(buy_button_red):
                print('Не хватает денег :(')
            elif event.type == pygame.MOUSEBUTTONDOWN and buy_button_green.isOver(pos) and \
                    check_button(buy_button_green):
                all_money -= upgrade_ships[ship_number].cost
                upgrade_ships[ship_number].owned = True
                buy_button_chose(ship_number, all_money)
                print('a')
            elif event.type == pygame.MOUSEBUTTONDOWN and chose_button_red.isOver(pos) and \
                    check_button(chose_button_red):
                for i in range(len(upgrade_ships)):
                    upgrade_ships[i].chosen = False
                upgrade_ships[ship_number].chosen = True
                buy_button_chose(ship_number, all_money)
                print('red')
            elif event.type == pygame.MOUSEBUTTONDOWN and chose_button_green.isOver(pos) and \
                    check_button(chose_button_green):
                upgrade_ships[ship_number].chosen = False
                buy_button_chose(ship_number, all_money)
                print('gr')
            if event.type == pygame.MOUSEMOTION:
                for button in upgrade_buttons:
                    if button.isOver(pos):
                        button.color = (INVISIBLE_COLOR)
                    else:
                        button.color = (WHITE)
        pygame.display.update()


def show_go_screen(money = all_money):
    screen.blit(background_mini, background_mini_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, 100)
    draw_text(screen, (str(money) + ' $'), 15, WIDTH / 2, 20)
    pygame.display.flip()
    menu = True
    waiting = True
    upgrade_screen = False
    info_screen = False
    while waiting:
        draw_waiting_buttons()
        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and exit_button.isOver(pos):
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and play_button.isOver(pos):
                waiting = False
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN and upgrade_button.isOver(pos):
                upgrade_screen = True
            if event.type == pygame.MOUSEBUTTONDOWN and info_button.isOver(pos):
                info_screen = True
            if event.type == pygame.MOUSEMOTION:
                for button in waiting_buttons:
                    if button.isOver(pos):
                        button.color = (INVISIBLE_COLOR)
                    else:
                        button.color = (WHITE)
            while upgrade_screen:
                all_money = show_upgrade_screen(money)
                upgrade_screen = False
                waiting = False
            while info_screen:
                pass
                info_screen = False
    return menu


class Upgrade_Ship(pygame.sprite.Sprite):

    def __init__(self, image, color, x, y, damage, shoot_delay, shield, lives, cost):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.damage = damage
        self.shoot_delay = shoot_delay
        self.shield = shield
        self.lives = lives
        self.cost = cost
        self.owned = False
        self.chosen = False

    def draw_characteristics(self):
        draw_text(screen, str(self.damage), 15, WIDTH / 2, 400)
        draw_text(screen, str(self.shoot_delay), 15, WIDTH / 2, 430)
        draw_text(screen, str(self.shield), 15, WIDTH / 2, 460)
        draw_lives(screen, 180, 490, self.lives, player_mini_img_lives)
        draw_text(screen, (str(self.cost) + ' $'), 15, 420, 575)


upgrade_sprites = pygame.sprite.Group()
# Спрайты
upgrade_ships = []
ship_1 = Upgrade_Ship(ship_1_mini_img, WHITE, WIDTH / 2, HEIGHT / 2, 1, 250, 100, 3, 1000)
ship_2 = Upgrade_Ship(ship_2_mini_img, BLUE, WIDTH / 2, HEIGHT / 2, 3, 200, 150, 3, 4000)
ship_3 = Upgrade_Ship(ship_3_mini_img, GREEN, WIDTH / 2, HEIGHT / 2, 2, 100, 200, 2, 10000)
ship_4 = Upgrade_Ship(ship_4_mini_img, YELLOW, WIDTH / 2, HEIGHT / 2, 5, 300, 300, 4, 20000)
upgrade_ships.append(ship_1)
upgrade_ships.append(ship_2)
upgrade_ships.append(ship_3)
upgrade_ships.append(ship_4)

# Кнопки
waiting_buttons = []
play_button = Button(WHITE, 100, 300, 250, 35, 'Играть', 30)
upgrade_button = Button(WHITE, 100, 350, 250, 35, 'Улучшения', 30)
info_button = Button(WHITE, 100, 400, 250, 35, 'Доп. информация', 30)
exit_button = Button(WHITE, 100, 450, 250, 35, 'Выход', 30)
waiting_buttons.append(play_button)
waiting_buttons.append(upgrade_button)
waiting_buttons.append(exit_button)
waiting_buttons.append(info_button)
upgrade_buttons = []
back_button = Button(WHITE, 100, 550, 250, 35, 'Назад', 30)
buy_button_green = Button_img(buy_button_green_mini_img, 395, 510)
buy_button_red = Button_img(buy_button_red_mini_img, 395, 510)
chose_button_green = Button_img(chose_button_green_mini_img, 395, 510)
chose_button_red = Button_img(chose_button_red_mini_img, 395, 510)
left_arrow = Button_img(arrow_left_img, 50, 300)
right_arrow = Button_img(arrow_right_img, 372, 300)
upgrade_buttons.append(back_button)
upgrade_buttons.append(right_arrow)
upgrade_buttons.append(left_arrow)
