from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *
from assets import *
from constants import *
from pipe_factory import PipeFactory
from population_factory import PopulationFactory

try:
    xrange
except NameError:
    xrange = range


def main():
    global SCREEN, FPSCLOCK, POPULATION, PIPES
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # numbers sprites for score display
    loadAssets(pygame)

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        # select random players
        POPULATION = PopulationFactory.create_random_population(10)

        # select random pipe sprites
        pipeImageindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(pygame.image.load(PIPES_LIST[pipeImageindex]).convert_alpha(), 180),
            pygame.image.load(PIPES_LIST[pipeImageindex]).convert_alpha(),
        )

        # hismask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        PIPES = [PipeFactory.getRandomPipe(), PipeFactory.getRandomPipe()]

        mainGame()


def mainGame():
    playerIndex = loopIter = 0
    playerIndexGen = cycle([0, 1, 2, 1])

    basex = 0
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = PipeFactory.getRandomPipe()
    newPipe2 = PipeFactory.getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        for bird in POPULATION.birds:
            distance_to_next_pipe = float(lowerPipes[0]['x'] - bird.x) / SCREENWIDTH
            pipe_hole = float((lowerPipes[0]['y']) - (PIPEGAPSIZE / 2)) / SCREENHEIGHT
            distance_to_pipe_hole = float(pipe_hole - bird.y) / SCREENHEIGHT
            if bird.should_flap(distance_to_next_pipe, distance_to_pipe_hole):
                if bird.y > -2 * IMAGES['player'][0].get_height():
                    bird.velY = playerFlapAcc

                bird.score -= pipeVelX

            # check for crash here
            if checkCrash(bird, playerIndex, upperPipes, lowerPipes)[0]:
                bird.dead()

        if len(POPULATION.alive()) == 0:
            return

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = PipeFactory.getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))


        playerHeight = IMAGES['player'][playerIndex].get_height()

        for bird in POPULATION.alive():
            # check for score
            playerMidPos = bird.x + IMAGES['player'][0].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    bird.score += 1

            # rotate the player
            if bird.rot > -90:
                bird.rot -= playerVelRot

            # player's movement
            if bird.velY < playerMaxVelY and not bird.flapped:
                bird.velY += playerAccY
            if bird.flapped:
                bird.flapped = False
                # more rotation to cover the threshold (calculated in visible rotation)
                bird.rot = 45

            bird.y += min(bird.velY, BASEY - bird.y - playerHeight)

            # Player rotation has a threshold
            visibleRot = playerRotThr
            if bird.rot <= playerRotThr:
                visibleRot = bird.rot

            playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
            SCREEN.blit(playerSurface, (bird.x, bird.y))
            # print score so player overlaps the score
            showScore(bird, bird.score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def showScore(bird, score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 12 + (bird.index*30)

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(bird, playerIndex, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    player = {}
    pi = playerIndex
    player['x'] = bird.x
    player['y'] = bird.y
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    elif player['y'] <= 0:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

if __name__ == '__main__':
    main()
