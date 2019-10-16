import random
import sys

sys.setrecursionlimit(9000)
R = +1  # right side
L = -1  # left side
allPossibleStates = []

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

def generateAllStates(current_state):
		nrM, nrC = 0, 0
		for i in range(0, boat_capacity+1):
			for j in range(0, boat_capacity+1):
				if validate(current_state,i,j):
					new_state = transition(current_state,i,j)
					allPossibleStates.append(new_state)
		return allPossibleStates
			   
def bktr_strategy(state,path):
	possible =[]
	possible = generateAllStates(state)
	if state in path:
	    bktr_strategy(path[len(path)-1], path)
	if is_final(state):
			path.append(state)
			return state
	else:
		for st in possible:
				path.append(st)
				bktr_strategy(st,path)	
	return path


if __name__ == '__main__':
		print("   M C M C")
		boat_capacity = 3
		m_no = 4
		c_no = 4
		path = []
		result = []
		state = initialize(boat_capacity, m_no, c_no)
		#path.append(state)
		result = bktr_strategy(state,path)
		view_all_states(result)
		
