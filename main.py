import sys
import math

import pygame


SIZE = (1000, 1000)

xRange = (-2, 4)
yRange = (-3, 3)

GRIDSIDELENGTH = 100

U = 0.9

# TODO make video


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

        lastPos = (self.lastPos[0] - xRange[0]) * SIZE[0] / (xRange[1] - xRange[0]),\
              SIZE[1] - (self.lastPos[1] - yRange[0]) * SIZE[1] / (yRange[1] - yRange[0])

        interpVal = interp(1 - animatingFrame / 60)

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

    for x in range(GRIDSIDELENGTH):
        for y in range(GRIDSIDELENGTH):
            c.hsva = ((x + y) / GRIDSIDELENGTH * 360 % 360, 100, 100, 0)
            xPos = x / GRIDSIDELENGTH * (xRange[1] - xRange[0]) + xRange[0]
            yPos = y / GRIDSIDELENGTH * (yRange[1] - yRange[0]) + yRange[0]
            pList.append(Particle((xPos, yPos), col=(c.r, c.g, c.b)))

    screen = pygame.display.set_mode(SIZE)

    c = pygame.time.Clock()

    while True:
        c.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and animating == 0:
                    for p in pList:
                        p.update()
                        animating = 60

        screen.fill((0, 0, 0))

        for p in pList:
            p.draw(screen, animating, animating=animating != 0)

        pygame.display.flip()

        print(animating)

        animating = max(animating - 1, 0)


if __name__ == '__main__':
    main()
