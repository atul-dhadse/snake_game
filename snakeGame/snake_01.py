import pygame
import sys
import random
import math
from pygame.locals import *

WINDOWWIDTH = 750
WINDOWHEIGHT = 600

CELLSIZE = 15
FPS = 15

assert (WINDOWWIDTH % CELLSIZE == 0)
assert (WINDOWHEIGHT % CELLSIZE == 0)

CELLWIDHT = int(WINDOWWIDTH/CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT/CELLSIZE)

#colors
DARKGREEN = (0  ,153,  0)
BLACK     = (0  ,0  ,  0)
GREY      = (40 ,40 , 40)
RED       = (255,0  ,  0)
GREEN     = (128,255,128)
WHITE     = (255,255,255)

BGCOLOR  = BLACK

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

def main():
    pygame.init()
    global DISPLAYSURF, FPSCLOCK
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    FPSCLOCK = pygame.time.Clock()

    showStartScreen()

    while True:
        runGame()
        gameOverScreen()

def runGame():
    
    HEAD = 0
    start_x = random.randint(5, CELLWIDHT - 5)
    start_y = random.randint(5, CELLHEIGHT - 5)

    direction = RIGHT

    wormCords = [
        {'x' : start_x    , 'y' : start_y},
        {'x' : start_x - 1, 'y' : start_y},
        {'x' : start_x - 2, 'y' : start_y}
    ]

    apple = getRandomLocation()


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_UP and direction != DOWN:
                    direction = UP
                elif event.key == K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == K_RIGHT and direction != LEFT:
                    direction = RIGHT

        if direction == UP:
            HEAD = {'x' : wormCords[0]['x'], 'y' : wormCords[0]['y'] - 1}
            # start_y -= 1
        elif direction == DOWN:
            HEAD = {'x' : wormCords[0]['x'], 'y' : wormCords[0]['y'] + 1}
            # start_y += 1
        elif direction == LEFT:
            HEAD = {'x' : wormCords[0]['x'] - 1, 'y' : wormCords[0]['y']}
            # start_x -= 1
        elif direction == RIGHT:
            HEAD = {'x' : wormCords[0]['x'] + 1, 'y' : wormCords[0]['y']}
            # start_x += 1

        if wormCords[0]['x'] == -1 or wormCords[0]['x'] == CELLWIDHT or wormCords[0]['y'] == -1 or wormCords[0]['y'] == CELLHEIGHT:
            return

        for worm in wormCords[1:]:
            if worm['x'] == wormCords[0]['x'] and worm['y'] == wormCords[0]['y']:
                return

        wormCords.insert(0, HEAD)

        if apple['x'] == wormCords[0]['x'] and apple['y'] == wormCords[0]['y']:
            apple = getRandomLocation()
        else:
            del wormCords[-1]

        DISPLAYSURF.fill(BGCOLOR)
        drawGrids()
        drawWorm(wormCords)
        drawApple(apple)
        drawScores(len(wormCords) - 3)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawScores(scores):
    FONT = pygame.font.Font("freesansbold.ttf", 20)
    FONTSURF = FONT.render("score : " + str(scores), True, WHITE)
    FONTRECT = FONTSURF.get_rect()
    FONTRECT.topleft = (WINDOWWIDTH - 100, 10)
    DISPLAYSURF.blit(FONTSURF, FONTRECT)

def drawApple(apple):
    pygame.draw.rect(DISPLAYSURF, RED, (apple['x'] * CELLSIZE, apple['y'] * CELLSIZE, CELLSIZE, CELLSIZE))

def getRandomLocation():
    return {'x' : random.randint(0, CELLWIDHT - 1), 'y' : random.randint(0, CELLHEIGHT - 1)}


def drawGrids():
    for i in range(CELLHEIGHT):
        pygame.draw.line(DISPLAYSURF, GREY, (0, CELLSIZE * i), (WINDOWWIDTH, CELLSIZE * i))
    for i in range(CELLWIDHT):
        pygame.draw.line(DISPLAYSURF, GREY, (CELLSIZE * i, 0), (CELLSIZE * i, WINDOWHEIGHT))


def terminate():
    pygame.quit()
    sys.exit()


def checkKeyPress():
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
            else:
                return True


def drawWorm(wormCords):
    for worm in wormCords:
        worm_x = worm['x'] * CELLSIZE
        worm_y = worm['y'] * CELLSIZE
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, (worm_x, worm_y, CELLSIZE, CELLSIZE))
        pygame.draw.rect(DISPLAYSURF, GREEN, (worm_x + CELLSIZE//4, worm_y + CELLSIZE//4,math.ceil(CELLSIZE/2),math.ceil(CELLSIZE/2)))
    pygame.display.update()


def showStartScreen():
    FONT1 = pygame.font.Font("freesansbold.ttf", 100)
    FONT2 = pygame.font.Font("freesansbold.ttf", 100)
    angle1 = 15
    angle2 = 45
    FONT1SURF = FONT1.render("WORMY!", True, WHITE, DARKGREEN)
    FONT2SURF = FONT2.render("WORMY!", True, GREEN)
    while True:
        if checkKeyPress():
            pygame.event.get()
            return
        
        DISPLAYSURF.fill(BGCOLOR)
        ROTATE1SURF = pygame.transform.rotate(FONT1SURF, angle1)
        ROTATE2SURF = pygame.transform.rotate(FONT2SURF, angle2)
        FONT1RECT = ROTATE1SURF.get_rect()
        FONT2RECT = ROTATE2SURF.get_rect()
        FONT1RECT.center = (WINDOWWIDTH//2, WINDOWHEIGHT//2)
        FONT2RECT.center = (WINDOWWIDTH//2, WINDOWHEIGHT//2)
        DISPLAYSURF.blit(ROTATE1SURF, FONT1RECT)
        DISPLAYSURF.blit(ROTATE2SURF, FONT2RECT)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        angle1 += 3
        angle2 += 7

def drawMsg(msg, fontSize):
    FONT = pygame.font.Font("freesansbold.ttf", fontSize)
    FONTSURF = FONT.render(msg, True, WHITE)
    FONTRECT = FONTSURF.get_rect()
    # FONTRECT.topleft = (x, y)
    return FONTSURF, FONTRECT

def gameOverScreen():
    # scored = SCORE
    gameOverFont = pygame.font.Font('freesansbold.ttf', 75)
    gameOverSurf = gameOverFont.render('Game Over', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (WINDOWWIDTH / 2, 10)

    # scoreSurf, scoreRect = drawMsg("You Scored : " + str(scored))
    # scoreRect.midtop = (WINDOWWIDTH/2, gameOverRect.height + 25 + 10)

    msg1surf, msg1rect = drawMsg("To Continue.., Press Any Key", 30)
    msg2surf, msg2rect = drawMsg("To Exit, Press Esc Key", 30)
    msg1rect.midtop = (WINDOWWIDTH /2, gameOverRect.height + 10 + 25 + 25)
    msg2rect.midtop = (WINDOWWIDTH /2, gameOverRect.height + msg1rect.height + 10 + 25 + 25 + 25)
    DISPLAYSURF.blit(gameOverSurf, gameOverRect)
    # DISPLAYSURF.blit(scoreSurf, scoreRect)
    DISPLAYSURF.blit(msg1surf, msg1rect)
    DISPLAYSURF.blit(msg2surf, msg2rect)

    pygame.display.update()
    pygame.time.wait(500)
    checkKeyPress() # clear out any key presses in the event queue

    while True:
        if checkKeyPress():
            pygame.event.get() # clear event queue
            return

if __name__ == "__main__":
    main()
