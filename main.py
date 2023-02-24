import pygame

# init the pygame --> Mandatory
pygame.init()

WIDTH = 800
HEIGHT = 800
GOAT_COUNT =0
GOAT_DEAD =0
# create the screen
screen = pygame.display.set_mode((WIDTH,HEIGHT)) # w * h


#set title and icon
pygame.display.set_caption("Baagchaal")
# icon = pygame.image.load('xyz.png')
# pygame.display.set_icon(icon)



# Define board dimensions
board_size =600
board_x = (WIDTH - board_size) // 2
board_y = (HEIGHT - board_size) // 2

# Define line and circle properties
line_width = 5
line_color = (255, 255, 255)


from collections import defaultdict
board_points_pos = defaultdict(tuple)
h = 100
pos = 1
for row in range(5):
    w = 100
    if row != 0:
        h += (board_size//4)
    for col in range(5):
        if col != 0:
            w += (board_size//4)
        board_points_pos[pos] = (w,h)
        pos +=1




# generating map for screen pos
"""
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
"""


state = {i: 'b' if i in [1, 5, 21, 25] else 'e' for i in range(1,26)}
baagh_draw_positions =set()
baagh_image = pygame.image.load('baagh.png')
baagh_image_size = baagh_image.get_size()
baagh_image_w = baagh_image_size[0]
baagh_image_h = baagh_image_size[1]
baagh_image_position = None
baagh_image_rect = baagh_image.get_rect()

goat_draw_positions =set()
goat_image = pygame.image.load('goat.png')
goat_image_size = goat_image.get_size()
goat_image_w = goat_image_size[0]
goat_image_h = goat_image_size[1]
goat_image_position = None
goat_image_rect = goat_image.get_rect()



valid_positions = []
pos_rec = {}
for i,pos in board_points_pos.items():
    if i in [1, 5, 21, 25]:
        baagh_draw_positions.add(i)
    r = pygame.Rect(pos[0]-25,pos[1]-25, 50, 50)
    pos_rec[i] = r
    valid_positions.append([i,r])

def is_filled(pos):
    global baagh_draw_positions, goat_draw_positions
    return pos in baagh_draw_positions or pos in goat_draw_positions



def get_possible_move_positions(i, baagh = False):
    diags = [3,7,11,17,23,19,15,9]
    possible_moves ={} 
    # get horizontal
    r = i+1 #right
    if (r in pos_rec and i not in [5, 10, 15, 20,25]): 
        if not is_filled(r):
            possible_moves[r] = False
        elif baagh and r+1 in pos_rec and not is_filled(r+1):
            possible_moves[r+1] = r
    l = i-1 #left
    if(l in pos_rec and i not in [1,6,11,16,21]): 
        if not is_filled(l):
            possible_moves[l] = False
        elif baagh and l-1 in pos_rec and not is_filled(l-1):
            naagyo = l
            possible_moves[l-1] = l
    # get vertical
    t = i-5 #top
    if(t in pos_rec): 
        if not is_filled(t):
            possible_moves[t] = False
        elif baagh and t-5 in pos_rec and not is_filled(t-5) and t-5 not in [1,2,3,4,5]:
            possible_moves[t-5] = t
    b = i+5 #bottom
    if(b in pos_rec): 
        if not is_filled(b):
            possible_moves[b] = False
        elif baagh and b+5 in pos_rec and not is_filled(b+5) and b not in [21, 22, 23, 24, 25]:
            possible_moves[b+5] = b
    # get diagonal
    if(i in diags):
        if(i == 3):
            if not is_filled(7):
                possible_moves[7] = False
            elif baagh and not is_filled(11):
                possible_moves[11] = 7

            if not is_filled(9):
                possible_moves[9] = False
            elif baagh and not is_filled(15):
                possible_moves[15] = 9

        elif(i == 23):
            if not is_filled(17):
                possible_moves[17] = False 
            elif baagh and not is_filled(11):
                possible_moves[11] = 17 

            if not is_filled(19):
                possible_moves[19] = False
            elif baagh and not is_filled(15):
                possible_moves[15] = 19

        elif(i == 11):
            if not is_filled(17):
                possible_moves[17] = False
            elif baagh and not is_filled(23):
                possible_moves[23] = 17

            if not is_filled(7):
                possible_moves[7] = False
            elif baagh and not is_filled(3):
                possible_moves[3] = 7


        elif(i == 15):
            if not is_filled(9):
                possible_moves[9] = False
            elif baagh and not is_filled(3):
                possible_moves[3] = 9

            if not is_filled(19):
                possible_moves[19] = False
            elif baagh and not is_filled(23):
                possible_moves[23] = 19


        elif(i == 7):
            if not is_filled(3):
                possible_moves[3] = False
            if not is_filled(11):
                possible_moves[11] = False

        elif(i == 9):
            if not is_filled(3):
                possible_moves[3] = False
            if not is_filled(15):
                possible_moves[15] = False
        elif(i == 19):
            if not is_filled(23):
                possible_moves[23] = False
            if not is_filled(15):
                possible_moves[15] = False
        elif(i == 17):
            if not is_filled(23):
                possible_moves[23] = False
            if not is_filled(11):
                possible_moves[11] = False
    return possible_moves
print('\n\n')
for i in range(1, 26):
    print(i, get_possible_move_positions(i, True))
def draw_board():
    global board_points_pos
    # horizontal
    pygame.draw.line(screen, line_color, board_points_pos[1], board_points_pos[5], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[6], board_points_pos[10], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[11], board_points_pos[15], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[16], board_points_pos[20], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[21], board_points_pos[25], line_width)
    # vertical
    pygame.draw.line(screen, line_color, board_points_pos[1], board_points_pos[21], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[2], board_points_pos[22], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[3], board_points_pos[23], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[4], board_points_pos[24], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[5], board_points_pos[25], line_width)
    # diagonal
    pygame.draw.line(screen, line_color, board_points_pos[3], board_points_pos[15], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[15], board_points_pos[23], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[23], board_points_pos[11], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[11], board_points_pos[3], line_width)

    global valid_positions
    for _,pos in valid_positions:
        pygame.draw.rect(screen,color =(255,255,255), rect=pos)


baagh_turn = False
baagh_dragging = False
goat_dragging = False
dragged_valid_rect  = None
dragged_valid_pos = None
def print_state():
    global state
    print(state[1], state[2], state[3], state[4], state[5])
    print(state[6], state[7], state[8], state[9], state[10])
    print(state[11], state[12], state[13], state[14], state[15])
    print(state[16], state[17], state[18], state[19], state[20])
    print(state[21], state[22], state[23], state[24], state[25])
    print('**********************')

running = True
while running:
    # handling events
    screen.fill((23,45,67))
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for pos,valid_rect in valid_positions:
                if (valid_rect.collidepoint(event.pos)):
                    if baagh_turn:
                        # baagh_draw_positions.append(valid_rect)
                        if(pos in baagh_draw_positions):
                            baagh_dragging = True
                            dragged_valid_rect = valid_rect
                            dragged_valid_pos = pos
                            break
                    else:
                        if (len(goat_draw_positions) < 20 and not is_filled(pos)):
                            goat_draw_positions.add(pos)
                            state[pos] = 'g'
                            baagh_turn = True
                            print_state()
                            break
                        elif len(goat_draw_positions) >= 20:
                            goat_dragging = True
                            dragged_valid_rect = valid_rect
                            dragged_valid_pos = pos
                            break
        elif event.type == pygame.MOUSEBUTTONUP:
            if(baagh_dragging or goat_dragging):
                legal_pos = get_possible_move_positions(dragged_valid_pos, baagh_turn)
                for pos,valid_rect in valid_positions:
                    if (valid_rect.collidepoint(event.pos)): 
                        if (baagh_turn and baagh_dragging and pos in legal_pos ):
                            baagh_draw_positions.remove(dragged_valid_pos)
                            if legal_pos[pos]:
                                GOAT_DEAD +=1
                                goat_draw_positions.remove(legal_pos[pos])
                                state[legal_pos[pos]] = 'e'
                            state[dragged_valid_pos] = 'e'
                            baagh_draw_positions.add(pos)
                            state[pos] = 'b'
                            print_state()
                            baagh_turn = False
                            baagh_dragging = False
                            break
                        if (not baagh_turn and goat_dragging and pos in legal_pos ):
                            goat_draw_positions.remove(dragged_valid_pos)
                            state[dragged_valid_pos] = 'e'
                            goat_draw_positions.add(pos)
                            for p in pos_rec:
                                if pos_rec[p] == valid_rect:
                                    state[p] = 'g'
                                    break
                            baagh_turn = True
                            goat_dragging = False
                            print_state()
                            break

    for pos in baagh_draw_positions:
        rect = pos_rec[pos]
        baagh_image_rect.center = rect.center
        screen.blit(baagh_image, baagh_image_rect)
    for pos in goat_draw_positions:
        rect = pos_rec[pos]
        goat_image_rect.center = rect.center
        screen.blit(goat_image, goat_image_rect)
    
    # check win
    if(GOAT_DEAD >= 5):
        print('Bagh won')
        break
    
    c = 0
    for pos, player in state.items():
        if player == 'b':
            legals = get_possible_move_positions(pos, True)
            if len(legals) == 0:
                c+=1
    print(c)
    if c == 4:
        print('GOAT WON')
        break
    # mandatory
    pygame.display.update()


