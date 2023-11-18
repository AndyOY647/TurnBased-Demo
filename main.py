import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid

"""

pygame.font.init()

# GLOBALS VARS
s_width = 768
s_height = 768
play_width = 640  # meaning 300 // 10 = 30 width per block
play_height = 640  # meaning 600 // 20 = 20 height per block
block_size = 64

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

LL = [['.....',
      '.....',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..0..',
      '.....']]

L = [['.....',
      '.....',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '...0.',
      '.....',
      '.....'],
     ['.....',
      '...0.',
      '..00.',
      '.....',
      '.....']]



shapes = [L,LL]
shape_colors = [(0, 255, 0), (255, 0, 0)]


# index 0 - 1 represent shape
# Only 2 shapes


class Piece(object):
    row = 10
    col = 10

    def __init__(self,x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    # creates a black 10 by 10 grid
    grid = [[(0,0,0) for i in range(10)]for i in range(20)]

    for row in range(len(grid)):
        for col in range(len(grid)):
            if(col, row) in locked_positions:
                c = locked_positions[(col,row)]
                grid[row][col] = c
    return grid

def convert_shape_format(shape):
    positions = []
    # Getting the sublist for each rotation
    format = shape.shape[shape.rotation % len(shape.shape)]

    # Checking every line
    for i, line  in  enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x +j, shape.y + i))

    for i , pos in enumerate(positions):
        # offset shape left and up
        positions[i] = pos[0] - 2, pos[1] - 4

    return positions




def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(10)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    global shapes, shape_colors

    return Piece(1,0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, row, col):
    # start_pos x, y
    sx = top_left_x
    sy = top_left_y

    # Grid lines
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size))
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx+ j *block_size, sy), (sx + j* block_size , sy + play_height))





def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface, grid):
    row = 10
    col = 10
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('Grand9K Pixel', 50)
    label = font.render('KillTrash', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
    # boarder for grid
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, row, col)
    pygame.display.update()

def main(win):
    lock_positions = {}
    grid = create_grid(lock_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.40

    while run:
        grid = create_grid(lock_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        #Music here
        #################
        if fall_time /1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid) and current_piece.y > 0):
                current_piece.y -= 1
                change_piece = True


        #Key press check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                #Left
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    #check boarder
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                #Right
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                #Down
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece,grid)):
                        current_piece.y -= 1
                #UP
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                lock_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

        draw_window(win, grid)
        if check_lost(lock_positions):
            run = False

    pygame.display.quit()
def main_menu(win):
    main(win)

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('KillTrash')
main_menu(win)  # start game