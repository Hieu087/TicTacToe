# AUTHOR: Trần Trung Hiếu
# STUDENT ID: 51703086

import pygame
import random
import time
from math import inf
from pygame.locals import *

# SYMBOLS CHOOSING
symbols = ['X', 'O']
humanSym = input('Choose your symbol (X,O): ').upper()

if humanSym != symbols[0] and humanSym != symbols[1]:
    humanSym = input('Not right! Please choose again (X,O): ').upper()
    
if humanSym != symbols[0] and humanSym != symbols[1]:
    print('You choose wrong again. Your symbol will be X')
    humanSym = symbols[0]

compSym = [symbol for symbol in symbols if symbol != humanSym][0]

# GENERATE 20x20 GIRD 
grid = [['_' for _ in range(20)] for _ in range(20)]
def showGrid():
    global grid
    for row in range(len(grid)):
        for col in range(len(grid)):
            if col == len(grid)-1:
                print(grid[row][col])
            else:
                print(grid[row][col], end=' | ')

# GENERATE 20x20 BOARD IN GAME
def initBoard(displayGame):
    board = pygame.Surface (displayGame.get_size())
    board = board.convert()
    board.fill((250, 250, 250))

    # DRAW GRID LINE
    # VERTICAL LINES
    for i in range(1, len(grid)+1):
        pygame.draw.line(board, (0,0,0), (i*50, 0), (i*50, 1000), 2)

    # HORIZONTAL LINES
    for i in range(1, len(grid)+1):
        pygame.draw.line(board, (0,0,0), (0, i*50) , (1000, i*50) , 2)

    return board

# SHOW BOARD IN GAME
def showBoard (gameDisplay, board):
    gameDisplay.blit(board, (0, 0))
    pygame.display.flip()

# SHOW STATUS 
def showStatus (board, message):
    # RENDER STATUS 
    font = pygame.font.Font(None, 35)
    text = font.render(message, 1, (0, 0, 0))

    # PIN THE RENDERED STATUS ON THE BOARD
    board.fill((250, 250, 0), (1002, 0, 150, 1000))
    board.blit(text, (1010, 500))

# DETERMINE THE POSITIONS
def boardPos(mouseX, mouseY):
    for i in range(len(grid)):
        if mouseY < i * 50 + 50:
            row = i
            break

    for i in range(len(grid)):
        if mouseX < i * 50 + 50:
            col = i
            break

    return (row, col)

# DRAW SYMBOLS
def drawSym(board, row, col, sym):
    global grid

    # DETERMINE THE CENTER OF SQUARE
    centerX = col * 50 + 25
    centerY = row * 50 + 25

    # DRAW SYMBOLs
    if (sym == 'O'):
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 15, 1)
    else:
        pygame.draw.line (board, (0,0,0), (centerX - 11, centerY - 11), (centerX + 11, centerY + 11), 2)
        pygame.draw.line (board, (0,0,0), (centerX + 11, centerY - 11), (centerX - 11, centerY + 11), 2)

    grid[row][col] = sym

# RETURN A LIST OF AVAILABLE POSITIONS
def availPos():
    global grid
    pos = []
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == '_':
                pos.append([row, col])
    return pos

# APPEND EVERY PATHS
def appendPath():
    global grid
    pentaSet = []
     # APPEND EVERY ROWS
    for row in range(len(grid)):
        pentaSet.append(grid[row])

    # APPEND EVERY COLUMNS
    for col in range(len(grid)):
        pentaSet.append([grid[row][col] for row in range(len(grid))])
    
    # APPEND EVERY DIAGONAL
    for t in range(len(grid)-4):
        pentaSet.append([grid[i][i+t] for i in range(len(grid) - t)])
    for t in range(1, len(grid)-4):
        pentaSet.append([grid[i+t][i] for i in range(len(grid) - t)])

    for t in range(len(grid)-1, 3, -1):
        pentaSet.append([grid[i][t-i] for i in range(t + 1)])
    for t in range(len(grid)-5):
        pentaSet.append([grid[len(grid)-i][i+t] for i in range(1,len(grid)-t)])
    return pentaSet

# CHECK IF THERE'RE A WINNER
def winner(sym):
    pathSet = appendPath()
    # CHECK IF THERE ARE 5 CONSECCUTIVE SYMBOLS IN ANY PATHS
    for path in pathSet:
        count = 0
        for s in path:
            if sym == s:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
    return False

# FINISH THE GAME WHEN THERE'S A WINNER
def gameOver():
    return winner(humanSym) or winner(compSym)

# SHOW RESULTS
def gameEnd(board):
    if winner(humanSym):
        showStatus(board, 'You win !')
    elif winner(compSym):
        showStatus(board, 'You lose !')
    else:
        showStatus(board, 'Draw !')

# RETURN THE OPPOSITE SYMBOL OF THE GIVEN SYMBOL
def oppositeSym(symbol):
    if symbol == humanSym:
        return compSym
    return humanSym

def isIn(grid, y, x):
    return 0 <= y < len(grid) and 0 <= x < len(grid)

# FIND THE FAREST POSITION IN DY, DX IN RANGE OF LENGTH
def checkPos(grid,y,x,dy,dx,length):
    yf = y + length*dy 
    xf = x + length*dx
    
    while not isIn(grid,yf,xf):
        yf -= dy
        xf -= dx   
    return yf,xf

# INITIALIZE THE POINT SYSTEM
def scoreReady(scores):
    sumSym = {0: {},1: {},2: {},3: {},4: {},5: {},-1: {}}
    for key in scores:
        for score in scores[key]:
            if key in sumSym[score]:
                sumSym[score][key] += 1
            else:
                sumSym[score][key] = 1
            
    return sumSym

# MERGE POINTS OF EACH DIRECTION
def sumValues(sumSym):
    for key in sumSym:
        if key == 5:
            sumSym[5] = int(1 in sumSym[5].values())
        else:
            sumSym[key] = sum(sumSym[key].values())

def score_of_list(lis, col):
    blank = lis.count('_')
    filled = lis.count(col)
    
    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled

# RETURN LIST OF Y,X FROM YF, XF
def row_to_list(grid,y,x,dy,dx,yf,xf):
    row = []
    while y != yf + dy or x !=xf + dx:
        row.append(grid[y][x])
        y += dy
        x += dx
    return row

# RETURN A LIST WITH EACH ELEMENT REPRESENTING THE SCORE OF 5
def score_of_row(grid,cordi,dy,dx,cordf,sym):
    symScores = []
    y,x = cordi
    yf,xf = cordf
    row = row_to_list(grid,y,x,dy,dx,yf,xf)
    for start in range(len(row)-4):
        score = score_of_list(row[start:start+5],sym)
        symScores.append(score)
    return symScores

# REUTRN THE SCORE OF COLUMN IN Y, X IN 4 DIRECTIONS
def score_of_col_one(grid,col,y,x):
    # key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    
    scores[(0,1)].extend(score_of_row(grid,checkPos(grid,y,x,0,-1,4), 0, 1, checkPos(grid,y,x,0,1,4), col))
    
    scores[(1,0)].extend(score_of_row(grid,checkPos(grid,y,x,-1,0,4), 1, 0, checkPos(grid,y,x,1,0,4), col))
    
    scores[(1,1)].extend(score_of_row(grid,checkPos(grid,y,x,-1,-1,4), 1, 1, checkPos(grid,y,x,1,1,4), col))

    scores[(-1,1)].extend(score_of_row(grid,checkPos(grid,y,x,-1,1,4), 1,-1, checkPos(grid,y,x,1,-1,4), col))
    
    return scoreReady(scores)

# RETURN THE CASE SURELY WIN (4 CONSECCUTIVE SYMBOLS)
def danger(score3, score4):
    for key4 in score4:
        if score4[key4] >=1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >=2:
                    return True
    return False

# RETURN THE WINNING SITUATION
def winningSituation(sumSym):
    if 1 in sumSym[5].values():
        return 5
    elif len(sumSym[4])>=2 or (len(sumSym[4])>=1 and max(sumSym[4].values())>=2):
        return 4
    elif danger(sumSym[3],sumSym[4]):
        return 4
    else:
        score3 = sorted(sumSym[3].values(),reverse = True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0

# TRY TO MOVE Y,X 
# RETURN THE ADVANTAGE SCORE
def minimax(Sym, oppoSym, y, x):
    global grid

    M = 1000
    res, adv, dis = 0, 0, 0

    # ATTACK
    grid[y][x] = Sym
    sumSym = score_of_col_one(grid,Sym,y,x)    
    a = winningSituation(sumSym)
    adv += a * M
    sumValues(sumSym)
    adv +=  sumSym[-1] + sumSym[1] + 4*sumSym[2] + 8*sumSym[3] + 16*sumSym[4]
    
    # DEFEND
    grid[y][x] = oppoSym
    sumOppoSym = score_of_col_one(grid,oppoSym,y,x)
    d = winningSituation(sumOppoSym)
    dis += d * (M-100)
    sumValues(sumOppoSym)
    dis += sumOppoSym[-1] + sumOppoSym[1] + 4*sumOppoSym[2] + 8*sumOppoSym[3] + 16*sumOppoSym[4]

    res = adv + dis
    
    grid[y][x] = '_'

    return res

# INITIALIZE LIST OF COORDIANTES FOR COMPUTER
def availPos_forCom(grid):  
    # TAKEN: SAVE THE NON-AVAILABLE POSITIONS
    taken = []

    # DIRECTIONS: SAVE THE DIRECTIONS (8 DIRECTIONS)
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]

    # CORD: SAVE THE NO GO DIRECTIONS
    cord = {}
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != '_':
                taken.append((i,j))

    for direction in directions:
        dy,dx = direction
        for cord1 in taken:
            y,x = cord1
            for length in [1,2]:
                move = checkPos(grid,y,x,dy,dx,length)
                if move not in taken and move not in cord:
                    cord[move] = False
    return cord

#COMPUTER TURN
def compTurn(board):
    global compSym, grid

    showStatus(board, 'Your turn...')

    # WHEN COM ALLOWED TO GO FIRST
    if len(availPos()) == len(grid)**2:
        rdm = [i for i in range(int(len(grid)/2)-2, int(len(grid)/2)+2)]
        pos = [random.choice(rdm), random.choice(rdm)]
        drawSym(board, pos[0], pos[1], compSym)

    else:            
        pos = (0,0)
        maxScore = ''

        # MINIMAX 
        moves = availPos_forCom(grid)
        for move in moves:
            y,x = move
            if maxScore == '':
                score = minimax(humanSym, oppositeSym(humanSym), y, x)
                maxScore = score
                pos = move
            else:
                score = minimax(humanSym, oppositeSym(humanSym), y, x)
                if score > maxScore:
                    maxScore = score
                    pos = move
        
        drawSym(board, pos[0], pos[1], compSym)

#HUMAN TURN
sym = humanSym
def humanTurn(board, mode):
    global humanSym, sym

    if mode == 1:
        showStatus(board, 'Com turn...')
    
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (row, col) = boardPos(mouseX, mouseY)
    
        if [row, col] not in availPos():
            humanTurn(board, 1)

        drawSym(board, row, col, humanSym)

    else:
        if sym == humanSym:
            showStatus(board, 'P2 turn...')
        else:
            showStatus(board, 'P1 turn...')
    
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (row, col) = boardPos(mouseX, mouseY)
    
        if [row, col] not in availPos():
            humanTurn(board, 2)

        drawSym(board, row, col, sym)
        sym = oppositeSym(sym)
        


def main():
    global humanSym

    pygame.init()
    gameDisplay = pygame.display.set_mode ((1150, 1000))
    pygame.display.set_caption ('Tic-Tac-Toe')

    # CREATE THE GAME'S BOARD
    board = initBoard (gameDisplay)

    running = True
    
    # SELECT GAME MODE
    print('-------------')
    print('P vs Com (1)')
    print('P vs P   (2)')
    playMode = input('Slect game mode (1 or 2): ')

    if playMode == '1':    
        # TURN: USE TO DETERMINE WHOSE TURN TO PLAY (FALSE => HUMAN, TRUE => COMPUTER)
        turn = False
        first = input('Do you want to go first? (Y/N): ').upper()
        if first != 'Y':
            turn = True

    print('-------DONT CHOOSE THE TAKEN POSITIONS !!-------')

    while (running):
        for event in pygame.event.get():
            if event.type is QUIT:
                running = False

            else:
                # P VS COM
                if playMode == '1':
                    if first == 'Y':
                        # HUMAN GO FIRST
                        if event.type is MOUSEBUTTONDOWN and gameOver() != True:
                            humanTurn(board, 1)
                            if len(availPos()) == 0 or gameOver():
                                gameEnd(board)
                                break
                            turn = True

                        elif turn and gameOver() != True:
                            time.sleep(1)
                            compTurn(board)
                            turn = False
                            if len(availPos()) == 0 or gameOver():
                                gameEnd(board)
                                break
                    else:
                        # COMPUTER GO FIRST
                        if turn and gameOver() != True:
                            time.sleep(1)
                            compTurn(board)
                            turn = False
                            if len(availPos()) == 0 or gameOver():
                                gameEnd(board)
                                break

                        elif event.type is MOUSEBUTTONDOWN and gameOver() != True:
                            humanTurn(board, 1)
                            if len(availPos()) == 0 or gameOver():
                                gameEnd(board)
                                break
                            turn = True
                
                # P VS P
                else:
                    if event.type is MOUSEBUTTONDOWN and gameOver() != True:
                        humanTurn(board, 2)
                        if len(availPos()) == 0 or gameOver():
                            if winner(humanSym):
                                showStatus(board, 'P1 win !')
                            else:
                                showStatus(board, 'P2 win !')
                            break

            showBoard(gameDisplay, board)

main()