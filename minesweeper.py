import random
import pygame
import sys

size_x = 9
size_y = 9
total_mines = 15
SCALE = 50


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

STAT_WIDTH = 7
WINDOW_HEIGHT = SCALE*size_y + 2*SCALE + int(1.5*SCALE)
WINDOW_WIDTH = SCALE*size_x

pygame.init()
FONT = pygame.font.SysFont("Microsoft Yahei UI Light", int(SCALE/2))
FONT2 = pygame.font.SysFont("Microsoft Yahei UI Light", int(SCALE/2.5))
surface = pygame.Surface((40, 60))

STAT_RECT = pygame.Rect(0, 0, WINDOW_WIDTH, SCALE*2)
SETTINGS_RECT = surface.get_rect(x=0,y=SCALE*size_y + 2*SCALE,width= WINDOW_WIDTH, height = int(SCALE*1.8))
RESTART_RECT = surface.get_rect(width = int(9/4*SCALE), height = int(SCALE*1.5),center = STAT_RECT.center)
AI_RECT = surface.get_rect(width = int(9/4*SCALE), height = int(SCALE*1.5),centery = STAT_RECT.centery, centerx = STAT_RECT.centerx -3*SCALE)
AUTO_RECT = surface.get_rect(width = int(9/4*SCALE), height = int(SCALE*1.5),centery = STAT_RECT.centery, centerx = STAT_RECT.centerx +3*SCALE)


#INP_RECT_1 = pygame.Rect()

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
DARK = (34, 34, 34)
LIGHT = (51, 51, 51)
BLUE = (62, 83, 162)
GREEN = (41, 127, 62)
RED = (224, 30, 37)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
CLOCK = pygame.time.Clock()

width_input = InputBox(STAT_RECT.centerx-3*SCALE+int(SCALE/15), SETTINGS_RECT.centery-int(SCALE/2.5),int(SCALE*1.2), int(SCALE/1.5), text = str(size_x))
height_input = InputBox(STAT_RECT.centerx, SETTINGS_RECT.centery-int(SCALE/2.5),int(SCALE*1.2), int(SCALE/1.5), text = str(size_y))
mines_input = InputBox(STAT_RECT.centerx+3*SCALE-int(SCALE/15), SETTINGS_RECT.centery-int(SCALE/2.5),int(SCALE*1.2), int(SCALE/1.5), text = str(total_mines))

input_boxes = [width_input, height_input, mines_input]

def drawStats():
    global FONT, SCREEN, STAT_RECT, SETTINGS_RECT
    pygame.draw.rect(SCREEN, LIGHT, STAT_RECT)
    pygame.draw.rect(SCREEN, DARK, SETTINGS_RECT)
    surface = pygame.Surface((40, 60))
    
    RESTART_RECT = surface.get_rect(width = int(9/4*SCALE), height = int(SCALE*1.5),center = STAT_RECT.center)
    pygame.draw.rect(SCREEN, DARK, RESTART_RECT)
    restartLabel = FONT.render("Restart", 1, WHITE)
    SCREEN.blit(restartLabel, restartLabel.get_rect(center=RESTART_RECT.center))
    
    AI_RECT = surface.get_rect(width = int(9/4*SCALE), height = int(SCALE*1.5),centery = STAT_RECT.centery, centerx = STAT_RECT.centerx -3*SCALE)
    pygame.draw.rect(SCREEN, DARK, AI_RECT)
    aiLabel = FONT.render("AI OFF", 1, RED)
    SCREEN.blit(aiLabel, aiLabel.get_rect(center=AI_RECT.center))

    AUTO_RECT = surface.get_rect(width = int(9/4*SCALE), height = int(SCALE*1.5),centery = STAT_RECT.centery, centerx = STAT_RECT.centerx +3*SCALE)
    pygame.draw.rect(SCREEN, DARK, AUTO_RECT)
    autoLabel = FONT.render("Auto-solve", 1, BLUE)
    SCREEN.blit(autoLabel, autoLabel.get_rect(center=AUTO_RECT.center))

    SCREEN.blit(FONT2.render("Width", 1, WHITE), FONT.render("Width", 1, WHITE).get_rect(centery= SETTINGS_RECT.centery, right = SETTINGS_RECT.centerx - 3*SCALE))
    SCREEN.blit(FONT2.render("Height", 1, WHITE), FONT.render("Height", 1, WHITE).get_rect(centery= SETTINGS_RECT.centery, right = SETTINGS_RECT.centerx))
    SCREEN.blit(FONT2.render("Mines", 1, WHITE), FONT.render("Mines", 1, WHITE).get_rect(centery= SETTINGS_RECT.centery, right = SETTINGS_RECT.centerx + 3*SCALE))
    
    for box in input_boxes:
        box.draw(SCREEN)


def set_board(size_x, size_y, total_mines, first_x, first_y):
    board = [[0 for i in range(size_y)] for j in range(size_x)]

    def num(x, y):
        if x < 0 or x >= size_x or y < 0 or y >= size_y:  # out of range
            return
        if not board[x][y] == -1:
            board[x][y] += 1
        else:
            print('setnumber error', x, y, board[x][y])
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
    global SCREEN, CLOCK, SCALE, first_click, mines, size_x, size_y, total_mines
    SCREEN.fill(BLACK)

    while True:
        drawGrid()
        drawStats()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONUP and not SETTINGS_RECT.collidepoint(event.pos) and not STAT_RECT.collidepoint(event.pos):
                x, y = event.pos
                x, y = int(x/SCALE), int(y/SCALE)
                if first_click:
                    first_click = False
                    mines = set_board(size_x, size_y, total_mines, x, y-2)
                    click(x, y)
                elif event.button == 1:
                    click(x, y)
                elif event.button == 2:
                    middleClick(x,y)
                elif event.button == 3:
                    flag(x, y)
            if event.type == pygame.MOUSEBUTTONDOWN and RESTART_RECT.collidepoint(event.pos):
                reset()


        pygame.display.update()


def reset():
    global SCREEN, board, mines, first_click, size_x, size_y, total_mines, STAT_RECT, SETTINGS_RECT, input_boxes
    size_x = (int(width_input.text))
    size_y = (int(height_input.text))
    total_mines = int(mines_input.text)
    SCALE = 50
    first_click = True
    WINDOW_HEIGHT = SCALE*size_y + 2*SCALE + int(1.5*SCALE)
    WINDOW_WIDTH = SCALE*size_x
    print('reset')
    
    pygame.display.quit()

    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
    
    pygame.display.flip()
    board = [[0 for i in range(size_y)] for j in range(size_x)]
    mines = [[0 for i in range(size_y)] for j in range(size_x)]

    STAT_RECT = pygame.Rect(0, 0, WINDOW_WIDTH, SCALE*2)
    SETTINGS_RECT = surface.get_rect(x=0,y=SCALE*size_y + 2*SCALE,width= WINDOW_WIDTH, height = int(SCALE*1.8))
    width_input2 = InputBox(STAT_RECT.centerx-3*SCALE+int(SCALE/15), SETTINGS_RECT.centery-int(SCALE/2.5),int(SCALE*1.2), int(SCALE/1.5), text = str(size_x))
    height_input2 = InputBox(STAT_RECT.centerx, SETTINGS_RECT.centery-int(SCALE/2.5),int(SCALE*1.2), int(SCALE/1.5), text = str(size_y))
    mines_input2 = InputBox(STAT_RECT.centerx+3*SCALE-int(SCALE/15), SETTINGS_RECT.centery-int(SCALE/2.5),int(SCALE*1.2), int(SCALE/1.5), text = str(total_mines))

    input_boxes = [width_input2, height_input2, mines_input2]


def clickedMine(x, y):
    global board
    print('CLICKED MINE')
    board[x][y] = 1


def click(x, y):
    reveal(x, y-2, True)

def check(x,y):
    if x < 0 or x >= size_x or y < 0 or y >= size_y:  # out of range
        return
    return board[x][y]

def middleClick(x, y):
    y-=2
    if x < 0 or x >= size_x or y < 0 or y >= size_y:  # out of range
        return
    flags = [check(x+1,y),check(x-1,y),check(x,y+1),check(x,y-1),check(x+1,y+1),check(x+1,y-1),check(x-1,y-1),check(x-1,y+1)].count(-1)
    print(mines[x][y],[check(x+1,y),check(x-1,y),check(x,y+1),check(x,y-1),check(x+1,y+1),check(x+1,y-1),check(x-1,y-1),check(x-1,y+1)],flags)
    if flags == mines[x][y]:
        reveal(x+1,y),reveal(x-1,y),reveal(x,y+1),reveal(x,y-1),reveal(x+1,y+1),reveal(x+1,y-1),reveal(x-1,y-1),reveal(x-1,y+1)
        print('yay')

def flag(x, y):
    global board
    y-=2
    if board[x][y] == 1:
        return
    if board[x][y] == -1:
        board[x][y] = 0
    else:
        board[x][y] = -1


def reveal(x, y, first_click=False):
    global board
    if first_click:  # if mouseclick
        print('Clicked', x, y)
        if mines[x][y] == -1:
            clickedMine(x, y)
        elif mines[x][y]:
            board[x][y] = 1
        if mines[x][y] > 0:
            return

    if x < 0 or x >= size_x or y < 0 or y >= size_y:  # out of range
        return
    if board[x][y] == 1 or board[x][y] == -1:
        return
    if mines[x][y]:
        board[x][y] = 1
        return
    board[x][y] = 1
   # print('recurring')
    reveal(x-1, y), reveal(x+1, y), reveal(x, y+1), reveal(x, y-1), reveal(x -
                                                                           1, y-1), reveal(x+1, y+1), reveal(x-1, y+1), reveal(x+1, y-1)


def drawGrid():
    global board, SCALE  # Set the size of the grid block
    for x in range(0, SCALE*size_x, SCALE):
        for y in range(0, SCALE*size_y, SCALE):
            rect = pygame.Rect(x, y+2*SCALE, SCALE, SCALE)
            location = board[int(x/SCALE)][int(y/SCALE)]
            if location == 0:
                pygame.draw.rect(SCREEN, DARK, rect)
            elif location == 1:
                if mines[int(x/SCALE)][int(y/SCALE)] == -1:
                    pygame.draw.rect(SCREEN, RED, rect)
                elif mines[int(x/SCALE)][int(y/SCALE)] == 0:
                    pygame.draw.rect(SCREEN, LIGHT, rect)
                else:
                    pygame.draw.rect(SCREEN, LIGHT, rect)
                    number = mines[int(x/SCALE)][int(y/SCALE)]
                    colour = BLUE
                    if number == 2:
                        colour = GREEN
                    elif number == 3:
                        colour == RED
                    num = pygame.font.SysFont('Comic Sans', int(SCALE/2)).render(
                        str(mines[int(x/SCALE)][int(y/SCALE)]), True, colour)
                    num_rect = num.get_rect(center=rect.center)
                    SCREEN.blit(num, num_rect)
            else:
                pygame.draw.rect(SCREEN, DARK, rect)
                number = mines[int(x/SCALE)][int(y/SCALE)]
                colour = RED
                num = pygame.font.SysFont('Comic Sans', int(
                    SCALE/2)).render('F', True, colour)
                num_rect = num.get_rect(center=rect.center)
                SCREEN.blit(num, num_rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)  # outline


main()
