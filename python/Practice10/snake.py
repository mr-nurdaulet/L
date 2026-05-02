import random
import pygame

def random_cords(a):
    while True:
        n = random.randint(1, 23)
        m = random.randint(1, 23)
        if [n, m] not in a:
            return [n, m]

def shift_massive(a):
    for i in range(len(a)):
        if i != 0:
            a[i-1] = a[i].copy()
    return a

pygame.init()
weight, height = 500, 550
screen = pygame.display.set_mode((weight, height))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont(None, 30)

dir = [1, 0]
snake = [[1, 10], [2, 10], [3, 10]]
apple = random_cords(snake)
clock = pygame.time.Clock()
board = [(x, y) for x in range(1, 24) for y in range(1, 24)]
score = 0
s = 0
running = True
a1, s1, d1, w1 = False, False, False, False

foods = []
FOOD_TYPES = [
    {"value": 1,  "color": (255, 0,   0  ), "lifetime": None, "prob": 50},
    {"value": 3,  "color": (255, 215, 0  ), "lifetime": 8000, "prob": 25},
    {"value": 5,  "color": (255, 140, 0  ), "lifetime": 5000, "prob": 15},
    {"value": 10, "color": (180, 0,   255), "lifetime": 3000, "prob": 10},
]

def pick_food_type():
    pool = []
    for ft in FOOD_TYPES:
        pool += [ft] * ft["prob"]
    return random.choice(pool)

def spawn_food(snake_pos, existing):
    occupied = snake_pos + [f["pos"] for f in existing]
    while True:
        n = random.randint(1, 23)
        m = random.randint(1, 23)
        if [n, m] not in occupied:
            ft = pick_food_type()
            return {"pos": [n, m], "value": ft["value"], "color": ft["color"],
                    "lifetime": ft["lifetime"], "born": pygame.time.get_ticks()}

foods.append(spawn_food(snake, []))

while running:
    for i in snake:
        if tuple(i) not in board:
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d and not a1:
                d1 = True; dir = [1, 0]; a1, s1, w1 = False, False, False
            elif event.key == pygame.K_a and not d1:
                a1 = True; dir = [-1, 0]; d1, s1, w1 = False, False, False
            elif event.key == pygame.K_w and not s1:
                w1 = True; dir = [0, -1]; a1, s1, d1 = False, False, False
            elif event.key == pygame.K_s and not w1:
                s1 = True; dir = [0, 1]; a1, d1, w1 = False, False, False

    now = pygame.time.get_ticks()
    foods = [f for f in foods if f["lifetime"] is None or now - f["born"] < f["lifetime"]]
    while len(foods) < 3:
        foods.append(spawn_food(snake, foods))

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (200, 128, 226), (20, 20, 460, 460))

    for i in snake:
        x, y = i
        pygame.draw.rect(screen, (0, 255, 0), (x*20, y*20, 20, 20))

    for f in foods:
        x, y = f["pos"]
        pygame.draw.rect(screen, f["color"], (x*20, y*20, 20, 20))
        if f["lifetime"]:
            elapsed = now - f["born"]
            ratio = 1 - elapsed / f["lifetime"]
            bar_w = int(20 * ratio)
            pygame.draw.rect(screen, (255, 255, 255), (x*20, y*20+17, bar_w, 3))

    txt = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(txt, (10, 515))

    s += 1
    if s % 60 == 0:
        u, i = snake[0]
        snake = shift_massive(snake)
        snake[-1][0] += dir[0]
        snake[-1][1] += dir[1]

        eaten = None
        for f in foods:
            if snake[-1] == f["pos"]:
                eaten = f
                break

        if eaten:
            snake.insert(0, [u, i])
            score += eaten["value"]
            foods.remove(eaten)
            foods.append(spawn_food(snake, foods))

        snake_check = snake.copy()
        snake_check.pop()
        for i in snake_check:
            if snake[-1] == i:
                running = False

    pygame.display.flip()
    clock.tick(500)

pygame.quit()