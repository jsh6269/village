import pygame
from pygame.transform import rotozoom

win = pygame.display.set_mode((2048//2, 1408//2))
win.fill((255, 255, 255))
bg = rotozoom(pygame.image.load('./img/ground.png').convert(), 0, 1)
win.blit(bg, (-2048//2, 0))
pygame.display.update()

pygame.mixer.init(buffer=128)
pygame.init()
clock = pygame.time.Clock()


class rect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        with open('rect_design(오른쪽 위).txt', 'a') as f:
            f.write('({}, {}, {}, {}),\n'.format(x1, y1, x2, y2))

    def draw_rect(self):
        pygame.draw.rect(win, (0, 0, 0), [self.x1, self.y1, self.x2-self.x1, self.y2-self.y1])


class triangle:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        with open('tri_design(오른쪽 위).txt', 'a') as f:
            f.write('({}, {}, {}, {}, {}, {}),\n'.format(x1, y1, x2, y2, x3, y3))

    def draw_rect(self):
        pygame.draw.polygon(win, (0, 0, 0), [[self.x1, self.y1], [self.x2, self.y2], [self.x3, self.y3]])


rectLst = []
shell = []


def redraw():
    win.blit(bg, (-2048//2, 0))
    for rectangle in rectLst:
        rectangle.draw_rect()


run = True

pre = []

while run:
    clock.tick(48)
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            shell.append(mouse[0])
            shell.append(mouse[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                del rectLst[-1]
                ori = None
                with open('rect_design(오른쪽 위).txt', 'r') as f:
                    ori = f.readlines()
                with open('rect_design(오른쪽 위).txt', 'w') as f:
                    for line in ori[:-1]:
                        f.write(line)
    if len(shell) == 4:
        rectLst.append(rect(shell[0], shell[1], shell[2], shell[3]))
        shell = []
    redraw()
    for rec in pre:
        rec.draw_rect()
    pygame.display.update()

