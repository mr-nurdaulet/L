import pygame
import math
from collections import deque


def draw_pencil(surface, p1, p2, color, size):
    pygame.draw.line(surface, color, p1, p2, size)


def draw_line(surface, p1, p2, color, size):
    pygame.draw.line(surface, color, p1, p2, size)


def draw_rect(surface, p1, p2, color, size):
    x = min(p1[0], p2[0])
    y = min(p1[1], p2[1])
    w = abs(p2[0] - p1[0])
    h = abs(p2[1] - p1[1])
    if w > 0 and h > 0:
        pygame.draw.rect(surface, color, (x, y, w, h), size)


def draw_square(surface, p1, p2, color, size):
    side = min(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))
    x = p1[0] if p2[0] >= p1[0] else p1[0] - side
    y = p1[1] if p2[1] >= p1[1] else p1[1] - side
    if side > 0:
        pygame.draw.rect(surface, color, (x, y, side, side), size)


def draw_circle(surface, p1, p2, color, size):
    cx = (p1[0] + p2[0]) // 2
    cy = (p1[1] + p2[1]) // 2
    r = int(math.hypot(p2[0] - p1[0], p2[1] - p1[1]) / 2)
    if r > 0:
        pygame.draw.circle(surface, color, (cx, cy), r, size)


def draw_right_triangle(surface, p1, p2, color, size):
    points = [p1, (p2[0], p1[1]), p2]
    pygame.draw.polygon(surface, color, points, size)


def draw_equilateral_triangle(surface, p1, p2, color, size):
    base = abs(p2[0] - p1[0])
    if base == 0:
        return
    bx = min(p1[0], p2[0])
    by = max(p1[1], p2[1])
    h = int(base * math.sqrt(3) / 2)
    points = [(bx, by), (bx + base, by), (bx + base // 2, by - h)]
    pygame.draw.polygon(surface, color, points, size)


def draw_rhombus(surface, p1, p2, color, size):
    cx = (p1[0] + p2[0]) // 2
    cy = (p1[1] + p2[1]) // 2
    points = [(cx, p1[1]), (p2[0], cy), (cx, p2[1]), (p1[0], cy)]
    pygame.draw.polygon(surface, color, points, size)


def draw_eraser(surface, p1, p2, size):
    pygame.draw.line(surface, (255, 255, 255), p1, p2, size * 5)


def flood_fill(surface, x, y, new_color):
    w, h = surface.get_size()
    if x < 0 or x >= w or y < 0 or y >= h:
        return
    old_color = surface.get_at((x, y))[:3]
    if old_color == new_color[:3]:
        return
    queue = deque([(x, y)])
    visited = {(x, y)}
    while queue:
        cx, cy = queue.popleft()
        if surface.get_at((cx, cy))[:3] != old_color:
            continue
        surface.set_at((cx, cy), new_color)
        for nx, ny in [(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)]:
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))