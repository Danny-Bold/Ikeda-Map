import math
import glob

import pygame
import cv2


SIZE = (3840, 2160)

xRange = (1 - 16 / 3, 1 + 16 / 3)
yRange = (-3, 3)

GRIDSIDELENGTH = 500

U = 0.9

MAP_ITERS = 16  # Number of map applications

GAP_BETWEEN_ITERS = 30  # number of frames between end of one animation and start of next

ANIMATION_LENGTH = 60  # length of transition from one state to the next


def videoGen():
    filenames = glob.glob('img/*.png')

    out = cv2.VideoWriter(
        'vid/vid.mp4',
        cv2.VideoWriter_fourcc(*'mp4v'),
        60,
        SIZE
    )

    for x in range(len(filenames)):
        img = cv2.imread('img/' + str(x) + '.png')
        out.write(img)

    out.release()


def interp(x):
    return x ** 3 * (1 - x) + x * (1 - (1 - x) ** 3)


class Particle:
    def __init__(self, pos, col=(255, 255, 255)):
        self.pos = pos
        self.lastPos = pos
        self.col = col

    def draw(self, screen, animatingFrame, animating=False):

        pos = (self.pos[0] - xRange[0]) * SIZE[0] / (xRange[1] - xRange[0]), \
              SIZE[1] - (self.pos[1] - yRange[0]) * SIZE[1] / (yRange[1] - yRange[0])

        if not animating:
            pygame.draw.circle(screen, self.col, pos, 1)

        else:
            lastPos = (self.lastPos[0] - xRange[0]) * SIZE[0] / (xRange[1] - xRange[0]),\
                  SIZE[1] - (self.lastPos[1] - yRange[0]) * SIZE[1] / (yRange[1] - yRange[0])

            interpVal = interp(1 - animatingFrame / ANIMATION_LENGTH)

            interpPos = (pos[0] - lastPos[0]) * interpVal + lastPos[0], (pos[1] - lastPos[1]) * interpVal + lastPos[1]

            pygame.draw.circle(screen, self.col, interpPos, 1)

    def update(self):
        """

        Perform the Ikeda map on self.pos

        """

        self.lastPos = [self.pos[0], self.pos[1]]

        t = 0.4 - 6 / (1 + self.pos[0] ** 2 + self.pos[1] ** 2)

        x = 1 + U * (self.pos[0] * math.cos(t) - self.pos[1] * math.sin(t))
        y = U * (self.pos[0] * math.sin(t) + self.pos[1] * math.cos(t))

        self.pos = [x, y]


def main():
    pList = []

    c = pygame.Color(0, 0, 0)

    animating = 0

    animStage = 0  # 0 = waiting, 1 = animating

    waitingCounter = GAP_BETWEEN_ITERS

    iterations = 0

    frameCounter = 0

    for x in range(GRIDSIDELENGTH):
        for y in range(GRIDSIDELENGTH):
            c.hsva = ((x + y) / GRIDSIDELENGTH * 360 % 360, 100, 100, 0)
            xPos = x / GRIDSIDELENGTH * (xRange[1] - xRange[0]) + xRange[0]
            yPos = y / GRIDSIDELENGTH * (yRange[1] - yRange[0]) + yRange[0]
            pList.append(Particle((xPos, yPos), col=(c.r, c.g, c.b)))

    screen = pygame.surface.Surface(SIZE)

    while iterations != MAP_ITERS:

        screen.fill((0, 0, 0))

        for p in pList:
            p.draw(screen, animating, animating=bool(animStage))

        if animStage == 1:
            animating -= 1

        if animating == 0:
            animStage = 0
            animating = ANIMATION_LENGTH
            iterations += 1

        if animStage == 0:
            waitingCounter -= 1

        if waitingCounter == 0:
            animStage = 1
            for p in pList:
                p.update()
            waitingCounter = GAP_BETWEEN_ITERS

        pygame.image.save(screen, 'img/' + str(frameCounter) + '.png')

        print('frame', frameCounter, 'generated')

        frameCounter += 1

    for frame in range(GAP_BETWEEN_ITERS):  # Make a waiting period at the end for convenience:

        screen.fill((0, 0, 0))

        for p in pList:
            p.draw(screen, animating, animating=bool(animStage))

        pygame.image.save(screen, 'img/' + str(frameCounter) + '.png')

        print('frame', frameCounter, 'generated')

        frameCounter += 1

    videoGen()


if __name__ == '__main__':
    main()
