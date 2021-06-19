import random
import pygame


size_x = 10
size_y = 10
total_mines = 15
blockSize = 20

WINDOW_HEIGHT = 20*size_y
WINDOW_WIDTH = 20*size_x
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

def set_board(size_x, size_y, total_mines):
    board =  [[0 for i in range(size_y)] for j in range(size_x)]
    while total_mines >0:
        x,y = random.randint(1,size_x)-1,random.randint(1,size_y)-1
        if board[x][y] == 0:
            board[x][y] = -1
            total_mines -= 1
    for j in range(size_y):
        for i in range(size_x):
            if board[i][j] == -1:
                if i+1<size_x:
                    board[i+1][j]+=1
                if i-1>=0:
                    board[i-1][j]+=1 
                if j+1<size_y:
                    board[i][j+1]+=1
                if j-1>=0:
                    board[i][j-1]+=1

    print(board)
    return board

mines = set_board(size_x, size_y, total_mines)
board =  [[0 for i in range(size_y)] for j in range(size_x)]


def main():
    global SCREEN, CLOCK, blockSize
    pygame.init()
    SCREEN.fill(BLACK)

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x, y = int(x/blockSize), int(y/blockSize)
                print('Clicked',x,y)
                reveal(x,y)


        pygame.display.update()

print(mines,mines[1][2])


def clickedMine(x,y):
    global board
    board[y][x] = -1
    print('CLICKED MINE')

def reveal(x,y):
    global board
    board[y][x] = 1


def drawGrid():
    global board
    blockSize = 20 #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            location = board[int(y/blockSize)][int(x/blockSize)]
            if location== 0:
                pygame.draw.rect(SCREEN, BLACK, rect)
            elif location == 1:
                if mines[int(y/blockSize)][int(x/blockSize)]==-1:
                    pygame.draw.rect(SCREEN, RED, rect)
                elif mines[int(y/blockSize)][int(x/blockSize)]==0:
                    pygame.draw.rect(SCREEN, WHITE, rect)
                else:
                    pygame.draw.rect(SCREEN, GREEN, rect)
            else:
                print('else?')

main()