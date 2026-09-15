import pygame
import random


def get_lane_x(lane):
    return 80 + lane * 90 + 45


pygame.init()
screen = pygame.display.set_mode((380, 600))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

COIN_TYPES = [
    {"value": 1, "color": (180, 180, 180), "prob": 60},
    {"value": 5, "color": (255, 215, 0), "prob": 25},
    {"value": 10, "color": (255, 140, 0), "prob": 10},
    {"value": 50, "color": (200, 80, 255), "prob": 5},
]


def pick_coin_value():
    pool = []
    for ct in COIN_TYPES:
        pool += [ct] * ct["prob"]
    return random.choice(pool)


player_lane = 1
player_x = float(get_lane_x(1))
player_y = 500

enemies = []
coins = []

enemy_timer = 0
coin_timer = 0
stripe_y = 0
score = 0
total_coins = 0
speed = 5.0
speed_mult = 1
key_cd = 0
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_lane > 0 and key_cd <= 0:
                player_lane -= 1
                key_cd = 12
            if event.key == pygame.K_RIGHT and player_lane < 2 and key_cd <= 0:
                player_lane += 1
                key_cd = 12

    key_cd -= 1
    player_x += (get_lane_x(player_lane) - player_x) * 0.2

    stripe_y = (stripe_y + speed) % 40

    enemy_timer += 1
    if enemy_timer >= 70:
        lane = random.randint(0, 2)
        enemies.append({"x": float(get_lane_x(lane)), "y": -40.0})
        enemy_timer = 0

    coin_timer += 1
    if coin_timer >= 55:
        lane = random.randint(0, 2)
        ct = pick_coin_value()
        coins.append({"x": float(get_lane_x(lane)), "y": -20.0,
                      "value": ct["value"], "color": ct["color"]})
        coin_timer = 0

    for e in enemies[:]:
        e["y"] += speed
        if abs(e["x"] - player_x) < 30 and abs(e["y"] - player_y) < 45:
            pygame.quit()
        if e["y"] > 650:
            enemies.remove(e)
            score += 1

    for c in coins[:]:
        c["y"] += speed
        if abs(c["x"] - player_x) < 20 and abs(c["y"] - player_y) < 20:
            total_coins += c["value"]
            coins.remove(c)
            new_mult = 1 + total_coins // 20
            if new_mult > speed_mult:
                speed_mult = new_mult
                speed = 5.0 + (speed_mult - 1) * 1.0
        elif c["y"] > 650:
            coins.remove(c)

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (60, 60, 70), (80, 0, 270, 600))

    for lane in range(1, 3):
        lx = 80 + lane * 90
        y = -40 + stripe_y
        while y < 600:
            pygame.draw.rect(screen, (220, 220, 180), (lx - 2, int(y), 4, 22))
            y += 40

    pygame.draw.rect(screen, (200, 200, 140), (78, 0, 5, 600))
    pygame.draw.rect(screen, (200, 200, 140), (347, 0, 5, 600))

    for e in enemies:
        pygame.draw.rect(screen, (220, 60, 60),
                         (int(e["x"]) - 18, int(e["y"]) - 28, 36, 56))

    for c in coins:
        pygame.draw.circle(screen, c["color"], (int(c["x"]), int(c["y"])), 11)
        pygame.draw.circle(screen, (0, 0, 0), (int(c["x"]), int(c["y"])), 11, 2)
        lbl = font.render(str(c["value"]), True, (0, 0, 0))
        screen.blit(lbl, lbl.get_rect(center=(int(c["x"]), int(c["y"]))))

    pygame.draw.rect(screen, (70, 140, 255),
                     (int(player_x) - 18, player_y - 28, 36, 56))

    hud = font.render(f"Score: {score}  Coins: {total_coins}  x{speed_mult}", True, (255, 255, 255))
    screen.blit(hud, (10, 10))

    pygame.display.flip()

pygame.quit()
