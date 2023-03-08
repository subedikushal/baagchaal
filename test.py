
def saving_goat_positions(state):
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
    for pos in state:
        if state[pos] == 'g':
            n = neighbours[pos]
            for n_pos in n:
                if state[n_pos] == 'b' and pos > n_pos:
                    diff = pos-n_pos
                    if (pos+diff) in state and state[pos + diff] == '.':
                        positions.append(pos+diff)
                elif state[n_pos] == 'b' and pos < n_pos:
                    diff = n_pos-pos
                    if (pos-diff) in state and state[pos - diff] == '.':
                        positions.append(pos-diff)
    return positions


def goat_safe_positions(state):
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
    for pos in state:
        if state[pos] == '.':
            n = neighbours[pos]
            available = all(state[n_pos] != 'b' for n_pos in n)
            if available:
                positions.append(pos)
    return positions


state = {
    i: 'b' if i in [1, 5, 21, 25] else '.' for i in range(1, 26)
}
state[15] = 'g'
state[20] = 'b'
print(saving_goat_positions(state))
print(goat_safe_positions(state))
