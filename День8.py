import threading

import pygame
import random
import os

width = 1920
height = 1030
fps = 60
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 120, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'pic_player.png'))
jump_img = pygame.image.load(os.path.join(img_folder, 'pic_jump.png'))
attack_img = pygame.image.load(os.path.join(img_folder, 'pic_attack.png'))
weapon_img = pygame.image.load(os.path.join(img_folder, 'pic_weapon.png'))
enemy_green = pygame.image.load(os.path.join(img_folder, 'pic_enemy_green.png'))
enemy_orange = pygame.image.load(os.path.join(img_folder, 'pic_enemy_orange.png'))
enemy_red = pygame.image.load(os.path.join(img_folder, 'pic_enemy_red.png'))
background_img = pygame.image.load(os.path.join(img_folder, 'background.png'))
background_rect = background_img.get_rect()

enemy_list = (enemy_red, enemy_orange, enemy_green)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height)
        self.speedx = 0
        self.speedy = 0
        self.isJump = False
        self.jumpCount = 10
        self.isAttack = False
        self.attackCount = 5

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.isJump = True
            self.image = jump_img
            self.image.set_colorkey((255, 255, 255))
        if self.isJump is True:

            if self.jumpCount >= -10:

                if self.jumpCount < 0:
                    self.rect.y += (self.jumpCount ** 2) // 2
                else:
                    self.rect.y -= (self.jumpCount ** 2) // 2

                self.jumpCount -= 1

            else:
                self.isJump = False
                self.jumpCount = 10
                self.image = player_img
                self.image.set_colorkey((255, 255, 255))
        if keystate[pygame.K_f]:
            self.isAttack = True
            self.image = attack_img
            self.image.set_colorkey((255, 255, 255))
        if self.isAttack is True:

            if self.attackCount >= 0:
                self.attackCount -= 1

            else:
                self.isAttack = False
                self.attackCount = 10
                self.image = player_img
                self.image.set_colorkey((255, 255, 255))
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(enemy_list)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (width - 200, height)
        self.direction = -1
        self.last_direction_change = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_direction_change > random.randrange(500, 2800):
            self.direction *= -1
            self.last_direction_change = current_time
        self.rect.x += 2.5 * self.direction
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = weapon_img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.right > width:
            self.kill()


all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
enemy = Enemy()
all_sprites.add(player)
enemies.add(enemy)
all_sprites.add(enemy)
score = 0

def DeathScreen():
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.death_text = self.font.render('Вы умерли. Нажмите R чтобы начать заново!', True, (255, 0, 0))
        self.death_text = self.death_text.get_rect(center=(400,300))
    def display(self, screen):
        screen.blit(self.death_text, self.death_rect)

deeath_screen = DeathScreen()

def show_go_screen():
    screen.blit(background_img, background_rect)
    draw_text(screen, "Токийский мститель", 70, width / 2, height / 4)
    draw_text(screen, "W,A,S,D - Движение, F - Стрельба", 30,
              width / 2, height / 2)
    draw_text(screen, "Нажмите кнопку, чтобы начатьа", 18, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
game_over = True
running = True
while running:
    clock.tick(fps)
    all_sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                player.shoot()
    all_sprites.update()

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 50
        n = Enemy()
        all_sprites.add(n)
        enemies.add(n)

    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False
    screen.fill(green)
    screen.blit(background_img, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 36, width / 2, 10)
    if score == 5000:
        running = False
    pygame.display.flip()

    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0

pygame.quit()
