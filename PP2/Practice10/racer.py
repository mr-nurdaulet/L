

import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

FPS           = 60
SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
SPEED         = 5
SCORE         = 0
COINS         = 0

BLUE    = (0, 0, 255)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
YELLOW  = (255, 215, 0)    # coin colour


font       = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over  = font.render("Game Over", True, BLACK)


DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer")


FramePerSec = pygame.time.Clock()


background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill((80, 80, 80))
for lane_x in [130, 200, 270]:
    for dash_y in range(0, SCREEN_HEIGHT, 60):
        pygame.draw.rect(background, WHITE, (lane_x - 2, dash_y, 4, 30))

bg_y = 0



class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((42, 70))
        self.image.fill(RED)
        pygame.draw.rect(self.image, (200, 200, 255), (5, 5, 32, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), 0)

    def move(self):
        global SCORE, SPEED
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            if SCORE % 5 == 0:
                SPEED += 1
            self.rect.top = 0
            self.rect.centerx = random.randint(50, SCREEN_WIDTH - 50)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((42, 70))
        self.image.fill(BLUE)
        pygame.draw.rect(self.image, (200, 200, 255), (5, 45, 32, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)  #

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 10:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH - 10:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):


    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (12, 12), 12)
        pygame.draw.circle(self.image, (200, 160, 0), (12, 12), 12, 2)  # border
        label = font_small.render("$", True, BLACK)
        self.image.blit(label, (5, 2))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), 0)

    def move(self):
        self.rect.move_ip(0, max(2, SPEED - 1))
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


P1      = Player()
E1      = Enemy()
C1      = Coin()

enemies = pygame.sprite.Group()
coins   = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

enemies.add(E1)
coins.add(C1)
all_sprites.add(P1, E1, C1)

SPAWN_COIN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_COIN, 3000)

INC_SPEED = pygame.USEREVENT + 2
pygame.time.set_timer(INC_SPEED, 1000)

def draw_hud():
    score_surf = font_small.render(f"Score: {SCORE}", True, WHITE)
    DISPLAYSURF.blit(score_surf, (10, 10))
    coin_surf  = font_small.render(f"Coins: {COINS} 🪙", True, YELLOW)
    coin_rect  = coin_surf.get_rect()
    coin_rect.topright = (SCREEN_WIDTH - 10, 10)
    DISPLAYSURF.blit(coin_surf, coin_rect)


def game_loop():
    global SCORE, COINS, SPEED, bg_y

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SPAWN_COIN:
                new_coin = Coin()
                coins.add(new_coin)
                all_sprites.add(new_coin)

        bg_y = (bg_y + SPEED // 2 + 1) % SCREEN_HEIGHT
        DISPLAYSURF.blit(background, (0, bg_y - SCREEN_HEIGHT))
        DISPLAYSURF.blit(background, (0, bg_y))

        P1.move()
        for enemy in enemies:
            enemy.move()
        for coin in coins:
            coin.move()

        if pygame.sprite.spritecollideany(P1, enemies):
            DISPLAYSURF.blit(game_over,
                             (SCREEN_WIDTH // 2 - game_over.get_width() // 2,
                              SCREEN_HEIGHT // 2 - game_over.get_height() // 2))
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()

        collected = pygame.sprite.spritecollide(P1, coins, True)
        COINS += len(collected)

        for sprite in all_sprites:
            DISPLAYSURF.blit(sprite.image, sprite.rect)

        draw_hud()

        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    game_loop()
