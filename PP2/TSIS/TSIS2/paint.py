import pygame
import sys
from datetime import datetime
from tools import (draw_pencil, draw_line, draw_rect, draw_square,
                   draw_circle, draw_right_triangle, draw_equilateral_triangle,
                   draw_rhombus, draw_eraser, flood_fill)

pygame.init()

W, H = 1000, 650
PANEL = 55
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint")

canvas = pygame.Surface((W, H - PANEL))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 13, bold=True)
font_text = pygame.font.SysFont("Arial", 20)

TOOLS = ["Pencil", "Line", "Rect", "Square", "Circle",
         "RtTri", "EqTri", "Rhombus", "Eraser", "Fill", "Text", "Picker"]

COLORS = [
    (0,0,0), (255,255,255), (128,128,128), (192,192,192),
    (255,0,0), (0,180,0), (0,0,255), (255,220,0),
    (255,140,0), (0,220,220), (220,0,220), (160,0,0),
    (0,100,0), (0,0,140), (200,100,0), (100,0,200),
]

SIZES = [2, 5, 10]

cur_tool  = "Pencil"
cur_color = (0, 0, 0)
cur_size  = 2

drawing   = False
start_pos = None
last_pos  = None
snapshot  = None

typing    = False
typed     = ""
text_pos  = (0, 0)


def draw_panel():
    pygame.draw.rect(screen, (215, 215, 220), (0, 0, W, PANEL))
    pygame.draw.line(screen, (150, 150, 160), (0, PANEL), (W, PANEL), 2)

    # tool buttons
    bw, bh = 52, 34
    for i, t in enumerate(TOOLS):
        rx = 4 + i * (bw + 3)
        ry = 10
        color = (55, 115, 205) if t == cur_tool else (180, 180, 190)
        pygame.draw.rect(screen, color, (rx, ry, bw, bh), border_radius=4)
        label = font.render(t[:5], True, (255,255,255) if t == cur_tool else (10,10,10))
        screen.blit(label, (rx + bw//2 - label.get_width()//2, ry + 9))

    # size buttons
    sx = 4 + len(TOOLS) * (bw + 3) + 8
    for i, s in enumerate(SIZES):
        rx = sx + i * 44
        color = (55, 115, 205) if s == cur_size else (180, 180, 190)
        pygame.draw.rect(screen, color, (rx, 10, 40, bh), border_radius=4)
        dot = (255,255,255) if s == cur_size else (10,10,10)
        pygame.draw.circle(screen, dot, (rx + 20, 27), s + 1)

    # color palette
    cx = sx + 3 * 44 + 10
    cw = 16
    for i, c in enumerate(COLORS):
        rx = cx + (i % 8) * (cw + 2)
        ry = 5 + (i // 8) * (cw + 2)
        pygame.draw.rect(screen, c, (rx, ry, cw, cw))
        if c == cur_color:
            pygame.draw.rect(screen, (55,115,205), (rx-2, ry-2, cw+4, cw+4), 2)

    # active color preview
    ax = cx + 8 * (cw + 2) + 6
    pygame.draw.rect(screen, cur_color, (ax, 10, 30, bh))
    pygame.draw.rect(screen, (60,60,60), (ax, 10, 30, bh), 2)


def panel_click(mx, my):
    global cur_tool, cur_color, cur_size
    bw, bh = 52, 34

    for i, t in enumerate(TOOLS):
        if pygame.Rect(4 + i*(bw+3), 10, bw, bh).collidepoint(mx, my):
            cur_tool = t
            return

    sx = 4 + len(TOOLS) * (bw + 3) + 8
    for i, s in enumerate(SIZES):
        if pygame.Rect(sx + i*44, 10, 40, bh).collidepoint(mx, my):
            cur_size = s
            return

    cx = sx + 3*44 + 10
    cw = 16
    for i, c in enumerate(COLORS):
        rx = cx + (i % 8) * (cw + 2)
        ry = 5 + (i // 8) * (cw + 2)
        if pygame.Rect(rx, ry, cw, cw).collidepoint(mx, my):
            cur_color = c
            return


def apply_shape(surf, tool, p1, p2, color, size):
    if tool == "Line":    draw_line(surf, p1, p2, color, size)
    elif tool == "Rect":  draw_rect(surf, p1, p2, color, size)
    elif tool == "Square": draw_square(surf, p1, p2, color, size)
    elif tool == "Circle": draw_circle(surf, p1, p2, color, size)
    elif tool == "RtTri":  draw_right_triangle(surf, p1, p2, color, size)
    elif tool == "EqTri":  draw_equilateral_triangle(surf, p1, p2, color, size)
    elif tool == "Rhombus": draw_rhombus(surf, p1, p2, color, size)


clock = pygame.time.Clock()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                pygame.image.save(canvas, f"canvas_{ts}.png")

            if not typing:
                if e.key == pygame.K_1: cur_size = 2
                if e.key == pygame.K_2: cur_size = 5
                if e.key == pygame.K_3: cur_size = 10

            if typing:
                if e.key == pygame.K_RETURN:
                    canvas.blit(font_text.render(typed, True, cur_color), text_pos)
                    typing = False; typed = ""
                elif e.key == pygame.K_ESCAPE:
                    typing = False; typed = ""
                elif e.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]
                elif e.unicode and e.unicode.isprintable():
                    typed += e.unicode

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = e.pos
            if my < PANEL:
                panel_click(mx, my)
            else:
                cp = (mx, my - PANEL)
                if cur_tool == "Picker":
                    cur_color = canvas.get_at(cp)[:3]
                elif cur_tool == "Fill":
                    flood_fill(canvas, cp[0], cp[1], cur_color)
                elif cur_tool == "Text":
                    if typing:
                        canvas.blit(font_text.render(typed, True, cur_color), text_pos)
                    typing = True; text_pos = cp; typed = ""
                elif cur_tool in ("Pencil", "Eraser"):
                    drawing = True; last_pos = cp
                else:
                    drawing = True; start_pos = cp; snapshot = canvas.copy()

        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            if drawing:
                cp = (e.pos[0], e.pos[1] - PANEL)
                if cur_tool not in ("Pencil", "Eraser") and start_pos:
                    apply_shape(canvas, cur_tool, start_pos, cp, cur_color, cur_size)
                drawing = False; start_pos = None; snapshot = None

        if e.type == pygame.MOUSEMOTION and drawing:
            mx, my = e.pos
            if my < PANEL:
                continue
            cp = (mx, my - PANEL)
            if cur_tool == "Pencil":
                draw_pencil(canvas, last_pos, cp, cur_color, cur_size)
                last_pos = cp
            elif cur_tool == "Eraser":
                draw_eraser(canvas, last_pos, cp, cur_size)
                last_pos = cp

    screen.blit(canvas, (0, PANEL))

    if drawing and cur_tool not in ("Pencil", "Eraser") and start_pos and snapshot:
        mx, my = pygame.mouse.get_pos()
        cp = (mx, my - PANEL)
        preview_surf = snapshot.copy()
        apply_shape(preview_surf, cur_tool, start_pos, cp, cur_color, cur_size)
        screen.blit(preview_surf, (0, PANEL))

    if typing:
        preview = font_text.render(typed, True, cur_color)
        screen.blit(preview, (text_pos[0], text_pos[1] + PANEL))
        cx = text_pos[0] + preview.get_width()
        cy = text_pos[1] + PANEL
        pygame.draw.line(screen, cur_color, (cx, cy), (cx, cy + font_text.get_height()), 2)

    draw_panel()
    pygame.display.flip()
    clock.tick(60)