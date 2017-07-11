# coding:utf-8

import random
import sys
import pygame
from pygame.locals import *

'''
1:设置board大小是640*480
2:board中共有10*7个box
3:boxsize为40*40,gapsize为10
4:表示box用列表,共7行10列(0-9...0-6).第0行为(0,0)...(0,9),第6行为(6,0)...(6,9)
5:计算每个box与x轴y轴的距离,用来确定绘制box的具体坐标
6:定义一个列表来保存boxes的shape和color(列表为boxes[boxX][boxY]=(shape,color))
7:根据以上条件绘制好基本的board和boxes
8:在boxes上覆盖一层白色cover
9:再定义一个列表来保存boxes的揭开/覆盖状态,函数为revealed,若为True则为揭开,False为覆盖。默认全是False
10:获取鼠标点击事件,获取mouseX和mouseY
11:根据(mouseX,mouseY)获取(boxX,boxY),从而确定box
12:根据(boxX,boxY)获取box的shape和color
13:点击就将其揭开:
    1:实现揭开动画,若box是firstSelection,则firstSelection = (boxAX,boxAY)
    2:若此box不是firstSelection,则box为(boxBX,boxBY)
    3:对比boxes[boxAX][boxAY]与boxes[boxBX][boxBY]是否相等
    4:若相等,就判断是否获胜,若不相等,则将boxA的revealed状态设置为False,boxB的revealed状态设置为False。
       对boxA和boxB实现覆盖动画。
    5:无论是否匹配,都将firstSelection设置为None
14:游戏揭开动画,游戏覆盖动画,游戏开场动画,游戏获胜动画
'''
FPS = 30
BOARDWIDTH = 640
BOARDHEIGHT = 480
BOXSIZE = 40
GAPSIZE = 10
COUNTWIDTH = 8
COUNTHEIGHT = 6

assert COUNTWIDTH * COUNTHEIGHT % 2 == 0

# color RGB
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

ALLCOLORS = [RED, GREEN, BLUE, YELLOW]

# 设置背景色
BGCOLOR = NAVYBLUE
# 设置亮背景色
LIGHTBGCOLOR = GRAY
# 设置box的颜色
BOXCOLOR = WHITE
# 设置高亮颜色
HIGHLIGHTCOLOR = BLUE

# shape
DONUT = 'donut'  # 甜甜圈
SQUARE = 'square'  # 方形
DIAMOND = 'diamond'  # 钻石
LINES = 'lines'  # 多条线
OVAL = 'oval'  # 椭圆

ALLSHAPES = [DONUT, SQUARE, DIAMOND, LINES, OVAL]

assert len(ALLSHAPES) * len(ALLCOLORS) * 10 >= COUNTWIDTH * COUNTHEIGHT

boxes = []
for i in range(COUNTWIDTH):
    for j in range(COUNTHEIGHT):
        boxes.append((i, j))
boxesCoords = [boxes[i:i + COUNTHEIGHT] for i in range(0, len(boxes), COUNTHEIGHT)]

# print(boxesCoords)
# print(len(boxesCoords))
# print(type(boxesCoords))
# print(boxes)
# print(len(boxes))

XMARGIN = int((BOARDHEIGHT - (COUNTHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((BOARDWIDTH - (COUNTWIDTH * (BOXSIZE + GAPSIZE))) / 2)

# print('xmargin value: %s' % (XMARGIN))
# print('ymargin value: %s' % (YMARGIN))


def getLeftTop(box):
    (boxX, boxY) = box
    top = boxX * (BOXSIZE + GAPSIZE) + XMARGIN
    left = boxY * (BOXSIZE + GAPSIZE) + YMARGIN

    return (top, left)


# (top, left) = getLeftTop((0, 0))
# print((top, left))
# (top, left) = getLeftTop((0, 1))
# print((top, left))
# (top, left) = getLeftTop((1, 0))
# print((top, left))


def generateBoxReveal(val):
    boxreveals = []
    for i in range(COUNTWIDTH):
        boxreveals.append([val] * COUNTHEIGHT)
    return boxreveals

boxreveals = generateBoxReveal(False)

# print('boxreveals data: %s' % (boxreveals))
# print('boxreveals type: %s' % (type(boxreveals)))
# print('boxreveals length: %s' % (len(boxreveals)))


def getBoxReveal(box):
    # boxreveals[1][0] = True
    (boxX, boxY) = box
    boxreveal = boxreveals[boxX][boxY]
    return boxreveal


def setBoxReveal(box, boxstatus):
    if box in boxes:
        (boxX, boxY) = box
        boxreveals[boxX][boxY] = boxstatus


# box = (1,0)
# gbr = getBoxReveal(box)
# print(gbr)


def generateShapeColor(allshapes, allcolors):
    result = []
    for shape in allshapes:
        for color in allcolors:
            result.append((shape, color))
    random.shuffle(result)
    result = result[:COUNTHEIGHT] * COUNTWIDTH
    random.shuffle(result)
    boxshapecolor = [result[i:(i + COUNTHEIGHT)] for i in range(0, len(boxes), COUNTHEIGHT)]
    return boxshapecolor


# 每个元素代表box的元组(shape,color)
gsc = generateShapeColor(ALLSHAPES, ALLCOLORS)
# print('gsc value: %s' % (gsc))
# print('gsc length: %s' % (len(gsc)))
# print('gsc type: %s' % (type(gsc)))


def getBoxShapeColor(box):
    if box in boxes:
        shape, color = gsc[box[0]][box[1]]
    return (shape, color)


# gbsc = getBoxShapeColor((7,5))
# print('gbsc value: (%s,%s)' % (gbsc))


def drawBoxShapeColor(box):
    half = int(BOXSIZE * 0.5)
    quarter = int(BOXSIZE * 0.25)

    (top, left) = getLeftTop(box)
    pygame.draw.rect(DISPLAYSURF, WHITE, (top, left, BOXSIZE, BOXSIZE))

    (shape, color) = getBoxShapeColor(box)
    if shape == DONUT:  # 甜甜圈
        pygame.draw.circle(DISPLAYSURF, color, (top + half, left + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (top + half, left + half), quarter - 5)
    elif shape == SQUARE:  # 方形
        pygame.draw.rect(DISPLAYSURF, color, (top + quarter, left + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:  # 钻石
        pygame.draw.polygon(DISPLAYSURF, color, (
            (top, left + half), (top + half, left + BOXSIZE - 1), (top + BOXSIZE - 1, left + half,),
            (top + half, left)))
    elif shape == LINES:  # 多条线
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (top + i, left), (top, left + i))
            pygame.draw.line(DISPLAYSURF, color, (top + BOXSIZE - 1, left + i), (top + i, left + BOXSIZE - 1))
    elif shape == OVAL:  # 椭圆
        # pygame.draw.ellipse(DISPLAYSURF, color, (top + quarter, left, BOXSIZE, half))
        pygame.draw.ellipse(DISPLAYSURF, color, (top, left + quarter, BOXSIZE, half))


def drawBoxCover(box):
    (boxX, boxY) = box
    (top, left) = getLeftTop(box)
    pygame.draw.rect(DISPLAYSURF, WHITE, (top, left, BOXSIZE, BOXSIZE))


def drawBoard():
    for box in boxes:
        drawBoxShapeColor(box)
        if not getBoxReveal(box):
            (top, left) = getLeftTop(box)
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (top, left, BOXSIZE, BOXSIZE))
        else:
            pass


def getBoxFromMouse(mousepos):
    mouseX, mouseY = mousepos
    for box in boxes:
        top, left = getLeftTop(box)
        boxRect = pygame.Rect(top, left, BOXSIZE, BOXSIZE)
        if boxRect.collidepoint(mouseX, mouseY):
            return box
    return None


def checkWin(boxreveals):
    for i in boxreveals:
        if False in i:
            return False
    return True


def winAnimation():
    boxreveals = generateBoxReveal(True)
    color1 = NAVYBLUE
    color2 = GRAY
    for i in range(8):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard()
        pygame.display.flip()
        pygame.time.wait(300)
    fontObj = pygame.font.Font('/usr/share/fonts/liberation/LiberationMono-Bold.ttf', 50)
    textSurfObj = fontObj.render('Congratulations!', True, RED, GREEN)
    textRectObj = textSurfObj.get_rect()
    textRectObj.center = (BOARDWIDTH/2, BOARDHEIGHT/2)
    pygame.time.wait(3000)
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfObj, textRectObj)


def startAnimation():
    boxes = []
    for i in range(COUNTWIDTH):
        for j in range(COUNTHEIGHT):
            boxes.append((i, j))
    boxesCoords = [boxes[i:i + COUNTHEIGHT] for i in range(0, len(boxes), COUNTHEIGHT)]

    BOXES = boxes
    random.shuffle(BOXES)
    BOXESCOORDS = [BOXES[i:i + COUNTHEIGHT] for i in range(0, len(BOXES), COUNTHEIGHT)]
    for i in BOXESCOORDS:
        for j in i:
            drawBoxShapeColor(j)
            pygame.display.flip()
            pygame.time.wait(100)
            drawBoxCover(j)
        pygame.time.wait(100)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((BOARDWIDTH, BOARDHEIGHT))
DISPLAYSURF.fill(NAVYBLUE)
pygame.display.set_caption('MemoryGame')
FPSCLOCK = pygame.time.Clock()

startAnimation()
drawBoard()
# drawBoxCover(boxes)
# BOX = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)]
# for box in BOX:
#     drawBoxShapeColor(box)

# for box in boxes:
#     drawBoxShapeColor(box)


firstSelection = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # elif event.type == MOUSEMOTION:
        #     mousepos = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousepos = event.pos
            box = getBoxFromMouse(mousepos)
            if box:
                print('box pos: ', box)
                setBoxReveal(box, True)

                print('drawboxshapecolor: ', box)
                print('start draw shapecolor')
                drawBoxShapeColor(box)
                print('end draw shapecolor')
                # 此处得加上自动更新，否则第二个box出不来
                pygame.display.flip()
                print('start wait 3s')
                pygame.time.wait(300)
                print('end wait 3s')

                if firstSelection is None:
                    firstSelection = box
                    firstShapeColor = getBoxShapeColor(firstSelection)
                    print('firstSelection: ', firstSelection)
                    print('firstSelection shapeColor: ', firstShapeColor)
                elif firstSelection is not None:
                    (boxX, boxY) = box
                    if firstSelection != box:
                        secondShapeColor = getBoxShapeColor(box)
                        print('Second: ', box)
                        print('Second shapeColor: ', secondShapeColor)

                        print('start judge first second')
                        if firstShapeColor == secondShapeColor:
                            print('match...')
                            if checkWin(boxreveals):
                                winAnimation()

                        elif firstShapeColor != secondShapeColor:
                            print('not match')
                            drawBoxShapeColor(box)
                            pygame.time.wait(300)
                            drawBoxCover(firstSelection)
                            setBoxReveal(firstSelection, False)
                            drawBoxCover(box)
                            setBoxReveal(box, False)
                        print('end judge first second')
                    elif firstSelection == box:
                        drawBoxCover(box)
                    firstSelection = None
    pygame.display.flip()