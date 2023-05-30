import pygame
import random
from time import sleep


S = [['....',
      '.00',
      '00.',
      '....',],
     ['0...',
      '00..',
      '.0..',]]

Z = [['....',
      '00..',
      '.00.',
      '....'],
     ['..0.',
      '.00.',
      '.0..',
      '....']]

I = [['..0.',
      '..0.',
      '..0.',
      '..0.',],
     ['.....',
      '0000',
      '.....',
      '.....',]
     ]

O = [['....',
      '.00.',
      '.00.',
      '....']]

J = [['....',
      '0...',
      '000.',
      '....',],
     ['.00.',
      '.0..',
      '.0..',
      '....'],
     ['.....',
      '000.',
      '..0.',
      '....'],
     ['.0..',
      '.0..',
      '00..',
      '....']]

L = [['....',
      '..0.',
      '000.',
      '....',],
     ['.0..',
      '.0..',
      '.00.',
      '....'],
     ['....',
      '000.',
      '0...',
      '....'],
     ['00..',
      '.0..',
      '.0..',
      '....']]

T = [['....',
      '.0..',
      '000.',
      '....',],
     ['.0..',
      '.00.',
      '.0..',
      '....'],
     ['....',
      '000.',
      '.0..',
      '....'],
     ['.0..',
      '00..',
      '.0..',
      '....']]

shapes_list = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# Initialize pygame
pygame.font.init()


# Set up the screen
s_width = 800
s_height = 700

# Game settings
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = (s_height - play_height)




class Score:
    def __init__(self):
        self.score = 0
        try:
            with open('scores.txt', 'r') as file:
                self.high_score = file.readline()
        except FileNotFoundError:
            with open('scores.txt', 'w') as file:
                file.write('0')
                self.high_score = '0'

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.rotation = 0
        self.shape = shape
        self.color = shape_colors[shapes_list.index(shape)]




def create_grid(locked_pos):
    # Create the game grid with locked positions
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) in locked_pos:
                c = locked_pos[(i, j)]
                grid[i][j] = c
    return grid

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))

def get_shape():
    # Get a random shape for the next piece
    return Piece(4, 0, random.choice(shapes_list))


def draw_grid(surface, grid,level,next_shape,shape,locked_pos):
    # Draw the game grid on the screen
    surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    font = pygame.font.SysFont('comicsans', 29)
    pause = font.render(f"Press P to pause", 1, (255, 255, 255))
    score_text = font.render(f"Score: {score.score}", 1, (255, 255, 255))
    level_text = font.render(f"Level: {level}", 1, (255, 255, 255))
    surface.blit(level_text, (550, 30))
    surface.blit(score_text, (20, 90))
    surface.blit(pause, (20, 180))
    surface.blit(label, (top_left_x + play_width / 2.5 - (label.get_width() / 2.5), 30))
    if len(score.high_score) > 5:
        font = pygame.font.SysFont('comicsans', 25)
    high_score = font.render(f"High Score: {score.high_score}", 1, (255, 255, 255))
    surface.blit(high_score, (20, 30))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30))
    # Draw grid and border
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)
    draw_lines(win, 10, 20)
    draw_next_shape(next_shape,win)
    shape_halo(grid,shape,locked_pos,win)
    pygame.display.update()


def draw_lines(surface, col, row):
    # Draw grid lines
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 228), (sx, sy + i * 30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 228), (sx + j * 30, sy), (sx + j * 30, sy + play_height))


def format_shape(shape,halo = None):
    # Format the shape for drawing and collision detection
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    if halo == None:
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
            
        return positions

    else:
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, halo + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0]-2 , pos[1])
        return positions


def clear_rows(grid: list, locked_pos,level):
    # Clear filled rows and update the score
    inc = 0
    score_inc = {
        0: 0,
        1: 100,
        2: 300,
        3: 500,
        4: 800
    }
    for i, row in enumerate(grid):
        if (0, 0, 0) not in row:
            pygame.mixer.Sound.play(clear_row_sound).set_volume(.2)
            new_locked = locked_pos.copy()
            inc += 1
            ind = i
            grid.pop(i)
            grid.insert(0, [(0, 0, 0) for _ in range(10)])
            for pos in new_locked:
                if pos[0] == ind:
                    del locked_pos[pos]
            new_locked = locked_pos.copy()
            end = {}
            for pos in new_locked:
                if pos[0] < ind:
                    end[(pos[0] + 1, pos[1])] = locked_pos.pop(pos)
                
                else:
                    end[pos] = locked_pos.pop(pos)
            
            locked_pos = end
    score.score += score_inc[inc] * level
    return locked_pos


def can_rotate(shape,locked_pos):
    # Check if the shape can rotate without colliding with other blocks
    for pos in shape:
    
        if pos[::-1] in locked_pos:
            pygame.mixer.Sound.play(cant_move).set_volume(.2)

            return False
        elif pos[0] < 0 or pos[0] > 9: 
            pygame.mixer.Sound.play(cant_move).set_volume(.2)
            return False


    return True

def check_lost(locked_pos):
    for pos in locked_pos:
        if pos[0] == 0:
            global running, paused
            running = False
            
            paused = True
            if score.score > int(score.high_score):
                with open('scores.txt', 'w') as file:
                    file.write(str(score.score))
            score.score = 0

def valid_space(shape1, command,locked_pos):
    # Check if the shape can move in the given direction without colliding with other blocks
    if type(command) == int:
        for position in shape1:
            if position[0] + command < 0 or position[0] + command > 9:
                pygame.mixer.Sound.play(cant_move)
                return False
            if (position[1], position[0] + command) in locked_pos:
                pygame.mixer.Sound.play(cant_move)
                return False
    elif command == 'down':
        for position in shape1:
            if position[1] + 1 > 19:
                return False
            elif (position[1] + 1, position[0]) in locked_pos:
                return False
    else:
        for position in shape1:
            if position[1] + 1 > 19:
                return False
            for pos in locked_pos:
                if (position[1] + 1, position[0]) in locked_pos and position[1] > pos[1]:
                    return False
        
    return True


def shape_halo(grid,shape,locked_pos,surface):
    #This shows where the piece is going to drop
    shape_poso = format_shape(shape)
    halo_y = 0 
    shape_pos = format_shape(shape,halo_y)

    can = True
    for pos in shape_poso:
        if pos[1] < 0:
            can = False
    if can:
        
        for i in grid:
            halo_y += 1

            if not valid_space(shape_pos, None, locked_pos):
                for pos in shape_pos:
                    if pos[1] > shape_poso[0][1]:
                        pygame.draw.rect(surface, shape.color, ((top_left_x + pos[0]*block_size), top_left_y + pos[1]*block_size, block_size, block_size), 2,6)

                break   

            else:
                shape_pos = format_shape(shape,halo_y)
    return grid            
   
    


def move_shape(tet: list,locked_pos,grid,shape):
    # Move the shape and check for collision or game over
    positions = []
    check_lost(locked_pos)

    for position in tet:
        if position[1] >= 20:

            for pos in tet:
                locked_pos.update({(pos[1]-1, pos[0]): shape.color})
            return False,locked_pos
        elif (position[1], position[0]) not in locked_pos:
            if position[1] > -1:
                
                grid[position[1]][position[0]] = shape.color
                positions.append([position[1], position[0]])
            else:
                positions.append([position[1], position[0]])
 
        else:

            for pos in tet:
                locked_pos.update({(pos[1]-1, pos[0]): shape.color})

            return (False,locked_pos)

    return (positions,locked_pos)

def hard_drop( locked_pos, shape, grid):
    #instantly drops the piece to as low as it can go
    shape_pos = format_shape(shape)
    can = True
    for pos in shape_pos:
        if pos[1] < 0:
            can = False
    if can:   
        for i in grid:
            shape.y += 1
            score.score += 2
            if not valid_space(shape_pos, 'down', locked_pos):
                shape_pos = format_shape(shape)
                move_shape(shape_pos, locked_pos, grid, shape)
                score.score -= 2
                break
            else:
                shape_pos = format_shape(shape)
        
    return can

    
def draw_next_shape(shape, surface):
    
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size))

    surface.blit(label, (sx + 10, sy - 30))



score = Score()

pygame.mixer.init()
cant_move = pygame.mixer.Sound('resources\sound/cant_move.mp3')
clear_row_sound = pygame.mixer.Sound('resources/sound/clear_row.mp3')


# Main game loop
def main(win): 
    global score,running,paused,halo_y
    shape = get_shape()

    
    next_shape = get_shape()
    locked_pos = {}
    fall_time = 0 
    end = False
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.load('resources/sound/Life-Blossom.mp3')
    pygame.mixer.music.play(-1)
    
    running = True
    fall_speed = 0.27
    level_time = 0
    level = 1
    paused = False
    clock = pygame.time.Clock()
    music = True
    
    
    while running:
        if not music:

            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
            
        while not paused:
   
            grid = create_grid(locked_pos)
            level_time += clock.get_rawtime()
            fall_time += clock.get_rawtime()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if valid_space(shape_pos, -1,locked_pos):
                            shape.x -= 1
                    if event.key == pygame.K_RIGHT:
                        if valid_space(shape_pos, +1,locked_pos):
                            shape.x += 1
                    if event.key == pygame.K_p:
                        paused = not paused
                    if event.key == pygame.K_SPACE:
                        new = hard_drop(locked_pos,shape,grid)
                        if new:
                            shape = next_shape
                            
                            sleep(.01)
                            next_shape = get_shape()
                    if event.key == pygame.K_DOWN:
                        score.score += 1
                        shape.y += 1
                        if not valid_space(shape_pos,'down',locked_pos):
                            shape.y -= 1
                    if event.key == pygame.K_UP:
                        shape.rotation +=1
                        if not can_rotate(format_shape(shape),locked_pos):
                            shape.rotation -= 1
                if event.type == pygame.QUIT:
                    paused = True
                    end = True
                    running = False
                   
                    if score.score > int(score.high_score):
                        with open('scores.txt', 'w') as file:
                            file.write(str(score.score))

            if level_time / 1000 > 20:
                fall_speed -= .03
                level_time = 0
                level += 1

            
            locked_pos = clear_rows(grid, locked_pos,level)
            shape_pos = format_shape(shape)
            
            success,locked_pos = move_shape(shape_pos,locked_pos,grid, shape)
            if not success:
                shape = next_shape
                sleep(.01)
                next_shape = get_shape()
            if fall_time / 1000 >= fall_speed:
                fall_time = 0
                shape.y += 1
                success,locked_pos  = move_shape(shape_pos,locked_pos,grid, shape)
                if not success:
                    shape = next_shape
                    
                    sleep(.01)
                    next_shape = get_shape()
            
            draw_grid(win, grid,level,next_shape,shape,locked_pos)
            
            pygame.display.set_caption(str(int(clock.get_fps())))
            
            pygame.display.update()
            
        #When the game in paused
        draw_text_middle(win,"Paused",150,(250,250,250))
        clock.tick(20)
    
        pygame.display.update()
        

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    
                if event.key == pygame.K_m:
                    music  = not music
                    
            if event.type == pygame.QUIT:
                end = True
                paused = True
                running = False
                

                if score.score > int(score.high_score):
                    with open('scores.txt', 'w') as file:
                        file.write(str(score.score))
    if not end:
        main_menu(win,'scoreYou Lost , Press Any Key To Play Again',38)

def main_menu(win,text,text_size):  # *
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, text , text_size, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
                run = False
    
    pygame.display.quit()

if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    main_menu(win,'Press Any Key To Play',60)
    pygame.quit()


