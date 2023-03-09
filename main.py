from collections import defaultdict
import pygame
import math
import random
from copy import deepcopy
import contextlib

# init the pygame --> Mandatory
pygame.init()
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # w * h
pygame.display.set_caption("Baagchaal")


class TreeNode:
    def __init__(self, board, parent=None):
        self.board = board
        self.childrens = {}
        self.baagh_wins = 0
        self.goat_wins = 0
        self.visits = 0
        self.parent = parent
        self.is_fully_expanded = len(self.childrens) == len(
            self.board.generate_states())


class MCTS:
    ITERATIONS = 500

    def __init__(self, board):
        self.root_node = TreeNode(board, None)
        self.GOAT_COUNT = board.GOAT_COUNT
        self.GOAT_DEAD = board.GOAT_DEAD

    def ucb(self, s, n, N, c):
        return (s/n) + c * math.sqrt(math.log(N)/n)

    def search(self):
        data = {0: 0, 1: 0, 2: 0}
        # walk through 1000 iterations
        for _ in range(MCTS.ITERATIONS):
            # select a node (selection phase)
            node = self.select(self.root_node)
            # scrore current node (simulation phase)
            temp_board = deepcopy(node.board)
            # temp_board.player = not temp_board.player
            score = temp_board.random_play()
            data[score] += 1
            # backpropagate results
            self.backpropagate(node, score)
        print(data)

        with contextlib.suppress(Exception):
            best_move = self.get_best_move(self.root_node, 0)
            return best_move.board.state

    def select(self, node):
        # make sure that we're dealing with non-terminal nodes
        # depth = 0
        while node.board.check_win() == -1:
            # case where the node is fully expanded

            if node.is_fully_expanded:
                # print('select')
                node = self.get_best_move(node, 2)

                # node.board.print_state()
            # case where the node is not fully expanded
            else:
                # print('expand')
                # otherwise expand the node
                return self.expand(node)

        # return node
        # print('yeta ta auna paryo ni')
        # print(depth)
        return node

    def expand(self, node):
        # generate legal states (moves) for the given node
        states = node.board.generate_states(filter=True)

        # loop over generated states (moves)
        for state in states:
            # make sure that current state (move) is not present in child nodes
            if str(state) not in node.childrens:
                # create a new node
                b = Board(not node.board.player, state)
                new_node = TreeNode(b, node)
                new_node.board.GOAT_COUNT = node.board.GOAT_COUNT
                new_node.board.GOAT_DEAD = node.board.GOAT_DEAD

                # add child node to parent's node children list (dict)
                node.childrens[str(state)] = new_node

                # case when node is fully expanded
                if len(states) == len(node.childrens):
                    node.is_fully_expanded = True

                # return newly created node
                if (node.board.player is False) and (
                    new_node.board.GOAT_COUNT < 20
                ):
                    new_node.board.GOAT_COUNT += 1
                if (node.board.player is True) and (
                    node.board.get_goat_count() > new_node.board.get_goat_count()
                ):
                    new_node.board.GOAT_DEAD += 1

                return new_node

        # debugging
        print('Should not get here!!!')

    def backpropagate(self, node, score):
        while node is not None:
            # depth += 1
            node.visits += 1

            if score == 1:
                node.baagh_wins += 1
            elif score == 2:
                node.goat_wins += 1
            elif score == 0:
                node.baagh_wins += 0.5
                node.goat_wins += 0.5
            # set node to parent
            node = node.parent
        # print('depth:', depth)

    def get_best_move(self, node, c):
        # define best score & best moves
        best_score = float('-inf')
        best_moves = []
        curr_player = node.board.player
        ucbs = []

        # loop over child nodes
        if (c == 0):
            print('Baagh wins       Goat Wins           Visits')
        for child_node in node.childrens.values():
            # define current player
            if (c == 0):
                print(child_node.baagh_wins,
                      child_node.goat_wins, child_node.visits)
            if curr_player is True:
                ucb = self.ucb(child_node.baagh_wins,
                               child_node.visits, self.root_node.visits, c)
            else:
                ucb = self.ucb(child_node.goat_wins,
                               child_node.visits, self.root_node.visits, c)
                ucbs.append(ucb)

            # better move has been found
            if ucb > best_score:
                best_score = ucb
                best_moves = [child_node]

            # found as good move as already available
            elif ucb == best_score:
                best_moves.append(child_node)

        # return one of the best moves randomly
        return random.choice(best_moves)


class Board:
    def __init__(self, player, state):
        self.state = state
        self.player = player
        self.GOAT_COUNT = 0
        self.GOAT_DEAD = 0

    def is_filled(self, pos):
        return self.state[pos] in ['g', 'b']

    def get_possible_move_positions(self, i):
        baagh = self.player
        diags = [3, 7, 11, 17, 23, 19, 15, 9]
        possible_moves = {}
        # get horizontal
        r = i+1  # right
        if (r in pos_rec and i not in [5, 10, 15, 20, 25]):
            if not self.is_filled(r):
                possible_moves[r] = False
            elif baagh and r+1 in pos_rec and not self.is_filled(r+1) and self.state[r] == 'g':
                possible_moves[r+1] = r
        l = i-1  # left
        if (l in pos_rec and i not in [1, 6, 11, 16, 21]):
            if not self.is_filled(l):
                possible_moves[l] = False
            elif baagh and l-1 in pos_rec and not self.is_filled(l-1) and self.state[l] == 'g':
                possible_moves[l-1] = l
        # get vertical
        t = i-5  # top
        if (t in pos_rec):
            if not self.is_filled(t):
                possible_moves[t] = False
            elif baagh and t-5 in pos_rec and not self.is_filled(t-5) and self.state[t] == 'g':
                possible_moves[t-5] = t
        b = i+5  # bottom
        if (b in pos_rec):
            if not self.is_filled(b):
                possible_moves[b] = False
            elif baagh and b+5 in pos_rec and not self.is_filled(b+5) and self.state[b] == 'g':
                possible_moves[b+5] = b

        # get diagonal
        if (i == 1):
            if not self.is_filled(7):
                possible_moves[7] = False
            elif baagh and not self.is_filled(13) and self.state[7] == 'g':
                possible_moves[13] = 7

        if (i == 5):
            if not self.is_filled(9):
                possible_moves[9] = False
            elif baagh and not self.is_filled(13) and self.state[9] == 'g':
                possible_moves[13] = 9

        if (i == 7):
            if not self.is_filled(1):
                possible_moves[1] = False
            if not self.is_filled(13):
                possible_moves[13] = False
            elif baagh and not self.is_filled(19) and self.state[13] == 'g':
                possible_moves[19] = 13

        if (i == 9):
            if not self.is_filled(5):
                possible_moves[5] = False
            if not self.is_filled(13):
                possible_moves[13] = False
            elif baagh and not self.is_filled(17) and self.state[13] == 'g':
                possible_moves[17] = 13

        if (i == 13):
            if not self.is_filled(7):
                possible_moves[1] = False
            elif baagh and not self.is_filled(1) and self.state[7] == 'g':
                possible_moves[1] = 7

            if not self.is_filled(19):
                possible_moves[19] = False
            elif baagh and not self.is_filled(25) and self.state[19] == 'g':
                possible_moves[25] = 19

            if not self.is_filled(9):
                possible_moves[9] = False
            elif baagh and not self.is_filled(5) and self.state[9] == 'g':
                possible_moves[5] = 9

            if not self.is_filled(17):
                possible_moves[17] = False
            elif baagh and not self.is_filled(21) and self.state[17] == 'g':
                possible_moves[21] = 17

        if (i == 19):
            if not self.is_filled(25):
                possible_moves[25] = False
            if not self.is_filled(13):
                possible_moves[13] = False
            elif baagh and not self.is_filled(7) and self.state[13] == 'g':
                possible_moves[7] = 13

        if (i == 17):
            if not self.is_filled(21):
                possible_moves[21] = False
            if not self.is_filled(13):
                possible_moves[13] = False
            elif baagh and not self.is_filled(9) and self.state[13] == 'g':
                possible_moves[9] = 13

        if (i == 25):
            if not self.is_filled(19):
                possible_moves[19] = False
            elif baagh and not self.is_filled(13) and self.state[19] == 'g':
                possible_moves[13] = 19

        if (i == 21):
            if not self.is_filled(17):
                possible_moves[17] = False
            elif baagh and not self.is_filled(13) and self.state[17] == 'g':
                possible_moves[13] = 17

        # get square
        if (i in diags):
            if (i == 3):
                if not self.is_filled(7):
                    possible_moves[7] = False
                elif baagh and not self.is_filled(11) and self.state[7] == 'g':
                    possible_moves[11] = 7

                if not self.is_filled(9):
                    possible_moves[9] = False
                elif baagh and not self.is_filled(15) and self.state[9] == 'g':
                    possible_moves[15] = 9

            elif (i == 23):
                if not self.is_filled(17):
                    possible_moves[17] = False
                elif baagh and not self.is_filled(11) and self.state[17] == 'g':
                    possible_moves[11] = 17

                if not self.is_filled(19):
                    possible_moves[19] = False
                elif baagh and not self.is_filled(15) and self.state[19] == 'g':
                    possible_moves[15] = 19

            elif (i == 11):
                if not self.is_filled(17):
                    possible_moves[17] = False
                elif baagh and not self.is_filled(23) and self.state[17] == 'g':
                    possible_moves[23] = 17

                if not self.is_filled(7):
                    possible_moves[7] = False
                elif baagh and not self.is_filled(3) and self.state[7] == 'g':
                    possible_moves[3] = 7

            elif (i == 15):
                if not self.is_filled(9):
                    possible_moves[9] = False
                elif baagh and not self.is_filled(3) and self.state[9] == 'g':
                    possible_moves[3] = 9

                if not self.is_filled(19):
                    possible_moves[19] = False
                elif baagh and not self.is_filled(23) and self.state[19] == 'g':
                    possible_moves[23] = 19

            elif (i == 7):
                if not self.is_filled(3):
                    possible_moves[3] = False
                if not self.is_filled(11):
                    possible_moves[11] = False

            elif (i == 9):
                if not self.is_filled(3):
                    possible_moves[3] = False
                if not self.is_filled(15):
                    possible_moves[15] = False
            elif (i == 19):
                if not self.is_filled(23):
                    possible_moves[23] = False
                if not self.is_filled(15):
                    possible_moves[15] = False
            elif (i == 17):
                if not self.is_filled(23):
                    possible_moves[23] = False
                if not self.is_filled(11):
                    possible_moves[11] = False
        return possible_moves

    def generate_states(self, filter=False):
        baagh = self.player
        state = self.state
        legal_states = []
        if baagh:
            for pos in state:
                if state[pos] == 'b':
                    legal_moves_from_this_position = self.get_possible_move_positions(
                        pos)
                    for next_pos, mareko in legal_moves_from_this_position.items():
                        c_state = deepcopy(state)
                        c_state[pos] = '.'
                        if mareko and state[mareko] == 'g':
                            c_state[mareko] = '.'
                        c_state[next_pos] = 'b'
                        legal_states.append(c_state)
        else:
            saving_positions = self.saving_goat_positions()
            safe_positions = self.goat_safe_positions()
            if self.GOAT_COUNT < 20:
                empty_pos = [pos for pos in state if state[pos] == '.']
                if filter and len(saving_positions) > 0:
                    for p in empty_pos:
                        if p in saving_positions:
                            c_state = deepcopy(state)
                            c_state[p] = 'g'
                            legal_states.append(c_state)
                elif filter and len(safe_positions) > 0:
                    for p in empty_pos:
                        if p in safe_positions:
                            c_state = deepcopy(state)
                            c_state[p] = 'g'
                            legal_states.append(c_state)
                else:
                    for p in empty_pos:
                        c_state = deepcopy(state)
                        c_state[p] = 'g'
                        legal_states.append(c_state)
                    
            else:
                for pos in state:
                    if state[pos] == 'g':
                        legal_moves_from_this_position = self.get_possible_move_positions(
                            pos)
                        for next_pos in legal_moves_from_this_position:
                            if filter and len(saving_positions) > 0 and next_pos in saving_positions:
                                c_state = deepcopy(state)
                                c_state[pos] = '.'
                                c_state[next_pos] = 'g'
                                legal_states.append(c_state)
                            elif filter and len(safe_positions) > 0 and next_pos in safe_positions:
                                c_state = deepcopy(state)
                                c_state[pos] = '.'
                                c_state[next_pos] = 'g'
                                legal_states.append(c_state)
                            else:
                                c_state = deepcopy(state)
                                c_state[pos] = '.'
                                c_state[next_pos] = 'g'
                                legal_states.append(c_state)
        return legal_states

    def print_state(self):
        state = self.state
        print(state[1], state[2], state[3], state[4], state[5])
        print(state[6], state[7], state[8], state[9], state[10])
        print(state[11], state[12], state[13], state[14], state[15])
        print(state[16], state[17], state[18], state[19], state[20])
        print(state[21], state[22], state[23], state[24], state[25])

    def check_win(self):
        # check win
        if (self.GOAT_DEAD >= 5):
            return 1
        c = 0
        for pos, player in self.state.items():
            if player == 'b':
                legals = self.get_possible_move_positions(pos)
                if len(legals) == 0:
                    c += 1
        return 2 if c == 4 else -1

    def draw_state(self):
        for pos in self.state:
            if self.state[pos] == 'b':
                rect = pos_rec[pos]
                baagh_image_rect.center = rect.center
                screen.blit(baagh_image, baagh_image_rect)
            elif self.state[pos] == 'g':
                rect = pos_rec[pos]
                goat_image_rect.center = rect.center
                screen.blit(goat_image, goat_image_rect)

    def get_goat_count(self):
        return sum(self.state[pos] == 'g' for pos in self.state)

    def random_play(self):
        while (self.check_win() == -1):
            legal_states = self.generate_states(filter=True)
            if len(legal_states) == 0:
                print('???????????????????????????????')
                self.print_state()
                print('???????????????????????????????')
                return 0
            # print('BEFORE PLAY:')
            # self.print_state()
            prev_goat_count = self.get_goat_count()
            # print("Goat count: ", prev_goat_count)
            # print("Goat dead: ", self.GOAT_DEAD)
            self.state = random.choice(legal_states)
            curr_goat_count = self.get_goat_count()
            # print('AFTER PLAY:')
            # self.print_state()
            # print('Goat count: ', curr_goat_count)
            if self.player is False:
                if self.GOAT_COUNT < 20:
                    self.GOAT_COUNT += 1
                self.player = True
            elif self.player is True:
                if (curr_goat_count < prev_goat_count):
                    self.GOAT_DEAD += 1
                self.player = False
            # print("Goat dead: ", self.GOAT_DEAD)
            # print('***************************')

        return self.check_win()

    def saving_goat_positions(self):
        neighbours = {
            1: [2, 6, 7],
            2: [1, 3, 7],
            3: [2, 4, 7, 8, 9],
            4: [3, 5, 9],
            5: [4, 9, 10],
            6: [1, 7, 11],
            7: [1, 2, 3, 6, 8, 11, 12, 13],
            8: [3, 7, 9, 13],
            9: [3, 4, 5, 8, 10, 13, 14, 15],
            10: [5, 9, 15],
            11: [6, 7, 12, 16, 17],
            12: [7, 11, 13, 17],
            13: [7, 8, 9, 12, 14, 17, 18, 19],
            14: [9, 13, 15, 19],
            15: [9, 10, 14, 19, 20],
            16: [11, 17, 21],
            17: [11, 12, 13, 16, 18, 21, 22, 23],
            18: [13, 17, 19, 23],
            19: [13, 14, 15, 18, 20, 23, 24, 25],
            20: [15, 19, 25],
            21: [16, 17, 22],
            22: [17, 21, 23],
            23: [17, 18, 19, 22, 24],
            24: [19, 23, 25],
            25: [19, 20, 24]
        }
        positions = []
        for pos in self.state:
            if self.state[pos] == 'g':
                n = neighbours[pos]
                for n_pos in n:
                    if self.state[n_pos] == 'b' and pos > n_pos:
                        diff = pos-n_pos
                        if (pos+diff) in self.state and self.state[pos + diff] == '.':
                            positions.append(pos+diff)
                    elif self.state[n_pos] == 'b' and pos < n_pos:
                        diff = n_pos-pos
                        if (pos-diff) in self.state and self.state[pos - diff] == '.':
                            positions.append(pos-diff)
        return positions

    def goat_safe_positions(self):
        neighbours = {
            1: [2, 6, 7],
            2: [1, 3, 7],
            3: [2, 4, 7, 8, 9],
            4: [3, 5, 9],
            5: [4, 9, 10],
            6: [1, 7, 11],
            7: [1, 2, 3, 6, 8, 11, 12, 13],
            8: [3, 7, 9, 13],
            9: [3, 4, 5, 8, 10, 13, 14, 15],
            10: [5, 9, 15],
            11: [6, 7, 12, 16, 17],
            12: [7, 11, 13, 17],
            13: [7, 8, 9, 12, 14, 17, 18, 19],
            14: [9, 13, 15, 19],
            15: [9, 10, 14, 19, 20],
            16: [11, 17, 21],
            17: [11, 12, 13, 16, 18, 21, 22, 23],
            18: [13, 17, 19, 23],
            19: [13, 14, 15, 18, 20, 23, 24, 25],
            20: [15, 19, 25],
            21: [16, 17, 22],
            22: [17, 21, 23],
            23: [17, 18, 19, 22, 24],
            24: [19, 23, 25],
            25: [19, 20, 24]
        }
        positions = []
        for pos in self.state:
            if(self.state[pos] == '.'):
                n = neighbours[pos]
                available = all(self.state[n_pos] != 'b' for n_pos in n)
                if available:
                    positions.append(pos)
        return positions


# Define board dimensions
board_size = 600

# Define line and circle properties
line_width = 5
line_color = (255, 255, 255)


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
        board_points_pos[pos] = (w, h)
        pos += 1


baagh_image = pygame.image.load('baagh.png')
baagh_image_rect = baagh_image.get_rect()

goat_image = pygame.image.load('goat.png')
goat_image_rect = goat_image.get_rect()


valid_positions = []
pos_rec = {}
for i, pos in board_points_pos.items():
    r = pygame.Rect(pos[0]-25, pos[1]-25, 50, 50)
    pos_rec[i] = r
    valid_positions.append([i, r])


# state = {
#         i: 'b' if i in [1, 5, 21, 25] else '.' for i in range(1, 26)
#     }
# board = Board(False, state)
# val = board.random_play()
# print(val)


def draw_board():
    global board_points_pos
    # horizontal
    pygame.draw.line(screen, line_color,
                     board_points_pos[1], board_points_pos[5], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[6], board_points_pos[10], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[11], board_points_pos[15], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[16], board_points_pos[20], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[21], board_points_pos[25], line_width)
    # vertical
    pygame.draw.line(screen, line_color,
                     board_points_pos[1], board_points_pos[21], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[2], board_points_pos[22], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[3], board_points_pos[23], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[4], board_points_pos[24], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[5], board_points_pos[25], line_width)
    # square
    pygame.draw.line(screen, line_color,
                     board_points_pos[3], board_points_pos[15], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[15], board_points_pos[23], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[23], board_points_pos[11], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[11], board_points_pos[3], line_width)
    # diagonal
    pygame.draw.line(screen, line_color,
                     board_points_pos[1], board_points_pos[25], line_width)
    pygame.draw.line(screen, line_color,
                     board_points_pos[5], board_points_pos[21], line_width)

    global valid_positions
    for _, pos in valid_positions:
        pygame.draw.rect(screen, color=(255, 255, 255), rect=pos)

# state = {i: 'b' if i in [1, 5, 21, 25] else '.' for i in range(1, 26)}
# board = Board(False, state)
# mcts = MCTS(board)
# board.state = mcts.search()
# board.print_state()


def game_loop_mulitplayer():
    state = {
        i: 'b' if i in [1, 5, 21, 25] else '.' for i in range(1, 26)
    }
    board = Board(False, state)
    baagh_dragging = False
    goat_dragging = False
    dragged_valid_pos = None

    win_text = {
        1: 'Bagh won',
        2: 'Goat won'
    }
    running = True
    while running:
        baagh_turn = board.player
        screen.fill((23, 45, 67))
        draw_board()
        # board.draw_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for pos, valid_rect in valid_positions:
                    if (baagh_turn and
                                (valid_rect.collidepoint(event.pos))
                                and (board.state[pos] == 'b')
                            ):
                        baagh_dragging = True
                        dragged_valid_pos = pos
                        break
                        # else:
                    elif (not baagh_turn and valid_rect.collidepoint(event.pos)):
                        if (board.GOAT_COUNT < 20 and not board.is_filled(pos)):
                            state[pos] = 'g'
                            board.player = True
                            board.GOAT_COUNT += 1
                            break
                        elif board.GOAT_COUNT >= 20 and board.state[pos] == 'g':
                            goat_dragging = True
                            dragged_valid_pos = pos
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if baagh_dragging or goat_dragging:
                    legal_pos = board.get_possible_move_positions(
                        dragged_valid_pos)
                    for pos, valid_rect in valid_positions:
                        if valid_rect.collidepoint(event.pos):
                            if baagh_dragging and pos in legal_pos:
                                board.state[dragged_valid_pos] = '.'
                                board.state[pos] = 'b'
                                baagh_dragging = False
                                board.player = False
                                if (legal_pos[pos]):
                                    board.GOAT_DEAD += 1
                                    board.state[legal_pos[pos]] = '.'
                            elif goat_dragging and pos in legal_pos:
                                board.state[dragged_valid_pos] = '.'
                                board.state[pos] = 'g'
                                board.player = True
                                goat_dragging = False

        board.draw_state()

        c_w = board.check_win()
        if (c_w == -1):
            pygame.display.update()
        else:
            print(win_text[c_w])
            break


def game_loop_gmcts():
    state = {
        i: 'b' if i in [1, 5, 21, 25] else '.' for i in range(1, 26)
    }
    board = Board(False, state)
    baagh_dragging = False
    goat_dragging = False
    dragged_valid_pos = None

    win_text = {
        1: 'Bagh won',
        2: 'Goat won'
    }
    running = True
    while running:
        baagh_turn = board.player
        screen.fill((23, 45, 67))
        draw_board()
        if not baagh_turn:
            mcts = MCTS(board)
            board.state = mcts.search()
            board.player = True
            if board.GOAT_COUNT < 20:
                board.GOAT_COUNT += 1
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for pos, valid_rect in valid_positions:
                        if (
                            (valid_rect.collidepoint(event.pos))
                            and (board.state[pos] == 'b')
                        ):
                            baagh_dragging = True
                            dragged_valid_pos = pos
                            break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if baagh_dragging:
                        legal_pos = board.get_possible_move_positions(
                            dragged_valid_pos)
                        for pos, valid_rect in valid_positions:
                            if valid_rect.collidepoint(event.pos) and pos in legal_pos:
                                if legal_pos[pos] and board.state[legal_pos[pos]] == 'g':
                                    board.GOAT_DEAD += 1
                                    board.state[legal_pos[pos]] = '.'
                                board.state[dragged_valid_pos] = '.'
                                board.state[pos] = 'b'
                                board.player = False
                                baagh_dragging = False
                                break
        board.draw_state()

        c_w = board.check_win()
        if (c_w == -1):
            pygame.display.update()
        else:
            print(win_text[c_w])
            break

    # mandatory


def game_loop_bmcts():
    state = {
        i: 'b' if i in [1, 5, 21, 25] else '.' for i in range(1, 26)
    }
    board = Board(False, state)
    baagh_dragging = False
    goat_dragging = False
    dragged_valid_pos = None

    win_text = {
        1: 'Bagh won',
        2: 'Goat won'
    }
    running = True
    while running:
        baagh_turn = board.player
        screen.fill((23, 45, 67))
        draw_board()
        if baagh_turn:
            mcts = MCTS(board)
            board.state = mcts.search()
            board.player = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for pos, valid_rect in valid_positions:
                        if valid_rect.collidepoint(event.pos):
                            if (board.GOAT_COUNT < 20 and not board.is_filled(pos)):
                                print('here')
                                board.state[pos] = 'g'
                                board.player = True
                                board.GOAT_COUNT += 1
                            elif board.GOAT_COUNT >= 20 and board.state[pos] == 'g':
                                goat_dragging = True
                                dragged_valid_pos = pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if baagh_dragging or goat_dragging:
                        legal_pos = board.get_possible_move_positions(
                            dragged_valid_pos)
                        for pos, valid_rect in valid_positions:
                            if (
                                valid_rect.collidepoint(event.pos)
                                and goat_dragging
                                and pos in legal_pos
                            ):
                                board.state[dragged_valid_pos] = '.'
                                board.state[pos] = 'g'
                                board.player = True
                                goat_dragging = False

        board.draw_state()

        c_w = board.check_win()
        if (c_w == -1):
            pygame.display.update()
        else:
            print(win_text[c_w])
            break


if __name__ == '__main__':
    game_loop_gmcts()
    # game_loop_mulitplayer()
