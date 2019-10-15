import random

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
    return True


def view(name, state):
    print(name, end=' ')
    if state[1] < 0:
        print('L', end=': ')
    else:
        print('R', end=': ')
    print(state[4], state[5], state[6], state[7])


def random_strategy(boat_capacity, m_no, c_no):
    state = initialize(boat_capacity, m_no, c_no)
    view('', state)
    m = random.randint(0, m_no)
    c = random.randint(0, c_no)
    while not is_final(state):
        new_state = transition(state, m, c)
        if validate(new_state, m, c):
            state = new_state
            view('', state)
        m = random.randint(0, m_no)
        c = random.randint(0, c_no)


if __name__ == '__main__':
    print("    M C M C")
    random_strategy(boat_capacity=2, m_no=4, c_no=3)

    # state = initialize(boat_capacity=6, m_no=4, c_no=3)
    # state = [6, -1, 4, 3, 0, 0, 4, 3]

    # if validate(STATE, 1, 1):
    #     transition(STATE, 1, 1)  # RIGHT ---> LEFT
    # view('S2 =', STATE)
    # if validate(STATE, 1, 1):
    #     transition(STATE, 1, 1)  # LEFT ---> RIGHT
    # view('S3 =', STATE)
