import pygame, sys, math

pygame.init()
W, H = 800, 600
PANEL = 50
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint")
clock = pygame.font.SysFont(None, 20)
font = pygame.font.SysFont(None, 20)

COLORS = [(0,0,0),(255,255,255),(255,0,0),(0,200,0),(0,0,255),
          (255,255,0),(255,140,0),(180,0,180),(0,200,200),(150,75,0)]

tool = "pencil"; color = (0,0,0); size = 3
drawing = False; start = None
canvas = pygame.Surface((W, H-PANEL)); canvas.fill((255,255,255))
undo = []
TOOLS = ["pencil","eraser","line","rect","square","rtri","equitri","rhombus"]
clock2 = pygame.time.Clock()

def save():
    undo.append(canvas.copy())
    if len(undo) > 20: undo.pop(0)

def square_pts(p1, p2):
    dx,dy = p2[0]-p1[0], p2[1]-p1[1]
    s = min(abs(dx),abs(dy))
    ex,ey = p1[0]+(s if dx>=0 else -s), p1[1]+(s if dy>=0 else -s)
    return [p1,(ex,p1[1]),(ex,ey),(p1[0],ey)]

def rtri_pts(p1, p2): return [p1,(p2[0],p1[1]),p2]

def equitri_pts(p1, p2):
    mx,my = (p1[0]+p2[0])/2,(p1[1]+p2[1])/2
    base = math.hypot(p2[0]-p1[0],p2[1]-p1[1]) or 1
    dx,dy = (p2[0]-p1[0])/base,(p2[1]-p1[1])/base
    h = base*math.sqrt(3)/2
    return [p1,p2,(mx-dy*h, my+dx*h)]

def rhombus_pts(p1, p2):
    cx,cy = (p1[0]+p2[0])/2,(p1[1]+p2[1])/2
    dx,dy = abs(p2[0]-p1[0])/2, abs(p2[1]-p1[1])/2
    return [(cx,cy-dy),(cx+dx,cy),(cx,cy+dy),(cx-dx,cy)]

PTS = {"square":square_pts,"rtri":rtri_pts,"equitri":equitri_pts,"rhombus":rhombus_pts}

def draw_shape(surf, t, p1, p2, c, s):
    if t=="line": pygame.draw.line(surf,c,p1,p2,s)
    elif t=="rect":
        pygame.draw.rect(surf,c,pygame.Rect(min(p1[0],p2[0]),min(p1[1],p2[1]),abs(p2[0]-p1[0]),abs(p2[1]-p1[1])),s)
    elif t in PTS:
        pts=[(int(x),int(y)) for x,y in PTS[t](p1,p2)]
        if len(pts)>=3: pygame.draw.polygon(surf,c,pts,s)

def draw_panel():
    pygame.draw.rect(screen,(50,50,50),(0,0,W,PANEL))
    for i,col in enumerate(COLORS):
        r=pygame.Rect(5+i*26,5,22,22); pygame.draw.rect(screen,col,r)
        pygame.draw.rect(screen,(200,200,200),r,1)
        if col==color: pygame.draw.rect(screen,(255,255,100),r,2)
    pygame.draw.rect(screen,color,(275,5,22,22))
    pygame.draw.rect(screen,(255,255,255),(275,5,22,22),2)
    for i,t in enumerate(TOOLS):
        r=pygame.Rect(304+i*58,5,54,18)
        pygame.draw.rect(screen,(80,120,200) if t==tool else (80,80,80),r,border_radius=3)
        screen.blit(font.render(t,True,(240,240,240)),(r.x+3,r.y+3))
    for i,sz in enumerate([2,4,8,14]):
        r=pygame.Rect(304+i*32,28,28,16)
        pygame.draw.rect(screen,(80,120,200) if sz==size else (70,70,70),r,border_radius=2)
        screen.blit(font.render(str(sz),True,(240,240,240)),(r.x+8,r.y+2))
    screen.blit(font.render("Ctrl+Z",True,(150,150,150)),(W-55,15))

while True:
    clock2.tick(60)
    mp=pygame.mouse.get_pos(); cp=(mp[0],mp[1]-PANEL)
    for e in pygame.event.get():
        if e.type==pygame.QUIT: pygame.quit(); sys.exit()
        if e.type==pygame.KEYDOWN and e.key==pygame.K_z and (pygame.key.get_mods()&pygame.KMOD_CTRL):
            if undo: canvas.blit(undo.pop(),(0,0))
        if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
            if mp[1]<PANEL:
                for i,col in enumerate(COLORS):
                    if pygame.Rect(5+i*26,5,22,22).collidepoint(mp): color=col
                for i,t in enumerate(TOOLS):
                    if pygame.Rect(304+i*58,5,54,18).collidepoint(mp): tool=t
                for i,sz in enumerate([2,4,8,14]):
                    if pygame.Rect(304+i*32,28,28,16).collidepoint(mp): size=sz
            else:
                save(); drawing=True; start=cp
                if tool in("pencil","eraser"):
                    pygame.draw.circle(canvas,(255,255,255) if tool=="eraser" else color,cp,size*2 if tool=="eraser" else size)
        if e.type==pygame.MOUSEBUTTONUP and e.button==1:
            if drawing and mp[1]>=PANEL and tool not in("pencil","eraser"):
                draw_shape(canvas,tool,start,cp,color,size)
            drawing=False; start=None
        if e.type==pygame.MOUSEMOTION and drawing and mp[1]>=PANEL:
            if tool=="pencil":
                prev=(mp[0]-e.rel[0],mp[1]-e.rel[1]-PANEL)
                pygame.draw.line(canvas,color,prev,cp,size)
            elif tool=="eraser":
                pygame.draw.circle(canvas,(255,255,255),cp,size*2)

    screen.fill((200,200,200)); screen.blit(canvas,(0,PANEL))
    if drawing and start and tool not in("pencil","eraser") and mp[1]>=PANEL:
        g=pygame.Surface((W,H-PANEL),pygame.SRCALPHA)
        if tool=="line": pygame.draw.line(g,(*color,150),start,cp,size)
        elif tool=="rect":
            pts=[(min(start[0],cp[0]),min(start[1],cp[1])),(max(start[0],cp[0]),min(start[1],cp[1])),(max(start[0],cp[0]),max(start[1],cp[1])),(min(start[0],cp[0]),max(start[1],cp[1]))]
            pygame.draw.polygon(g,(*color,60),pts,0); pygame.draw.polygon(g,(*color,200),pts,size)
        elif tool in PTS:
            pts=[(int(x),int(y)) for x,y in PTS[tool](start,cp)]
            if len(pts)>=3: pygame.draw.polygon(g,(*color,60),pts,0); pygame.draw.polygon(g,(*color,200),pts,size)
        screen.blit(g,(0,PANEL))
    draw_panel()
    pygame.display.flip()
