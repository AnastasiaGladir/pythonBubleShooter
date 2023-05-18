import math, pygame, sys, copy, random
import pygame.gfxdraw
from pygame.locals import *
import pygame_menu
from pygame_menu import themes


FPS = 120
WINDOWWIDTH = 700
WINDOWHEIGHT = 500
TEXTHEIGHT = 20
BUBBLERADIUS = 17
BUBBLEWIDTH = BUBBLERADIUS * 2
BUBBLELAYERS = 5
BUBBLEYADJUST = 5
STARTX = WINDOWWIDTH / 2
STARTY = WINDOWHEIGHT - 27
ARRAYWIDTH = 21
ARRAYHEIGHT = 14

RIGHT = 'right'
LEFT = 'left'
BLANK = '.'

## COLORS ##

#            R    G    B
white = ((255,255,255))
blue = ((0,0,255))
green = ((0,255,0))
red = ((255,0,0))
black = ((0,0,0))
orange = ((255,100,10))
yellow = ((255,255,0))
blue_green = ((0,255,170))
marroon = ((115,0,0))
lime = ((180,255,100))
pink = ((255,100,180))
purple = ((240,0,255))
gray = ((127,127,127))
magenta = ((255,0,230))
brown = ((100,40,0))
forest_green = ((0,50,0))
navy_blue = ((0,0,100))
rust = ((210,150,75))
dandilion_yellow = ((255,200,0))
highlighter = ((255,255,100))
sky_blue = ((0,255,255))
light_gray = ((200,200,200))
dark_gray = ((50,50,50))
tan = ((230,220,170))
coffee_brown =((200,190,140))
moon_glow = ((235,245,255))

BGCOLOR = purple
COLORLIST = [sky_blue,magenta, moon_glow,blue_green,dandilion_yellow]


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
BackGround = Background('picture_fon.jpg', [0,0])



class Bubble(pygame.sprite.Sprite):
    def __init__(self, color, row=0, column=0):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.centerx = STARTX
        self.rect.centery = STARTY
        self.speed = 10
        self.color = color
        self.radius = BUBBLERADIUS
        self.angle = 0
        self.row = row
        self.column = column

    def update(self):

        if self.angle == 90:
            xmove = 0
            ymove = self.speed * -1
        elif self.angle < 90:
            xmove = self.xcalculate(self.angle)
            ymove = self.ycalculate(self.angle)
        elif self.angle > 90:
            xmove = self.xcalculate(180 - self.angle) * -1
            ymove = self.ycalculate(180 - self.angle)

        self.rect.x += xmove
        self.rect.y += ymove

    def draw(self):
        pygame.gfxdraw.filled_circle(DISPLAYSURF, self.rect.centerx, self.rect.centery, self.radius, self.color)
        pygame.gfxdraw.aacircle(DISPLAYSURF, self.rect.centerx, self.rect.centery, self.radius, dark_gray)

    def xcalculate(self, angle):
        radians = math.radians(angle)

        xmove = math.cos(radians) * (self.speed)
        return xmove

    def ycalculate(self, angle):
        radians = math.radians(angle)

        ymove = math.sin(radians) * (self.speed) * -1
        return ymove


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.angle = 90
        image = pygame.image.load('pushka.png')
        image.convert_alpha()
        DEFAULT_IMAGE_SIZE = (50, 50)
        image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)
        image = pygame.transform.rotate(image, 270)
        arrowRect = image.get_rect()
        self.image = image
        self.transformImage = self.image
        self.rect = arrowRect
        self.rect.centerx = STARTX
        self.rect.centery = STARTY

    def update(self, direction):

        if direction == LEFT and self.angle < 180:
            self.angle += 2
        elif direction == RIGHT and self.angle > 0:
            self.angle -= 2

        self.transformImage = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.transformImage.get_rect()
        self.rect.centerx = STARTX
        self.rect.centery = STARTY

    def draw(self):
        DISPLAYSURF.blit(self.transformImage, self.rect)


class Score(object):
    def __init__(self):
        self.total = 0
        self.font = pygame.font.SysFont('Helvetica', 15)
        self.render = self.font.render('Score: ' + str(self.total), True, black, moon_glow)
        self.rect = self.render.get_rect()
        self.rect.left = 5
        self.rect.bottom = WINDOWHEIGHT - 5

    def update(self, deleteList):
        self.total += ((len(deleteList)) * 10)
        self.render = self.font.render('Score: ' + str(self.total), True, black, moon_glow)

    def draw(self):
        DISPLAYSURF.blit(self.render, self.rect)


def main():
    global FPSCLOCK, DISPLAYSURF, DISPLAYRECT, MAINFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Puzzle Bobble')
    MAINFONT = pygame.font.SysFont('Helvetica', TEXTHEIGHT)
    DISPLAYSURF, DISPLAYRECT = makeDisplay()

    while True:
        score, winorlose = runGame()
        endScreen(score, winorlose)


def runGame():
    musicList = ['Music1.mp3', 'Music2.mp3', 'Music3.mp3']
    pygame.mixer.music.load(musicList[0])
    pygame.mixer.music.play()
    track = 0
    gameColorList = copy.deepcopy(COLORLIST)
    direction = None
    launchBubble = False
    newBubble = None

    arrow = Arrow()
    bubbleArray = makeBlankBoard()
    setBubbles(bubbleArray, gameColorList)

    nextBubble = Bubble(gameColorList[0])
    nextBubble.rect.right = WINDOWWIDTH - 5
    nextBubble.rect.bottom = WINDOWHEIGHT - 5

    score = Score()

    while True:
        DISPLAYSURF.fill([255, 255, 255])
        DISPLAYSURF.blit(BackGround.image, BackGround.rect)


        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if (event.key == K_LEFT):
                    direction = LEFT
                elif (event.key == K_RIGHT):
                    direction = RIGHT

            elif event.type == KEYUP:
                direction = None
                if event.key == K_SPACE:
                    launchBubble = True
                elif event.key == K_ESCAPE:
                    terminate()

        if launchBubble == True:
            if newBubble == None:
                newBubble = Bubble(nextBubble.color)
                newBubble.angle = arrow.angle

            newBubble.update()
            newBubble.draw()

            if newBubble.rect.right >= WINDOWWIDTH - 5:
                newBubble.angle = 180 - newBubble.angle
            elif newBubble.rect.left <= 5:
                newBubble.angle = 180 - newBubble.angle

            launchBubble, newBubble, score = stopBubble(bubbleArray, newBubble, launchBubble, score)

            finalBubbleList = []
            for row in range(len(bubbleArray)):
                for column in range(len(bubbleArray[0])):
                    if bubbleArray[row][column] != BLANK:
                        finalBubbleList.append(bubbleArray[row][column])
                        if bubbleArray[row][column].rect.bottom > (WINDOWHEIGHT - arrow.rect.height - 50):
                            return score.total, 'lose'

            if len(finalBubbleList) < 1:
                return score.total, 'win'

            gameColorList = updateColorList(bubbleArray)
            random.shuffle(gameColorList)

            if launchBubble == False:
                nextBubble = Bubble(gameColorList[0])
                nextBubble.rect.right = WINDOWWIDTH - 5
                nextBubble.rect.bottom = WINDOWHEIGHT - 5

        nextBubble.draw()
        if launchBubble == True:
            coverNextBubble()

        arrow.update(direction)
        arrow.draw()

        setArrayPos(bubbleArray)
        drawBubbleArray(bubbleArray)

        score.draw()

        if pygame.mixer.music.get_busy() == False:
            if track == len(musicList) - 1:
                track = 0
            else:
                track += 1

            pygame.mixer.music.load(musicList[track])
            pygame.mixer.music.play()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeBlankBoard():
    array = []

    for row in range(ARRAYHEIGHT):
        column = []
        for i in range(ARRAYWIDTH):
            column.append(BLANK)
        array.append(column)

    return array


def setBubbles(array, gameColorList):
    for row in range(BUBBLELAYERS):
        for column in range(len(array[row])):
            random.shuffle(gameColorList)
            newBubble = Bubble(gameColorList[0], row, column)
            array[row][column] = newBubble

    setArrayPos(array)


def setArrayPos(array):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].rect.x = (BUBBLEWIDTH * column) + 5
                array[row][column].rect.y = (BUBBLEWIDTH * row) + 5

    for row in range(1, ARRAYHEIGHT, 2):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].rect.x += BUBBLERADIUS

    for row in range(1, ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].rect.y -= (BUBBLEYADJUST * row)

    deleteExtraBubbles(array)


def deleteExtraBubbles(array):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                if array[row][column].rect.right > WINDOWWIDTH:
                    array[row][column] = BLANK


def updateColorList(bubbleArray):
    newColorList = []

    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[0])):
            if bubbleArray[row][column] != BLANK:
                newColorList.append(bubbleArray[row][column].color)

    colorSet = set(newColorList)

    if len(colorSet) < 1:
        colorList = []
        colorList.append(moon_glow)
        return colorList

    else:

        return list(colorSet)


def checkForFloaters(bubbleArray):
    bubbleList = [column for column in range(len(bubbleArray[0]))
                  if bubbleArray[0][column] != BLANK]

    newBubbleList = []

    for i in range(len(bubbleList)):
        if i == 0:
            newBubbleList.append(bubbleList[i])
        elif bubbleList[i] > bubbleList[i - 1] + 1:
            newBubbleList.append(bubbleList[i])

    copyOfBoard = copy.deepcopy(bubbleArray)

    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[0])):
            bubbleArray[row][column] = BLANK

    for column in newBubbleList:
        popFloaters(bubbleArray, copyOfBoard, column)


def popFloaters(bubbleArray, copyOfBoard, column, row=0):
    if (row < 0 or row > (len(bubbleArray) - 1)
            or column < 0 or column > (len(bubbleArray[0]) - 1)):
        return

    elif copyOfBoard[row][column] == BLANK:
        return

    elif bubbleArray[row][column] == copyOfBoard[row][column]:
        return

    bubbleArray[row][column] = copyOfBoard[row][column]

    if row == 0:
        popFloaters(bubbleArray, copyOfBoard, column + 1, row)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row)
        popFloaters(bubbleArray, copyOfBoard, column, row + 1)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row + 1)

    elif row % 2 == 0:
        popFloaters(bubbleArray, copyOfBoard, column + 1, row)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row)
        popFloaters(bubbleArray, copyOfBoard, column, row + 1)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row + 1)
        popFloaters(bubbleArray, copyOfBoard, column, row - 1)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row - 1)

    else:
        popFloaters(bubbleArray, copyOfBoard, column + 1, row)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row)
        popFloaters(bubbleArray, copyOfBoard, column, row + 1)
        popFloaters(bubbleArray, copyOfBoard, column + 1, row + 1)
        popFloaters(bubbleArray, copyOfBoard, column, row - 1)
        popFloaters(bubbleArray, copyOfBoard, column + 1, row - 1)


def stopBubble(bubbleArray, newBubble, launchBubble, score):
    deleteList = []
    popSound = pygame.mixer.Sound('pop_buble.ogg')

    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[row])):

            if (bubbleArray[row][column] != BLANK and newBubble != None):
                if (pygame.sprite.collide_rect(newBubble, bubbleArray[row][column])) or newBubble.rect.top < 0:
                    if newBubble.rect.top < 0:
                        newRow, newColumn = addBubbleToTop(bubbleArray, newBubble)

                    elif newBubble.rect.centery >= bubbleArray[row][column].rect.centery:

                        if newBubble.rect.centerx >= bubbleArray[row][column].rect.centerx:
                            if row == 0 or (row) % 2 == 0:
                                newRow = row + 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn

                            else:
                                newRow = row + 1
                                newColumn = column + 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn

                        elif newBubble.rect.centerx < bubbleArray[row][column].rect.centerx:
                            if row == 0 or row % 2 == 0:
                                newRow = row + 1
                                newColumn = column - 1
                                if newColumn < 0:
                                    newColumn = 0
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                            else:
                                newRow = row + 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn


                    elif newBubble.rect.centery < bubbleArray[row][column].rect.centery:
                        if newBubble.rect.centerx >= bubbleArray[row][column].rect.centerx:
                            if row == 0 or row % 2 == 0:
                                newRow = row - 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                            else:
                                newRow = row - 1
                                newColumn = column + 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn

                        elif newBubble.rect.centerx <= bubbleArray[row][column].rect.centerx:
                            if row == 0 or row % 2 == 0:
                                newRow = row - 1
                                newColumn = column - 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn

                            else:
                                newRow = row - 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn

                    popBubbles(bubbleArray, newRow, newColumn, newBubble.color, deleteList)

                    if len(deleteList) >= 3:
                        for pos in deleteList:
                            popSound.play()
                            row = pos[0]
                            column = pos[1]
                            bubbleArray[row][column] = BLANK
                        checkForFloaters(bubbleArray)

                        score.update(deleteList)

                    launchBubble = False
                    newBubble = None

    return launchBubble, newBubble, score


def addBubbleToTop(bubbleArray, bubble):
    posx = bubble.rect.centerx
    leftSidex = posx - BUBBLERADIUS

    columnDivision = math.modf(float(leftSidex) / float(BUBBLEWIDTH))
    column = int(columnDivision[1])

    if columnDivision[0] < 0.5:
        bubbleArray[0][column] = copy.copy(bubble)
    else:
        column += 1
        bubbleArray[0][column] = copy.copy(bubble)

    row = 0
    return row, column


def popBubbles(bubbleArray, row, column, color, deleteList):
    if row < 0 or column < 0 or row > (len(bubbleArray) - 1) or column > (len(bubbleArray[0]) - 1):
        return

    elif bubbleArray[row][column] == BLANK:
        return

    elif bubbleArray[row][column].color != color:
        return

    for bubble in deleteList:
        if bubbleArray[bubble[0]][bubble[1]] == bubbleArray[row][column]:
            return

    deleteList.append((row, column))

    if row == 0:
        popBubbles(bubbleArray, row, column - 1, color, deleteList)
        popBubbles(bubbleArray, row, column + 1, color, deleteList)
        popBubbles(bubbleArray, row + 1, column, color, deleteList)
        popBubbles(bubbleArray, row + 1, column - 1, color, deleteList)

    elif row % 2 == 0:

        popBubbles(bubbleArray, row + 1, column, color, deleteList)
        popBubbles(bubbleArray, row + 1, column - 1, color, deleteList)
        popBubbles(bubbleArray, row - 1, column, color, deleteList)
        popBubbles(bubbleArray, row - 1, column - 1, color, deleteList)
        popBubbles(bubbleArray, row, column + 1, color, deleteList)
        popBubbles(bubbleArray, row, column - 1, color, deleteList)

    else:
        popBubbles(bubbleArray, row - 1, column, color, deleteList)
        popBubbles(bubbleArray, row - 1, column + 1, color, deleteList)
        popBubbles(bubbleArray, row + 1, column, color, deleteList)
        popBubbles(bubbleArray, row + 1, column + 1, color, deleteList)
        popBubbles(bubbleArray, row, column + 1, color, deleteList)
        popBubbles(bubbleArray, row, column - 1, color, deleteList)


def drawBubbleArray(array):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].draw()


def makeDisplay():
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYRECT = DISPLAYSURF.get_rect()
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.convert()
    pygame.display.update()

    return DISPLAYSURF, DISPLAYRECT


def terminate():
    pygame.quit()
    sys.exit()


def coverNextBubble():
    whiteRect = pygame.Rect(0, 0, BUBBLEWIDTH, BUBBLEWIDTH)
    whiteRect.bottom = WINDOWHEIGHT
    whiteRect.right = WINDOWWIDTH
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, whiteRect)


def endScreen(score, winorlose):
    endFont = pygame.font.SysFont('Helvetica', 20)
    endMessage1 = endFont.render('You ' + winorlose + '! Your Score is ' + str(score) + '. Press Enter to Play Again.',
                                 True, black, BGCOLOR)
    endMessage1Rect = endMessage1.get_rect()
    endMessage1Rect.center = DISPLAYRECT.center

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(endMessage1, endMessage1Rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_RETURN:
                    return
                elif event.key == K_ESCAPE:
                    terminate()


pygame.init()
surface = pygame.display.set_mode((600, 400))

def start_the_game():
    mainmenu._open(loading)
    main()

mainmenu = pygame_menu.Menu('Welcome', 600, 400, theme=themes.THEME_BLUE)
mainmenu.add.text_input('Name: ', default='username')
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)


loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id="1", default=0, width=200, )

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

update_loading = pygame.USEREVENT + 0

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
        if event.type == pygame.QUIT:
            exit()

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())

    pygame.display.update()

