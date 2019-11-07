from copy import deepcopy
import random
from math import inf as infinity


class Piece:
    def __init__(self, index, position, owner):
        self.index = index
        self.position = {
            "row": position[0],
            "col": position[1]
        }
        self.owner = owner

    def __str__(self):
        return self.owner[0].lower() + str(self.index)

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        if self.index != other.index:
            return False
        if self.owner != other.owner:
            return False
        if self.position['row'] != other.position['row']:
            return False
        if self.position['col'] != other.position['col']:
            return False
        return True


class Table:
    def __init__(self):
        self.table = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        self.initialization()

    def initialization(self):
        for i in range(4):
            p = Piece(i + 1, [3, i], 'Player')
            self.table[p.position.get('row')][p.position.get('col')] = p
        for i in range(4):
            c = Piece(i + 1, [0, i], 'Computer')
            self.table[c.position.get('row')][c.position.get('col')] = c

    def is_final(self, local_table=None):
        if local_table is None:
            local_table = self.table
        if local_table[0][0] == local_table[0][1] == local_table[0][2] == local_table[0][3]:
            if local_table[0][0] is not None:
                if local_table[0][0].owner == 'Player':
                    return 1
        if local_table[3][0] == local_table[3][1] == local_table[3][2] == local_table[3][3]:
            if local_table[3][0] is not None:
                if local_table[3][0].owner == 'Computer':
                    return 2
        return 0

    def print(self, local_table=None, local_end=''):
        if local_table is None:
            local_table = self.table
        for i in local_table:
            for j in i:
                if j is None:
                    print('--', end=' ')
                else:
                    print(j, end=' ')
            print()
        print(local_end)

    def is_valid_move(self, positions, local_table=None):
        if local_table is None:
            local_table = self.table
        if positions[0] < 0 or positions[0] > 3:
            return False
        if positions[1] < 0 or positions[1] > 3:
            return False
        if local_table[positions[0]][positions[1]] is not None:
            return False
        return True

    def heuristics(self, heuristic_table, owner='Computer'):
        n = range(len(heuristic_table))
        h = None
        if owner == 'Computer':
            h = 0
            for i in n:
                for j in n:
                    piece = heuristic_table[i][j]
                    if piece is not None:
                        if piece.owner == 'Computer':
                            h += i
                        elif piece.owner == 'Player':
                            h -= (3 - i)
        return h

    def move(self, piece, position, local_table=None):
        if local_table is None:
            local_table = self.table
            piece.position['row'] = position[0]
            piece.position['col'] = position[1]
        n = range(len(local_table))
        for i in n:
            for j in n:
                if local_table[i][j] == piece:
                    local_table[i][j] = None
        local_table[position[0]][position[1]] = piece

    def get_piece(self, index, owner='Player'):
        n = range(len(self.table))
        for i in n:
            for j in n:
                piece = self.table[i][j]
                if piece is not None:
                    if piece.index == index and piece.owner == owner:
                        return piece
        return None

    def get_moves(self, piece):
        directions = [
            (-1, 1), (0, 1), (1, 1), (1, 0),
            (1, -1), (0, -1), (-1, -1), (-1, 0)
        ]
        h_max = None
        queue = []
        for direction in directions:
            row = piece.position['row'] + direction[0]
            col = piece.position['col'] + direction[1]
            if self.is_valid_move([row, col]):
                heuristic_table = deepcopy(self.table)
                self.move(piece, [row, col], heuristic_table)
                if h_max is None:
                    h_max = self.heuristics(heuristic_table)
                    queue = [(piece, (row, col))]
                else:
                    h = self.heuristics(heuristic_table)
                    if h > h_max:
                        h_max = h
                        queue = [(piece, (row, col))]
                    elif h == h_max:
                        queue.append((piece, (row, col)))

        return {"h_max": h_max, "queue": queue}

    def get_tables(self, piece, local_table=None):
        if local_table is None:
            local_table = self.table
        directions = [
            (-1, 1), (0, 1), (1, 1), (1, 0),
            (1, -1), (0, -1), (-1, -1), (-1, 0)
        ]
        queue = []
        for direction in directions:
            row = piece.position['row'] + direction[0]
            col = piece.position['col'] + direction[1]
            if self.is_valid_move([row, col], local_table):
                heuristic_table = deepcopy(local_table)
                self.move(piece, [row, col], heuristic_table)
                queue.append(heuristic_table)
        return queue

    def get_actions(self, local_table=None, owner='Computer'):
        if local_table is None:
            local_table = self.table
        n = range(len(local_table))
        queue = []
        for i in n:
            for j in n:
                piece = local_table[i][j]
                if piece is not None:
                    if piece.owner == owner:
                        queue.extend(self.get_tables(piece, local_table))
        return queue

    def computer_moves(self):
        n = range(len(self.table))
        queue = []
        for i in n:
            for j in n:
                piece = self.table[i][j]
                if piece is not None:
                    if piece.owner == 'Computer':
                        queue.append(self.get_moves(piece))
        h_max = None
        result = []
        for elem in queue:
            h = elem['h_max']
            if h_max is None:
                h_max = h
                result = elem['queue']

            elif h_max > h:
                h_max = h
                result = elem['queue']

            elif h_max == h:
                for val in elem['queue']:
                    result.append(val)

        move_no = random.randint(0, len(result) - 1)
        piece = result[move_no][0]
        positions = (result[move_no][1][0], result[move_no][1][1])
        self.move(piece, positions)

    def player_moves(self, index_str, move_str):
        directions = [
            (-1, -1), (0, -1), (1, -1), (1, 0),
            (1, 1), (0, 1), (-1, 1), (-1, 0)
        ]

        piece = self.get_piece(int(index_str))

        if piece is None:
            print('Index incorrect!')
            return False

        direction_index = None
        if move_str.upper() == 'NV':
            direction_index = 0
        elif move_str.upper() == 'N':
            direction_index = 1
        elif move_str.upper() == 'NE':
            direction_index = 2
        elif move_str.upper() == 'E':
            direction_index = 3
        elif move_str.upper() == 'SE':
            direction_index = 4
        elif move_str.upper() == 'S':
            direction_index = 5
        elif move_str.upper() == 'SV':
            direction_index = 6
        elif move_str.upper() == 'V':
            direction_index = 7
        positions = (
            piece.position['row'] + directions[direction_index][1],
            piece.position['col'] + directions[direction_index][0]
        )

        if self.is_valid_move(positions):
            self.move(piece, positions)
            return True

        print('Invalid move')
        return False

    def minimax(self, state=None, maximizer=True, depth=0, max_depth=2):
        if state is None:
            state = self.table

        if depth >= max_depth or self.is_final(state):
            return state, self.heuristics(state)

        if maximizer:
            value = -infinity
            for action in self.get_actions(state):
                _, h = self.minimax(action, False, depth + 1)
                return action, max(value, h)
        else:
            value = infinity
            for action in self.get_actions(state):
                _, h = self.minimax(action, True, depth + 1)
                return action, min(value, h)

    def minimaxAB(self, state=None, maximizer=True, depth=0, max_depth=2, alpha=-infinity, beta=infinity):
        if state is None:
            state = self.table

        if depth >= max_depth or self.is_final(state):
            return state, self.heuristics(state)

        if maximizer:
            value = -infinity
            for action in self.get_actions(state):
                _, h = self.minimaxAB(action, False, depth + 1, max_depth, alpha, beta)
                value = max(value, h)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
                return action, max(value, h)
        else:
            value = infinity
            for action in self.get_actions(state):
                _, h = self.minimaxAB(action, True, depth + 1, max_depth, alpha, beta)
                value = min(value, h)
                beta = min(beta, value)
                if beta <= alpha:
                    break
                return action, min(value, h)

    def minimax_wrapper(self):
        self.table, _ = self.minimax()

    def minimaxAB_wrapper(self):
        self.table, _ = self.minimaxAB()


if __name__ == '__main__':
    print('Initial State')
    table = Table()
    table.print()
    switch = random.randint(0, 1)

    while True:
        final = table.is_final()
        if final == 1:
            print('Player won!')
            break
        elif final == 2:
            print('Computer won!')
            break
        if switch == 0:
            print('Computer choice:')
            table.minimaxAB_wrapper()
            switch = 1
            table.print()
        elif switch == 1:
            print('Player choice:')
            x = input('What\'s your piece #number? ')
            y = input('Where to move your piece? ')
            a = table.player_moves(x, y)
            while not a:
                x = input('What\'s your piece #number? ')
                y = input('Where to move your piece? ')
                a = table.player_moves(x, y)
            else:
                switch = 0
                table.print()
