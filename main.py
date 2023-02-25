import pygame
import random
from copy import deepcopy

# init the pygame --> Mandatory
pygame.init()

WIDTH = 800
HEIGHT = 800
GOAT_COUNT =0
GOAT_DEAD =0

screen = pygame.display.set_mode((WIDTH,HEIGHT)) # w * h


pygame.display.set_caption("Baagchaal")



# Define board dimensions
board_size =600

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
baagh_image = pygame.image.load('baagh.png')
baagh_image_rect = baagh_image.get_rect()

goat_image = pygame.image.load('goat.png')
goat_image_rect = goat_image.get_rect()



valid_positions = []
pos_rec = {}
for i,pos in board_points_pos.items():
    r = pygame.Rect(pos[0]-25,pos[1]-25, 50, 50)
    pos_rec[i] = r
    valid_positions.append([i,r])

def is_filled(pos):
    # global baagh_draw_positions, goat_draw_positions
    return state[pos] in ['g', 'b']



def get_possible_move_positions(i, baagh = False):
    diags = [3,7,11,17,23,19,15,9]
    possible_moves ={} 
    # get horizontal
    r = i+1 #right
    if (r in pos_rec and i not in [5, 10, 15, 20,25]): 
        if not is_filled(r):
            possible_moves[r] = False
        elif baagh and r+1 in pos_rec and not is_filled(r+1) and state[r] == 'g':
            possible_moves[r+1] = r
    l = i-1 #left
    if(l in pos_rec and i not in [1,6,11,16,21]): 
        if not is_filled(l):
            possible_moves[l] = False
        elif baagh and l-1 in pos_rec and not is_filled(l-1) and state[l] == 'g':
            naagyo = l
            possible_moves[l-1] = l
    # get vertical
    t = i-5 #top
    if(t in pos_rec): 
        if not is_filled(t):
            possible_moves[t] = False
        elif baagh and t-5 in pos_rec and not is_filled(t-5) and t-5 not in [1,2,3,4,5] and state[t] == 'g':
            possible_moves[t-5] = t
    b = i+5 #bottom
    if(b in pos_rec): 
        if not is_filled(b):
            possible_moves[b] = False
        elif baagh and b+5 in pos_rec and not is_filled(b+5) and b not in [21, 22, 23, 24, 25] and state[b] == 'g':
            possible_moves[b+5] = b

            

    # get diagonal
    if ( i == 1):
        if not is_filled(7):
            possible_moves[7] = False
        elif baagh and not is_filled(13) and state[7] == 'g':
            possible_moves[13] = 7

    if ( i == 5):
        if not is_filled(9):
            possible_moves[9] = False
        elif baagh and not is_filled(13) and state[9] == 'g':
            possible_moves[13] = 9



    if ( i == 7):
        if not is_filled(1):
            possible_moves[1] = False
        if not is_filled(13):
            possible_moves[13] = False
        elif baagh and not is_filled(19) and state[13] == 'g':
            possible_moves[19] =13 

            
    if ( i == 9):
        if not is_filled(5):
            possible_moves[5] = False
        if not is_filled(13):
            possible_moves[13] = False
        elif baagh and not is_filled(17) and state[13] == 'g':
            possible_moves[17] =13 
            
    if ( i == 13):
        if not is_filled(7):
            possible_moves[1] = False
        elif baagh and not is_filled(1) and state[7] == 'g':
            possible_moves[1] = 7

        if not is_filled(19):
            possible_moves[19] = False
        elif baagh and not is_filled(25) and state[19] == 'g':
            possible_moves[25] =19 

        if not is_filled(9):
            possible_moves[9] = False
        elif baagh and not is_filled(5) and state[9] == 'g':
            possible_moves[5] = 9

        if not is_filled(17):
            possible_moves[17] = False
        elif baagh and not is_filled(21) and state[17] == 'g':
            possible_moves[21] = 17

    if ( i == 19):
        if not is_filled(25):
            possible_moves[25] = False
        if not is_filled(13):
            possible_moves[13] = False
        elif baagh and not is_filled(7) and state[13] == 'g':
            possible_moves[7] =13 
    
    if ( i == 17):
        if not is_filled(21):
            possible_moves[21] = False
        if not is_filled(13):
            possible_moves[13] = False
        elif baagh and not is_filled(9) and state[13] == 'g':
            possible_moves[9] =13 

    if(i == 25):
        if not is_filled(19):
            possible_moves[19] = False
        elif baagh and not is_filled(13) and state[19] == 'g':
            possible_moves[13] = 19

    if(i == 21):
        if not is_filled(17):
            possible_moves[17] = False
        elif baagh and not is_filled(13) and state[17] == 'g':
            possible_moves[13] = 17

           
    
    # get square
    if(i in diags):
        if(i == 3):
            if not is_filled(7):
                possible_moves[7] = False
            elif baagh and not is_filled(11) and state[7] == 'g':
                possible_moves[11] = 7

            if not is_filled(9):
                possible_moves[9] = False
            elif baagh and not is_filled(15) and state[9] == 'g':
                possible_moves[15] = 9

        elif(i == 23):
            if not is_filled(17):
                possible_moves[17] = False 
            elif baagh and not is_filled(11) and state[17] == 'g':
                possible_moves[11] = 17 

            if not is_filled(19):
                possible_moves[19] = False
            elif baagh and not is_filled(15) and state[19] == 'g':
                possible_moves[15] = 19

        elif(i == 11):
            if not is_filled(17):
                possible_moves[17] = False
            elif baagh and not is_filled(23) and state[17] == 'g':
                possible_moves[23] = 17

            if not is_filled(7):
                possible_moves[7] = False
            elif baagh and not is_filled(3) and state[7] == 'g':
                possible_moves[3] = 7


        elif(i == 15):
            if not is_filled(9):
                possible_moves[9] = False
            elif baagh and not is_filled(3) and state[9] == 'g':
                possible_moves[3] = 9

            if not is_filled(19):
                possible_moves[19] = False
            elif baagh and not is_filled(23) and state[19] == 'g':
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

def generate_states(state, baagh = False):
    legal_states = []
    if baagh:
        for pos in state:
            if state[pos] == 'b':
                legal_moves_from_this_position = get_possible_move_positions(pos, True)
                for next_pos, mareko in legal_moves_from_this_position.items():
                    c_state = deepcopy(state)
                    c_state[pos] = 'e'
                    if mareko:
                        c_state[mareko] = 'e'
                    c_state[next_pos] = 'b'
                    legal_states.append(c_state)
    elif GOAT_COUNT + GOAT_DEAD < 20:
        empty_pos = [pos for pos in state if state[pos] == 'e']
        for pos in empty_pos:
            c_state = deepcopy(state)
            c_state[pos] = 'g'
            legal_states.append(c_state)
    else:
        for pos in state:
            if state[pos] == 'g':
                legal_moves_from_this_position = get_possible_move_positions(pos, False)
                for next_pos in legal_moves_from_this_position:
                    c_state = deepcopy(state)
                    c_state[pos] = 'e'
                    c_state[next_pos] = 'g'
                    legal_states.append(c_state)

    return legal_states
                
                
                        

                        

        
    

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
    # square
    pygame.draw.line(screen, line_color, board_points_pos[3], board_points_pos[15], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[15], board_points_pos[23], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[23], board_points_pos[11], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[11], board_points_pos[3], line_width)
    #diagonal
    pygame.draw.line(screen, line_color, board_points_pos[1], board_points_pos[25], line_width)
    pygame.draw.line(screen, line_color, board_points_pos[5], board_points_pos[21], line_width)

    global valid_positions
    for _,pos in valid_positions:
        pygame.draw.rect(screen,color =(255,255,255), rect=pos)


baagh_turn = False
baagh_dragging = False
goat_dragging = False
dragged_valid_pos = None

def print_state(state):
    print(state[1], state[2], state[3], state[4], state[5])
    print(state[6], state[7], state[8], state[9], state[10])
    print(state[11], state[12], state[13], state[14], state[15])
    print(state[16], state[17], state[18], state[19], state[20])
    print(state[21], state[22], state[23], state[24], state[25])
    print('**********************')
    
def draw_state(state):
    for pos in state:
        if state[pos] == 'b':
            rect = pos_rec[pos]
            baagh_image_rect.center = rect.center
            screen.blit(baagh_image, baagh_image_rect)
        elif state[pos] == 'g':
            rect = pos_rec[pos]
            goat_image_rect.center = rect.center
            screen.blit(goat_image, goat_image_rect)

def check_win(state):            
    # check win
    if (GOAT_DEAD >= 5):
        return 1
    c = 0
    for pos, player in state.items():
        if player == 'b':
            legals = get_possible_move_positions(pos, True)
            if len(legals) == 0:
                c+=1
    return 2 if c==4 else -1 

win_text = {
    1:'Bagh won', 
    2: 'Goat won'
}         

running = True
while running:
    screen.fill((23,45,67))
    draw_board()
    if not baagh_turn:
        legal_states = generate_states(state, False)
        state = random.choice(legal_states)
        GOAT_COUNT +=1
        baagh_turn = True
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for pos,valid_rect in valid_positions:
                    if (
                        (valid_rect.collidepoint(event.pos))
                        and (state[pos] == 'b')
                    ):
                        baagh_dragging = True
                        dragged_valid_pos = pos
                        break
                                    # else:
                                    # elif (valid_rect.collidepoint(event.pos)):
                                    #     if (len(goat_draw_positions) < 20 and not is_filled(pos)):
                                    #         goat_draw_positions.add(pos)
                                    #         state[pos] = 'g'
                                    #         baagh_turn = True
                                    #         print_state()
                                    #         break
                                    #     elif len(goat_draw_positions) >= 20:
                                    #         goat_dragging = True
                                    #         dragged_valid_rect = valid_rect
                                    #         dragged_valid_pos = pos
                                    #         break
            elif event.type == pygame.MOUSEBUTTONUP:
                if (baagh_dragging or goat_dragging):
                    legal_pos = get_possible_move_positions(dragged_valid_pos, baagh_turn)
                    for pos,valid_rect in valid_positions:
                        if (valid_rect.collidepoint(event.pos)) and (
                            baagh_dragging and pos in legal_pos
                        ):
                            if legal_pos[pos] and state[legal_pos[pos]] == 'g':
                                GOAT_DEAD +=1
                                state[legal_pos[pos]] = 'e'
                            state[dragged_valid_pos] = 'e'
                            state[pos] = 'b'
                            baagh_turn = False
                            baagh_dragging = False
                            break
    draw_state(state)


    c_w = check_win(state)
    if(c_w == -1):
        pygame.display.update()
    else:
        print(win_text[c_w])
        break

    # mandatory


