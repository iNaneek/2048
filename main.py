import pygame
import random
from copy import deepcopy

printableMat = [ #defines the matrix, printed out instead of automated for testing
        [0, 0, 0, 0], #for simplicity, these are presented to player are 2^x
        [0, 0, 0, 0], #so a 128 on the board is a 7 and 2048 is an 11
        [0, 0, 0, 0], #this makes logic simpler to handle
        [0, 0, 0, 0]
    ]

#refrenceMat = 0 #redefined later, but refrenced in functions

pygame.init()
screen = pygame.display.set_mode((820, 820))
pygame.display.set_caption('2048')
clock = pygame.time.Clock()
testFont = pygame.font.Font(None, 85)
background = pygame.Surface((820, 820))
background.fill((42, 42, 42))#sets up the window
running = True #when set as false, the window closes. used in whileloop further down

def getGameStatus(mat): #determines if game is over or not, not yet implemented
    for y in range(4):
        for x in range(4):
            if mat[y][x] == 0: #if any 0 is found then the game is still in progress
                return 1


def twoOrFour(): #this returns a 2 or a 4, because when a move is made, a four has a 20% chance to appear
    number = random.randint(1, 5)
    if number == 1:
        return 2 #prints 4
    else:
        return 1 #prints 2

def newNumberOnMat(mat): #imput a matrix, and replace a random 0 with a 1 or a 2, uses previous funtion
    print('new')
    while True:
        rand1 = random.randint(0, 3)
        rand2 = random.randint(0, 3)
        if mat[rand1][rand2] == 0:
            mat[rand1][rand2] = twoOrFour()
            break
    return mat

def transpose4x4Mat(matTranspose):
    matTranspose2 = []
    for i in range(4):
        matTranspose2.append([])
        for j in range(4):
            matTranspose2[i].append(matTranspose[j][i])
    return matTranspose2

def shift(shiftRow):
    #this function takes a 4 integer row and takes out all 0s and then adds the 0s again
    #for example: input[0,2,0,2] and get an output of [2,2,0,0]
    #this is neccissary for the next function
    shiftRowReturn = [] #makes a second list used to add elements in the new order
    blanks = 0 #acts as a counter and re adds this many 0s
    for i in range(4):
        if shiftRow[i] == 0: blanks = blanks + 1
        else: shiftRowReturn.append(shiftRow[i])
    for i in range(blanks):shiftRowReturn.append(0)
    return shiftRowReturn

def compile(compileRowInput):
    compileRow = compileRowInput.copy()
    #for example input=[1,2,0,2] and then output=[1,3,0,0] (for pushing left only)
    for i in range(3): #3 is the perfect number bc it combines numbers for [1,1,0,0] [0,1,1,0] and [0,0,1,1]
        compileRow = shift(compileRow)
        if (compileRow[i] != 0) and (compileRow[i] == compileRow[i + 1]):
            compileRow[i + 1] = 0
            compileRow[i] = compileRow[i] + 1
    return compileRow





def compileMat(compileFuncMat):
    for i in range(4):
        compileFuncMat[i] = compile(compileFuncMat[i])
    return compileFuncMat


def left(leftMatTemp):
    leftMatTemp = compileMat(leftMatTemp)
    return leftMatTemp


def right(rightMatTemp):
    for i in range(4):
        rightMatTemp[i].reverse()
        rightMatTemp[i] = compile(rightMatTemp[i])
        rightMatTemp[i].reverse()
    return rightMatTemp

def up(upMatTemp):
    upMatTemp = transpose4x4Mat(upMatTemp)
    upMatTemp = left(upMatTemp)
    upMatTemp = transpose4x4Mat(upMatTemp)
    return upMatTemp

def down(downMatTemp):
    downMatTemp = transpose4x4Mat(downMatTemp)
    downMatTemp = right(downMatTemp)
    downMatTemp = transpose4x4Mat(downMatTemp)
    return downMatTemp



def compareMatrixes(mat1, mat2):
    for i in range(4):
        for j in range(4):
            if mat1[i][j] != mat2[i][j]:
                return True
    print('MOVE NOT POSSIBLE')
    return False


setOfPrintableNumbers = [
    testFont.render(' ', False, (255, 255, 255)),
    testFont.render('2', False, (255, 255, 255)),
    testFont.render('4', False, (255, 255, 255)),
    testFont.render('8', False, (255, 255, 255)),
    testFont.render('16', False, (255, 255, 255)),
    testFont.render('32', False, (255, 255, 255)),
    testFont.render('64', False, (255, 255, 255)),
    testFont.render('128', False, (255, 255, 255)),
    testFont.render('256', False, (255, 255, 255)),
    testFont.render('512', False, (255, 255, 255)),
    testFont.render('1024', False, (0, 255, 255)),
    testFont.render('2048', False, (42, 42, 42)),
    testFont.render('4096', False, (255, 255, 255))
]

colors = [
    (20, 20, 20),
          (191, 255, 0), (64, 255, 0), (0, 255, 255),
          (0, 191, 255), (0, 64, 255), (128, 0, 255),
          (255, 0, 255), (255, 0, 0), (255, 128, 0),
          (255, 255, 0), (255, 255, 255), (0, 0, 0)]

def placement(numberIn): # for positioning of a number in the squares. just centers them
    if numberIn >= 10:
        return 21
    if numberIn >= 7:
        return 40
    if numberIn >= 4:
        return 60
    else:
        return 77

def makeASquare(squareX, squareY, squareNumber): #makes a square with rounded corners, +a color and number
    pygame.draw.rect(screen, colors[squareNumber], ((squareX, squareY + 40), (180, 100))) #two squares are used to
    pygame.draw.rect(screen, colors[squareNumber], ((squareX + 40, squareY), (100, 180))) #leave the corners open
    pygame.draw.circle(screen, colors[squareNumber], (squareX + 40, squareY + 40), 40) #4 cirlces used, one for each corner
    pygame.draw.circle(screen, colors[squareNumber], (squareX + 140, squareY + 40), 40)
    pygame.draw.circle(screen, colors[squareNumber], (squareX + 40, squareY + 140), 40)
    pygame.draw.circle(screen, colors[squareNumber], (squareX + 140, squareY + 140), 40)

    screen.blit(setOfPrintableNumbers[squareNumber], (squareX + placement(squareNumber), squareY + 64)) #this adds text

printableMat = newNumberOnMat(printableMat[:])
printableMat = newNumberOnMat(printableMat[:])
while running:
    refrenceMat = deepcopy(printableMat)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #exit()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                printableMat = newNumberOnMat(printableMat[:])

            if keys[pygame.K_a] or keys[pygame.K_LEFT]: #left
                print('left')
                printableMat = left(printableMat[:])
                if compareMatrixes(printableMat[:], refrenceMat[:]):
                    printableMat = newNumberOnMat(printableMat[:])

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]: #right
                print('right')
                printableMat = right(printableMat)
                if compareMatrixes(printableMat, refrenceMat):
                    printableMat = newNumberOnMat(printableMat[:])

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                print('up')
                printableMat = up(printableMat)
                if compareMatrixes(printableMat, refrenceMat):
                    printableMat = newNumberOnMat(printableMat[:])

            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                print('down')
                printableMat = down(printableMat)
                if compareMatrixes(printableMat, refrenceMat):
                    printableMat = newNumberOnMat(printableMat[:])

            print(printableMat)

    #start adding to screen
    screen.blit(background, (0, 0))
    #pygame.draw.rect(win, color[1], ()

    for x in range(4):
        for y in range(4):
            #screen.blit(setOfPrintableNumbers[printableMat[y][x]], (x*150+10, y*100))
            makeASquare(200 * x + 20, 200 * y + 20, printableMat[y][x])


    pygame.display.update()
    clock.tick(60)
    #print('frame')