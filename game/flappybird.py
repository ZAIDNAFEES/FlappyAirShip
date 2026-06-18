import pygame
import sys
import random
import os
import math
os.system('cls')

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 420, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# COLORS
WHITE = (255,255,255)
GRAY = (40,40,40)
LIGHT = (220,220,220)
YELLOW = (255,220,0)
RED = (255,80,80)

# LOAD
bg = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))
player1 = pygame.transform.scale(pygame.image.load("player.png"), (80,40))
player2 = pygame.transform.scale(pygame.image.load("player2.png"), (80,40))
pillar = pygame.transform.scale(pygame.image.load("pillar.png"), (70,400))
pillar_flip = pygame.transform.flip(pillar, False, True)
coin_img = pygame.transform.scale(pygame.image.load("coin.png"), (35,35))
rock_img = pygame.transform.scale(pygame.image.load("rock.png"), (50,50))

# SOUND
jump = pygame.mixer.Sound("jump.wav")
hit = pygame.mixer.Sound("hit.wav.wav")

font = pygame.font.Font("font.ttf", 24)
title = pygame.font.Font("font.ttf", 48)

# LOAD DATA
def load(file, default):
    try: return int(open(file).read())
    except: return default

coins_total = load("coins.txt",0)
high = load("highscore.txt",0)

# RESET
def reset():
    global px,py,vel,pillars,coins,rocks,score,coin_count,saved
    px,py = 80,300
    vel = 0
    pillars,coins,rocks = [],[],[]
    score,coin_count = 0,0
    saved = False

reset()
gravity = 0.5

def spawn():
    y = random.randint(150,400)
    pillars.append([WIDTH,y])
    coins.append([WIDTH+40,y+90])

def spawn_rock():
    y = random.randint(50,600)
    rocks.append([WIDTH,y])

# BUTTON CLASS
class Button:
    def __init__(self,x,y,w,h,text):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text

    def draw(self,color=(200,200,200)):
        pygame.draw.rect(screen,color,self.rect,border_radius=12)
        pygame.draw.rect(screen,(100,100,100),self.rect,2,border_radius=12)
        txt = font.render(self.text,True,(30,30,30))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self,e):
        return e.type==pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos)

# BUTTONS
play_btn = Button(140,300,140,50,"PLAY")
skins_btn = Button(140,370,140,50,"SKINS")

buy_btn = Button(240,420,120,40,"BUY")
use_btn = Button(60,420,120,40,"USE")
back_btn = Button(140,500,140,50,"BACK")

retry_btn = Button(140,420,140,50,"RETRY")
menu_btn = Button(140,490,140,50,"MENU")

resume_btn = Button(140,400,140,50,"RESUME")

pause_btn = pygame.Rect(WIDTH-60,20,40,40)

# GAME STATE
state = "menu"
skin = "default"

# LOOP
while True:

    screen.blit(bg,(0,0))

    # MENU
    if state=="menu":
        screen.blit(title.render("SKY ESCAPE",True,WHITE),(60,150))
        screen.blit(font.render(f"BEST: {high}",True,YELLOW),(140,230))
        screen.blit(font.render(f"COINS: {coins_total}",True,YELLOW),(140,260))

        play_btn.draw()
        skins_btn.draw()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if play_btn.click(e):
                reset()
                state="play"
            if skins_btn.click(e):
                state="skins"

    # SKINS
    elif state=="skins":

        screen.blit(title.render("SKINS",True,WHITE),(120,80))

        # DEFAULT CARD
        pygame.draw.rect(screen,LIGHT,(50,200,140,180),border_radius=15)
        screen.blit(player1,(80,230))
        screen.blit(font.render("FREE",True,GRAY),(90,300))

        # SPACE CARD
        pygame.draw.rect(screen,LIGHT,(230,200,140,180),border_radius=15)
        screen.blit(player2,(260,230))
        screen.blit(font.render("500",True,YELLOW),(280,300))

        use_btn.draw()
        buy_btn.draw()
        back_btn.draw()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()

            if use_btn.click(e):
                skin="default"

            if buy_btn.click(e):
                if coins_total>=500:
                    coins_total-=500
                    skin="space"

            if back_btn.click(e):
                state="menu"

    # GAME
    elif state=="play":

        speed = 4 + score//10
        gap = 180

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()

            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    vel=-9
                    jump.play()

            if e.type==pygame.MOUSEBUTTONDOWN:
                if pause_btn.collidepoint(e.pos):
                    state="pause"

        vel += gravity
        py += vel

        if py<0 or py>HEIGHT:
            hit.play()
            state="gameover"

        if len(pillars)==0 or pillars[-1][0]<WIDTH-250:
            spawn()

        if random.randint(0,120)==1:
            spawn_rock()

        player = player1 if skin=="default" else player2
        rect = pygame.Rect(px,int(py),80,40)

        for p in pillars:
            p[0]-=speed
            screen.blit(pillar_flip,(p[0],p[1]-400))
            screen.blit(pillar,(p[0],p[1]+gap))

            if rect.colliderect(pygame.Rect(p[0],p[1]-400,70,400)) or \
               rect.colliderect(pygame.Rect(p[0],p[1]+gap,70,400)):
                hit.play()
                state="gameover"

        for c in coins[:]:
            c[0]-=speed
            screen.blit(coin_img,(c[0],c[1]))
            if rect.colliderect(pygame.Rect(c[0],c[1],35,35)):
                coins.remove(c)
                coin_count+=1

        for r in rocks[:]:
            r[0]-=speed+2
            screen.blit(rock_img,(r[0],r[1]))
            if rect.colliderect(pygame.Rect(r[0],r[1],50,50)):
                hit.play()
                state="gameover"

        screen.blit(player,(px,int(py)))

        score+=0.05
        if score>high: high=int(score)

        screen.blit(font.render(f"{int(score)}",True,WHITE),(10,10))

        # PAUSE BUTTON
        pygame.draw.rect(screen,(60,60,60),pause_btn)
        pygame.draw.line(screen,WHITE,(pause_btn.x+12,25),(pause_btn.x+12,45),4)
        pygame.draw.line(screen,WHITE,(pause_btn.x+25,25),(pause_btn.x+25,45),4)

    # PAUSE
    elif state=="pause":
        screen.blit(title.render("PAUSED",True,WHITE),(100,200))
        resume_btn.draw()
        menu_btn.draw()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if resume_btn.click(e): state="play"
            if menu_btn.click(e): state="menu"

    # GAME OVER
    elif state=="gameover":

        if not saved:
            coins_total += coin_count
            open("coins.txt","w").write(str(coins_total))
            open("highscore.txt","w").write(str(high))
            saved=True

        screen.blit(title.render("GAME OVER",True,RED),(70,180))
        screen.blit(font.render(f"SCORE: {int(score)}",True,WHITE),(120,260))
        screen.blit(font.render(f"+{coin_count} coins",True,YELLOW),(120,300))

        retry_btn.draw()
        menu_btn.draw()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()

            if retry_btn.click(e):
                reset()
                state="play"

            if menu_btn.click(e):
                state="menu"

    pygame.display.update()
    clock.tick(60)