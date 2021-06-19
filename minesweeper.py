import random
import pygame

size_x = 10
size_y = 10
total_mines = 5
blockSize = 20

WINDOW_HEIGHT = 20*size_y
WINDOW_WIDTH = 20*size_x
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()


def set_board(size_x, size_y, total_mines, first_x, first_y):
    board = [[0 for i in range(size_y)] for j in range(size_x)]

    def num(x, y):
        if x < 0 or x >= size_x or y < 0 or y >= size_y:  # out of range
            return
        if not board[x][y] == -1:
            board[x][y] += 1
        else:
            print('setnumber error', x, y)
    counter = total_mines
    while counter > 0:
        x, y = random.randint(1, size_x)-1, random.randint(1, size_y)-1
        if board[x][y] == 0 and not (x == first_x and y == first_y):
            board[x][y] = -1
            counter -= 1
    for j in range(size_y):
        for i in range(size_x):
            if board[i][j] == -1:
                num(i+1, j), num(i-1, j), num(i, j+1), num(i, j-1)
                num(i+1, j-1), num(i-1, j+1), num(i+1, j+1), num(i-1, j-1)
    print(board)
    if not board[first_x][first_y] == 0:
        return set_board(size_x, size_y, total_mines, first_x, first_y)
    return board


board = [[0 for i in range(size_y)] for j in range(size_x)]
mines = [[0 for i in range(size_y)] for j in range(size_x)]

first_click = True


def main():
    global SCREEN, CLOCK, blockSize, first_click, mines
    pygame.init()
    SCREEN.fill(BLACK)

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                x, y = int(x/blockSize), int(y/blockSize)
                if first_click:
                    first_click = False
                    mines = set_board(size_x, size_y, total_mines, x, y)
                    click(x, y)
                elif event.button == 1:
                    click(x, y)
                elif event.button == 3:
                    flag(x, y)

        pygame.display.update()


def clickedMine(x, y):
    global board
    print('CLICKED MINE')
    board[x][y] = -1


def click(x, y):
    reveal(x, y, True)


def flag(x, y):
    board[x][y] = -1


def reveal(x, y, first_click=False):
    global board
    if first_click:  # if mouseclick
        print('Clicked', x, y)
        if mines[x][y] == -1:
            clickedMine(x, y)
        elif mines[x][y]:
            board[x][y] = 1
    if x < 0 or x >= size_x or y < 0 or y >= size_y:  # out of range
        return
    if board[x][y] == 1:
        return
    if mines[x][y]:
        board[x][y] = 1
        return
    board[x][y] = 1
   # print('recurring')
    reveal(x-1, y), reveal(x+1, y), reveal(x, y+1), reveal(x, y-1)


def drawGrid():
    global board
    blockSize = 20  # Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            location = board[int(x/blockSize)][int(y/blockSize)]
            if location == 0:
                pygame.draw.rect(SCREEN, BLACK, rect, 1)
            elif location == 1:
                if mines[int(x/blockSize)][int(y/blockSize)] == -1:
                    pygame.draw.rect(SCREEN, RED, rect, 1)
                elif mines[int(x/blockSize)][int(y/blockSize)] == 0:
                    pygame.draw.rect(SCREEN, WHITE, rect)
                else:
                    pygame.draw.rect(SCREEN, GREEN, rect, 1)
                    num = pygame.font.SysFont('Arial', 10).render(
                        str(mines[int(x/blockSize)][int(y/blockSize)]), True, WHITE)
                    num_rect = num.get_rect(center=rect.center)
                    SCREEN.blit(num, num_rect)
            else:
                pygame.draw.rect(SCREEN, GREEN, rect, 1)
                num = pygame.font.SysFont('Arial', 10).render('F', True, WHITE)
                num_rect = num.get_rect(center=rect.center)
                SCREEN.blit(num, num_rect)


main()
