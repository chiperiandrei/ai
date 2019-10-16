import random
import sys

sys.setrecursionlimit(9000)
R = +1  # right side
L = -1  # left side


# state = [boat_capacity, boat_side, m_no, c_no, m_no R, c_no R,  m_no L, c_no L]

# 0 - boat_capacity
# 1 - side
# 2 - m number
# 3 - c number
# 4 - m number on left side
# 5 - c number on left side
# 6 (-2) - m number on right side
# 7 (-1) - c number on right side


def initialize(boat_capacity, m_no, c_no):
    return [boat_capacity, R, m_no, c_no, m_no, c_no, 0, 0]


def is_final(state):
    if state[1] == L and state[4] == 0 and state[5] == 0 and state[-2] == state[2] and state[-1] == state[3]:
        return True
    return False


def transition(state, m, c):
    new_state = state.copy()
    new_state[1] = -1 * state[1]
    new_state[4] = new_state[4] + new_state[1] * m
    new_state[5] = new_state[5] + new_state[1] * c
    new_state[6] = new_state[6] - new_state[1] * m
    new_state[7] = new_state[7] - new_state[1] * c
    return new_state;


def validate(state, m, c):
    if m == 0 and c == 0:
        return False
    if state[4] < state[5]:
        return False
    if state[6] < state[7]:
        return False
    if m + c > state[0]:
        return False
    if state[1] == R:
        if state[-1] < 0 or state[-2] < 0:
            return False
    if state[1] == L:
        if state[4] < 0 or state[5] < 0:
            return False
    if m < c:
        return False
    return True


def view(index, state):
    if state[1] < 0:
        part = 'L'
    else:
        part = 'R'
    print('{}: {} {} {} {} ({})'.format(part, state[4], state[5], state[6], state[7], index))


def view_all_states(list_of_states):
    for index, state in enumerate(list_of_states):
        view(index, state)


def bktr_strategy(state, boat_capacity, m_no, c_no, k, p, path):
    for m in range(k, m_no + 1):
        for c in range(p, c_no + 1):
            if validate(state, m, c):
                state = transition(state, m, c)
                path.append(state)
                if is_final(state):
                    path.append(state)
                    break
                bktr_strategy(path[path.__len__() - 1], boat_capacity, m_no, c_no, m, c + 1, path)
            # else:
            #     bktr_strategy(state, boat_capacity, m_no, c_no, m, c, path)
    for c in path:
        print(view(1, c))
    path.clear()


if __name__ == '__main__':
    print("   M C M C")
    boat_capacity = 4
    m_no = 4
    c_no = 4
    path = []
    result = []
    state = initialize(boat_capacity, m_no, c_no)
    path.append(state)
    bktr_strategy(state, boat_capacity=3, m_no=4, c_no=4, k=0, p=0, path=path)
