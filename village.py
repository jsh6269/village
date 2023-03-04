import pygame
from pygame.transform import rotozoom, flip

# initialize
bg_mag = 2.1
size = width, height = int(2048 * bg_mag), int(1408 * bg_mag)
a, b = width//4, height//4
win = pygame.display.set_mode((a, b))
winX, winY = None, None
midX, midY = a//2, b//2
change = True
mag = 1.8
vel = 5 # running velocity of hero
cating = None
cutoff = True

npc_block = [[393, 64, 471, 109]]

bg = rotozoom(pygame.image.load('./img/ground.png').convert(), 0, bg_mag)
motion = {'left': [rotozoom(pygame.image.load('./img/left1.png'), 0, mag),
                   rotozoom(pygame.image.load('./img/left2.png'), 0, mag),
                   rotozoom(pygame.image.load('./img/left3.png'), 0, mag),
                   rotozoom(pygame.image.load('./img/left4.png'), 0, mag),
                   rotozoom(pygame.image.load('./img/left5.png'), 0, mag)],
          'right': [rotozoom(flip(pygame.image.load('./img/left1.png'), True, False), 0, mag),
                    rotozoom(flip(pygame.image.load('./img/left2.png'), True, False), 0, mag),
                    rotozoom(flip(pygame.image.load('./img/left3.png'), True, False), 0, mag),
                    rotozoom(flip(pygame.image.load('./img/left4.png'), True, False), 0, mag),
                    rotozoom(flip(pygame.image.load('./img/left5.png'), True, False), 0, mag)],
          'up': [rotozoom(pygame.image.load('./img/up1.png'), 0, mag),
                 rotozoom(pygame.image.load('./img/up2.png'), 0, mag),
                 rotozoom(pygame.image.load('./img/up3.png'), 0, mag),
                 rotozoom(pygame.image.load('./img/up4.png'), 0, mag),
                 rotozoom(pygame.image.load('./img/up5.png'), 0, mag)],
          'down': [rotozoom(pygame.image.load('./img/down1.png'), 0, mag),
                   rotozoom(pygame.image.load('./img/down2.png'), 0, mag),
                   rotozoom(pygame.image.load('./img/down3.png'), 0, mag),
                   rotozoom(pygame.image.load('./img/down4.png'), 0, mag),
                   rotozoom(pygame.image.load('./img/down5.png'), 0, mag)]
          }
npc1 = rotozoom(pygame.image.load('./img/잠만보.png'), 0, 0.8)

win.fill((255, 255, 255))
x, y = 132, 234
win.blit(bg, (0, 0))
pygame.display.update()

pygame.mixer.init(buffer=128)
pygame.init()
clock = pygame.time.Clock()


count = 0
pre = 'down'
# 리스트의 2번째 인자는 key가 눌렸는지 여부를 저장함. 수시로 바뀜
keySet = {'left': [pygame.K_LEFT, None],
          'right': [pygame.K_RIGHT, None],
          'up': [pygame.K_UP, None],
          'down': [pygame.K_DOWN, None],
          'tool': [pygame.K_a, None],
          'menu': [pygame.K_s, None],
          'dash': [pygame.K_z, None],
          'interact': [pygame.K_x, None]
          }


def press(*command):
    # string 타입의 기술 이름을 받아 해당 키가 눌려져 있는지 확인
    # 변수가 하나면 bool 타입으로 반환, 여러개면 bool 로 구성된 리스트를 반환
    ans = [keySet[cmd][1] for cmd in command]
    if len(ans) == 1:
        return ans[0]
    return ans


def form():
    # x와 y좌표를 점검해 캐릭터가 화면 밖으로 나가지 않도록 한다.
    global x, y
    if x < 18:
        x = 18
    if x > width - 22:
        x = width - 22
    if y < 22:
        y = 22
    if y > height - 25:
        y = height - 25


def possible(xx, yy):
    for a, b, c, d in npc_block:

        if (xx * bg_mag >= a and xx * bg_mag <= c) or (xx * bg_mag >= c and xx * bg_mag <= a):
            if (yy * bg_mag >= b and yy * bg_mag <= d) or (yy * bg_mag >= d and yy * bg_mag <= b):
                return False

    with open('rect_design(왼쪽 위).txt', 'r') as f:
        k = f.readlines()
        for item in k:
            it = item[1:-3].split(', ')
            a, b, c, d = int(it[0]), int(it[1]), int(it[2]), int(it[3])
            if (xx >= a and xx <= c) or (xx >= c and xx<= a):
                if (yy >= b and yy <= d) or (yy >= d and yy<= b):
                    return True

    with open('tri_design(왼쪽 위).txt', 'r') as f:
        k = f.readlines()
        for item in k:
            it = item[1:-3].split(', ')
            a, b, c, d, e, f = int(it[0]), int(it[1]), int(it[2]), int(it[3]), int(it[4]), int(it[5])

            alpha = ((d - f)*(xx - e) + (e - c)*(yy - f)) / ((d - f)*(a - e) + (e - c)*(b - f))
            beta = ((f - b)*(xx - e) + (a - e)*(yy - f)) / ((d - f)*(a - e) + (e - c)*(b - f))
            gamma = 1.0 - alpha - beta
            if alpha > 0 and beta > 0 and gamma > 0:
                return True
    return False


def go(cmd):
    global x, y, cating
    tempx, tempy = 0, 0
    # 벽에 맞기 좀더 전에 막히도록 하는게 자연스러운 듯
    stricterVal = 20 - vel
    new_x, new_y = x, y
    if cmd == 'left':
        new_x -= vel
        tempx -= stricterVal
    elif cmd == 'right':
        new_x += vel
        tempx += stricterVal
    elif cmd == 'up':
        new_y -= vel
        tempy -= stricterVal
    elif cmd == 'down':
        new_y += vel
        tempy += stricterVal

    # if possible((new_x + 25 * mag / 2) / bg_mag, (new_y + 31 * mag / 2) / bg_mag):
    if cmd == 'up' or gradual(new_x, tempx, new_y, tempy, cmd):
        if possible(new_x / bg_mag, new_y / bg_mag):
            x = new_x
            y = new_y
    cating = cmd


def gradual(nx, tx, ny, ty, cmd):
    if cmd == 'left' or cmd == 'right':
        ny = ny + 10
        if cmd == 'left':
            tx = tx + 25
    for ttx in range(tx+1):
        for tty in range(ty+1):
            if not possible((nx + ttx) / bg_mag, (ny + tty) / bg_mag):
                return False
    return True


def status_check():
    global x, y
    global pre, count, change
    import random

    key_state = pygame.key.get_pressed()
    for key in keySet:
        data = keySet[key]
        data[1] = key_state[data[0]]

    lst = [x for x in ['left', 'right', 'up', 'down'] if press(x)]
    if len(lst) == 0:
        count = 0
        hero = motion[pre][0]
        change = True
        
    elif len(lst) > 1:
        if pre in lst and not change:
            go(pre)
            count = (count + 1) % 18
            hero = motion[pre][count//6 + 1]
            change = False
        elif pre in lst and change:
            lst.remove(pre)
            newDirection = random.sample(lst, 1)[0]
            pre = newDirection
            go(newDirection)
            count = 0
            hero = motion[pre][count//6 + 1]
            change = False
        else:
            newDirection = random.sample(lst, 1)[0]
            pre = newDirection
            go(newDirection)
            count = 0
            hero = motion[pre][count//6 + 1]
            change = True

    else:
        if press(pre):
            count = (count + 1) % 18
        else:
            count = 0
            
        pre = lst[0]
        hero = motion[pre][count//6 + 1]
        go(lst[0])
        change = True

    form()
    # adjustment
    cx, cy = midX, midY
    if x < midX:
        cx = x
    if y < midY:
        cy = y
    if x > width - width//4 + midX:
        cx = x - (width - width//4)
    if y > height - height//4 + midY:
        cy = y - (height - height//4)

    if pre == 'up' and len(lst) != 0:
        win.blit(hero, (cx-25*mag/2, cy-31*mag/2 + 3))
    else:
        win.blit(hero, (cx-25*mag/2, cy-31*mag/2))


def check_mouse():
    global x, y
    mouse = pygame.mouse.get_pos()
    font = pygame.font.Font('Noto-Black.otf', 30)
    text = font.render("mouse: ({}, {})".format(-winX+mouse[0], -winY+mouse[1]), True, (230, 230, 230), (0, 0, 0))
    text2 = font.render("character: ({}, {})".format(x, y), True, (230, 230, 230), (0, 0, 0))
    win.blit(text, (50, 80))
    win.blit(text2, (50, 40))


def redraw():
    global winX, winY
    winX, winY = midX - x, midY - y
    if winX > 0:
        winX = 0
    if winX < -width * 3 / 4:
        winX = -width * 3 / 4
    if winY > 0:
        winY = 0
    if winY < -height * 3 / 4:
        winY = -height * 3 / 4
    win.blit(bg, (winX, winY))
    draw_npc()
    status_check()
    check_mouse()


def draw_npc():
    ex1 = (188*bg_mag+winX, 25*bg_mag+winY)
    win.blit(npc1, ex1)
    # if cating == 'up' and y == 114 and 397 <= x and x<= 457:
    #     if press('interact'):
    #     # npc1과 대화할 조건


run = True

while run:
    clock.tick(48)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    redraw()
    if 2120 < x and 129 < y and y < 210 and cutoff:
        if cating == 'right':
            gg = rotozoom(pygame.image.load('./img/gg.png'), 0, 1)
            win.blit(gg, (0, 0))
            pygame.display.update()
            import time
            time.sleep(5)
            cutoff = False

    pygame.display.update()


pygame.quit()
