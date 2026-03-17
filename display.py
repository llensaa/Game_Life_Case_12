import pygame
import os
import math

_alive_color = (255, 255, 255)
_dead_color = (0, 0, 0)
_grid_color = (40, 40, 40)
_text_color = (0, 255, 0)

_font_small = None
_font_medium = None
_font_large = None

RES_PATH = "Case_12/resources"
IMG_PATH = os.path.join(RES_PATH, "images")
SND_PATH = os.path.join(RES_PATH, "sounds")

SCREEN_MAIN_MENU = 0
SCREEN_SHAPE_SELECT = 1
SCREEN_COLOR_SELECT = 2
SCREEN_GAME = 3

SHAPE_SQUARE = 0
SHAPE_HEXAGON = 1

SHAPE_NAMES = {
    SHAPE_SQUARE: "Квадрат",
    SHAPE_HEXAGON: "Шестиугольник"
}

COLOR_SCHEMES = [
    ("Классическая", (255,255,255),(0,0,0),(40,40,40)),
    ("Неоновая", (0,255,0),(0,0,0),(0,50,0)),
    ("Огненная", (255,100,0),(30,0,0),(80,20,0)),
    ("Морская", (0,150,255),(0,0,50),(0,30,80)),
    ("Мистическая", (200,0,255),(30,0,30),(60,0,60))
]

class Button:
    def __init__(self,x,y,w,h,text):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.hover = False

    def draw(self,screen):
        color = (150,150,150) if self.hover else (100,100,100)
        pygame.draw.rect(screen,color,self.rect)
        pygame.draw.rect(screen,(255,255,255),self.rect,2)
        txt = _font_medium.render(self.text,True,(255,255,255))
        screen.blit(txt,txt.get_rect(center=self.rect.center))

    def handle(self,e):
        if e.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(e.pos)
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            return self.rect.collidepoint(e.pos)
        return False

def init_display(rows,cols,cell=20):
    global _font_small,_font_medium,_font_large
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    _font_small = pygame.font.Font(None,24)
    _font_medium = pygame.font.Font(None,36)
    _font_large = pygame.font.Font(None,48)

    w = cols*cell if rows else 800
    h = rows*cell+60 if rows else 600

    screen = pygame.display.set_mode((w,h))
    clock = pygame.time.Clock()
    return screen,clock,w,h

def load_background(screen):
    try:
        p = os.path.join(IMG_PATH,"menu_bg.jpg")
        if os.path.exists(p):
            img = pygame.image.load(p)
            return pygame.transform.scale(img,screen.get_size())
    except:
        pass
    return None

def load_music():
    try:
        p = os.path.join(SND_PATH,"background_music.mp3")
        if os.path.exists(p):
            pygame.mixer.music.load(p)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
    except:
        pass

def handle_color_scheme(a,d,g):
    global _alive_color,_dead_color,_grid_color
    _alive_color,_dead_color,_grid_color = a,d,g

def draw_hex(screen,x,y,size,color):
    pts = [(x+size*math.cos(math.pi/3*i),y+size*math.sin(math.pi/3*i)) for i in range(6)]
    pygame.draw.polygon(screen,color,pts)

def draw_grid(screen,grid,shape):
    rows,cols = len(grid),len(grid[0])
    w,_ = screen.get_size()
    cell = w//cols

    for r in range(rows):
        for c in range(cols):
            color = _alive_color if grid[r][c] else _dead_color
            x,y = c*cell,r*cell
            if shape == SHAPE_SQUARE:
                pygame.draw.rect(screen,color,(x,y,cell,cell))
            else:
                draw_hex(screen,x+cell//2,y+cell//2,cell//2,color)

def draw_ui(screen,gen,speed,run):
    w,h = screen.get_size()
    pygame.draw.rect(screen,(20,20,20),(0,h-80,w,80))

    screen.blit(_font_medium.render(f"Gen:{gen}",True,_text_color),(10,h-70))
    screen.blit(_font_medium.render(f"{speed:.2f}",True,_text_color),(10,h-40))
    screen.blit(_font_medium.render("RUN" if run else "PAUSE",True,(0,255,0)),(w-150,h-70))

    controls = "SPACE старт/пауза | S/→ шаг | R сброс | C очистка | L загрузка | F сохранить | +/- скорость | Q выход"
    txt = _font_small.render(controls, True, (180,180,180))
    screen.blit(txt,(w//2 - txt.get_width()//2, h-25))

def create_buttons(names,w,start=200):
    return [Button(w//2-75,start+i*70,150,50,n) for i,n in enumerate(names)]