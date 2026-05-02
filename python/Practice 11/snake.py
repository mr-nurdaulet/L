import pygame
import random
import time

pygame.init()

CELL = 20
COLS = 30
ROWS = 25
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 20)

# food types: (points, color, lifetime seconds)
FOOD_TYPES = [
    {"points": 1, "color": (255, 107, 107), "lifetime": 10},
    {"points": 3, "color": (255, 217, 61),  "lifetime": 7},
    {"points": 5, "color": (107, 203, 119), "lifetime": 5},
]

def random_cell():
    return [random.randint(0, COLS-1), random.randint(0, ROWS-1)]

def spawn_food(snake):
    t = random.choice(FOOD_TYPES)
    while True:
        pos = random_cell()
        if pos not in snake:
            break
    return {
        "pos": pos,
        "points": t["points"],
        "color": t["color"],
        "lifetime": t["lifetime"],
        "spawned": time.time()
    }

def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (30, 42, 74), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (30, 42, 74), (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, seg in enumerate(snake):
        color = (78, 204, 163) if i == 0 else (46, 168, 135)
        pygame.draw.rect(screen, color, (seg[0]*CELL+1, seg[1]*CELL+1, CELL-2, CELL-2))

def draw_foods(foods):
    now = time.time()
    for f in foods:
        elapsed = now - f["spawned"]
        remaining = 1 - elapsed / f["lifetime"]
        # fade alpha
        alpha = int((0.4 + remaining * 0.6) * 255)
        color = tuple(min(255, c) for c in f["color"])

        # draw circle
        surf = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*color, alpha), (CELL//2, CELL//2), CELL//2 - 2)
        screen.blit(surf, (f["pos"][0]*CELL, f["pos"][1]*CELL))

        # timer bar
        bar_w = int((CELL - 4) * remaining)
        if bar_w > 0:
            pygame.draw.rect(screen, color, (f["pos"][0]*CELL+2, f["pos"][1]*CELL+CELL-5, bar_w, 3))

def main():
    snake = [[10, 10]]
    direction = [1, 0]
    next_dir = [1, 0]
    score = 0
    foods = []
    game_over = False
    move_timer = 0
    MOVE_DELAY = 0.15  # seconds per step

    # spawn initial food
    foods.append(spawn_food(snake))
    foods.append(spawn_food(snake))

    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                if event.key == pygame.K_UP    and direction[1] != 1:  next_dir = [0, -1]
                if event.key == pygame.K_DOWN  and direction[1] != -1: next_dir = [0,  1]
                if event.key == pygame.K_LEFT  and direction[0] != 1:  next_dir = [-1, 0]
                if event.key == pygame.K_RIGHT and direction[0] != -1: next_dir = [1,  0]

        if not game_over:
            # remove expired food
            now = time.time()
            foods = [f for f in foods if now - f["spawned"] < f["lifetime"]]
            while len(foods) < 2:
                foods.append(spawn_food(snake))

            # move snake by timer
            move_timer += dt
            if move_timer >= MOVE_DELAY:
                move_timer = 0
                direction = next_dir[:]
                head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

                # wall check
                if head[0] < 0 or head[0] >= COLS or head[1] < 0 or head[1] >= ROWS:
                    game_over = True
                elif head in snake:
                    game_over = True
                else:
                    snake.insert(0, head)

                    # food check
                    eaten = next((i for i, f in enumerate(foods) if f["pos"] == head), -1)
                    if eaten != -1:
                        score += foods[eaten]["points"]
                        foods.pop(eaten)
                        foods.append(spawn_food(snake))
                    else:
                        snake.pop()

        # draw
        screen.fill((22, 33, 62))
        draw_grid()
        draw_snake(snake)
        draw_foods(foods)

        score_text = font.render(f"Score: {score}", True, (238, 238, 238))
        screen.blit(score_text, (8, 6))

        if game_over:
            msg = font.render("Game Over! Press R", True, (233, 69, 96))
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))

        pygame.display.flip()

main()