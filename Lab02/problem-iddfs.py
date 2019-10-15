import sys
import io

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


class Graph:
    def __init__(self, root_state):
        self.__dict = [[0, root_state, []]]

    def add_vertex(self, state):
        for vertex in self.__dict:
            if vertex[1] == state:
                return False
        self.__dict.append([len(self.__dict), state, []])
        return True

    def add_edge(self, state, new_state):
        for index, vertex1 in enumerate(self.__dict):
            if vertex1[1] == state:
                for vertex2 in self.__dict:
                    if vertex2[1] == new_state:
                        if vertex1[0] < vertex2[0]:
                            vertex1[2].append(vertex2[0])

    def get_vertex_state(self, vertex_id):
        for vertex in self.__dict:
            if vertex[0] == vertex_id:
                return vertex[1]

    def __str__(self):
        result = ''
        for elem in self.__dict:
            result += str(elem) + '\n'
        return result

    def __len__(self):
        return len(self.__dict)

    def dls(self, initial_state_id, final_state_id, max_depth):
        if initial_state_id == final_state_id:
            print('%d' % initial_state_id, end='')
            return True

        if max_depth <= 0:
            return False

        for i in self.__dict[initial_state_id][2]:
            if self.dls(i, final_state_id, max_depth - 1):
                print(' %d' % initial_state_id, end='')
                return True
        return False

    def iddfs(self, max_depth):
        initial_state_id = 0
        final_state_id = None

        for vortex in self.__dict:
            if is_final(vortex[1]):
                final_state_id = vortex[0]

        old_stdout = sys.stdout
        buffer = sys.stdout = io.StringIO()

        for i in range(max_depth):
            if self.dls(initial_state_id, final_state_id, i):
                sys.stdout = old_stdout
                string = buffer.getvalue()
                buffer.close()

                moves = string.split(' ');
                moves.reverse()
                for index, element in enumerate(moves):
                    # print(int(element))
                    view(index, self.__dict[int(element)][1])
        sys.stdout = old_stdout
        return None


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
    return new_state


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


def view(index, state):
    if state[1] < 0:
        part = 'L'
    else:
        part = 'R'
    print('{}: {} {} {} {} ({})'.format(part, state[4], state[5], state[6], state[7], index))


def manage_graph_connection(graph, state, new_state):
    graph.add_vertex(new_state)
    graph.add_edge(state, new_state)


def combinations(graph, state):
    if state is not None:
        stack = [0]
        mask = list(range(state[2] + 1))
        while stack:
            if stack[-1] <= state[2]:
                stack[-1] += 1
                if len(stack) == 2:
                    m, c = mask[stack[0] - 1], mask[stack[1] - 1]
                    new_state = transition(state, m, c)
                    if validate(new_state, m, c):
                        manage_graph_connection(graph, state, new_state)
                else:
                    stack.append(0)
            else:
                stack.pop()


def initialize_graph(state):
    graph = Graph(state)
    cnt = 0
    # ACEST len(graph) se actualizeaza la fiecare iteratie #BeCarefull
    while cnt < len(graph):
        combinations(graph, graph.get_vertex_state(cnt))
        cnt += 1
    return graph


if __name__ == '__main__':
    GRAPH = initialize_graph(initialize(boat_capacity=6, m_no=4, c_no=3))
    # print(GRAPH)
    GRAPH.iddfs(4)
