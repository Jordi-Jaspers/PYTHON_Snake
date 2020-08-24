## Imports
import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox

##Constants
_FPS = 10
_HEIGHT = 720
_WIDTH = 1280
_CELLWIDTH = 16
_ROWS = _HEIGHT/_CELLWIDTH
_COLUMNS = _WIDTH/_CELLWIDTH
_BACKGROUND = "background.png"

class Cube(object):
    def __init__(self, start, xVel = 1, yVel = 0, color=(255, 0, 0)):
        self.pos = start
        self.xVel = 1
        self.yVel = 0
        self.color = color

    def move(self, xVel, yVel):
        self.xVel = xVel
        self.yVel = yVel
        self.pos(self.pos[0] + self.xVel, self.pos[1] + self.yVel)   

    def draw(self, surface, eyes=False):
        dis = _CELLWIDTH
        i = self.pos[0]
        j = self.pos[1]

        # Draw the cube
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        # Draw eyes on the cube if it is the head of the snake
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class Snake(object):
    # List of body cubes with coordinates
    body = []

    # Dictionary remembers when the cube has turned
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.xVel = 1
        self.yVel = 0

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                #draw eyes on the head of the snake
                c.draw(surface, True)
            else:
                c.draw(surface)    

    def reset(self, pos):
        pass

    def addCube(self):
        pass

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_RIGHT]:
                    self.xVel = 1
                    self.yVel = 0
                    self.turns[self.head.pos[:]] = [self.xVel, self.yVel]

                elif keys[pygame.K_LEFT]:
                    self.xVel = -1
                    self.yVel = 0
                    self.turns[self.head.pos[:]] = [self.xVel, self.yVel]

                elif keys[pygame.K_UP]:
                    self.xVel = 0
                    self.yVel = -1
                    self.turns[self.head.pos[:]] = [self.xVel, self.yVel]

                elif keys[pygame.K_DOWN]:
                    self.xVel = 0
                    self.yVel = 1
                    self.turns[self.head.pos[:]] = [self.xVel, self.yVel]

            for i, c in enumerate(self.body):
                p = c.pos[:]
                if p in self.turns:
                    turn = self.turns[p]
                    c.move(turn[0], turn[1])
                    if i == len(self.body) - 1:
                        self.turn.pop(p)

                else:
                    if   c.xVel == -1 and c.pos[0] <= 0: 
                        c.pos = (_ROWS - 1, c.pos[1]) 
                    elif c.xVel == 1 and c.pos[0]  >= _ROWS-1: 
                        c.pos = (0, c.pos[1])
                    elif c.yVel == 1 and c.pos[1]  >= _ROWS-1: 
                        c.pos = (c.pos[0], 0)
                    elif c.yVel == -1 and c.pos[1] <= 0: 
                        c.pos = (c.pos[0] - 1, _ROWS-1)
                    else: c.move (c.xVel, c.yVel)   

def introScreen(surface):
    # Load in image
    intro_background = pygame.image.load(_BACKGROUND)
    intro_background = pygame.transform.scale(intro_background,(_WIDTH, _HEIGHT))
    surface.blit(intro_background, (0,0))

    # Render in label
    pygame.font.init()
    myfont = pygame.font.SysFont("monospace", 24)
    label = myfont.render("© 2020 - Jordi Jaspers", 1, (0,0,0))
    surface.blit(label, (0, 696))

    #update
    pygame.display.update() 

def drawGrid(surface):
    x = 0
    y = 0

    for i in range(math.floor(_COLUMNS)):
        x = x + _CELLWIDTH
        pygame.draw.line(surface, (255,255,255), (x, 0), (x, _WIDTH)) 

    for j in range(math.floor(_ROWS)):
        y = y + _CELLWIDTH
        pygame.draw.line(surface, (255,255,255), (0, y), (_WIDTH, y))
    
def updateGrid(surface):
    global s

    s.draw(surface)
    surface.fill((0,0,0))
    drawGrid(surface)
    pygame.display.update() 

def randomSnack(snake):
    positions = snake.body

    while True:
        x = random.randrange(_ROWS)
        y = random.randrange(_COLUMNS)
        
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)            

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

## Main function of the program
def main():
    global s
    s = Snake( (255,0,0), (_ROWS//2, _COLUMNS//2))
    snack = Cube(randomSnack(s), color=(0,255,0))

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((_WIDTH, _HEIGHT))
    pygame.display.set_caption('Snake - The Game')
    
    intro = True
    running = False
    outro = False    
    
    while intro:
        introScreen(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:    
                    intro = False  
                    running = True           

    while running:  
        pygame.time.delay(50)   
        clock.tick(_FPS) 

        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(s), color=(0,255,0)) 

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print(\'Score: \', len(s.body))
                message_box(\'You Lost!\', \'Play again...\')
                s.reset((_ROWS//2, _COLUMNS//2))
                break

        updateGrid(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                quit()                  

    pass

main()
