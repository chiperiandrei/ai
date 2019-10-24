import sys
import io
import random
import math
import time
from threading import Thread

R = +1  # right side
L = -1  # left side

# state = [boat_capacity, boat_side, m_no, c_no, m_no L, c_no L,  m_no R, c_no R]

# 0      - boat_capacity
# 1      - side
# 2      - missionaries number
# 3      - cannibals number
# 4      - missionaries number on left side
# 5      - cannibals number on left side
# 6 (-2) - missionaries number on right side
# 7 (-1) - cannibals number on right side


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
    if state[4] < state[5] and state[4] != 0:
        return False
    if state[6] < state[7] and state[6] != 0:
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
    if index == 0:
        print('\n')
    if state[1] < 0:
        part = 'L'
    else:
        part = 'R'
    print('{}: {} {} {} {} ({})'.format(part, state[4], state[5], state[6], state[7], index))


def view_all_states(list_of_states):
    for index, state in enumerate(list_of_states):
        view(index, state)


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
    while cnt < len(graph):
        combinations(graph, graph.get_vertex_state(cnt))
        cnt += 1
    return graph


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

        checked = True
        for vortex in self.__dict:
            if is_final(vortex[1]):
                final_state_id = vortex[0]
                for i in vortex[2]:
                    if i < final_state_id:
                        checked = False
        if not checked:
            return -1

        old_stdout = sys.stdout
        buffer = sys.stdout = io.StringIO()

        for i in range(max_depth):
            if self.dls(initial_state_id, final_state_id, i):
                sys.stdout = old_stdout
                string = buffer.getvalue()
                moves = string.split(' ')
                moves.reverse()
                for index, element in enumerate(moves):
                    view(index, self.__dict[int(element)][1])
                    sys.stdout = old_stdout
                    buffer.close()
                return len(moves)
        sys.stdout = old_stdout
        buffer.close()
        return -1

    def test_iddfs(self, max_depth=None):
        if max_depth is None:
            max_depth = self.__dict[0][1][2] + self.__dict[0][1][3]

        while 1 and max_depth < 30:
            result = self.iddfs(max_depth)
            if result != -1:
                return result
            max_depth += 1
        return -1

    def a_star(self):
        initial_state = self.__dict[0][1]
        key = str(initial_state)
        distances, parent_of = {key: 0}, {key: None}
        queue = [initial_state]

        while queue:
            state = queue.pop()
            key = str(state)

            if is_final(state):
                full_path = [state]
                while parent_of[str(full_path[-1])] is not None:
                    full_path.append(parent_of[str(full_path[-1])])
                full_path.reverse()
                view_all_states(full_path)
                return len(full_path)

            for m_no in range(initial_state[2]):
                for c_no in range(initial_state[3]):
                    new_state = transition(state, m_no, c_no)
                    new_key = str(new_state)
                    add_to_queue = False
                    if validate(new_state, m_no, c_no):
                        if new_key not in distances:
                            add_to_queue = True
                        elif distances[key] + 1 < distances[new_key]:
                            add_to_queue = True
                    if add_to_queue:
                        distances[new_key] = distances[key] + 1
                        parent_of[new_key] = state
                        queue.append(new_state)

            queue.sort(
                reverse=True,
                key=lambda state, : distances[str(state)] + (state[4] + state[5] / 1)  # / 2
            )


def random_strategy(boat_capacity, m_no, c_no):
    state = initialize(boat_capacity, m_no, c_no)
    list_of_states = [state]

    count = 0

    while not is_final(state):
        m = random.randint(0, m_no)
        c = random.randint(0, c_no)

        new_state = transition(state, m, c)

        if validate(new_state, m, c):
            if new_state not in list_of_states:
                state = new_state
                list_of_states.append(state)

        count += 1
        if count >= 10**3:
            count = 0
            state = initialize(boat_capacity, m_no, c_no)
            list_of_states = [state]

    view_all_states(list_of_states)

    return len(list_of_states)


def bktr_strategy(state, path):
    if is_final(state):
        view_all_states(path)
        quit()
    else:
        for i in range(state[0] + 1):
            for j in range(i, state[0] + 1):
                if validate(state, i, j):
                    new_state = transition(state, i, j)
                    if new_state not in path:
                        path.append(new_state)
                        bktr_strategy(new_state, path)
                        path.pop()


if __name__ == '__main__':
    old_stdout = sys.stdout

    random_boat_capacity, random_m_no, random_c_no = 5, 7, 6
    a_star_times = []
    iddfs_times = []
    bkt_times = []
    random_times = []

    for index in range(10):
        file_name = 'instance%s.txt' % str(index)
        file = open(file_name, 'w+')

        random_m_no = random.randint(3, 15)
        random_c_no = random.randint(3, random_m_no)
        random_boat_capacity = random.randint(3, 5)

        sys.stdout = old_stdout
        print('Instance {}: bc = {}, m = {}, c = {}'.format(index, random_boat_capacity, random_m_no, random_c_no))

        file_buffer = sys.stdout = io.StringIO()

        lines = '-' * 10
        condition = True

        print('\n{} Initial conditions {}'.format(lines, lines))
        print('\nb = {}\nm = {}\nc = {}'.format(random_boat_capacity, random_m_no, random_c_no))

        print('\n{} iddfs strategy {}'.format(lines, lines), end='')
        start_time1 = time.time()
        GRAPH = initialize_graph(initialize(random_boat_capacity, random_m_no, random_c_no))
        start_time2 = time.time()
        iddfs_moves_no = GRAPH.test_iddfs()
        end_time = time.time()
        if iddfs_moves_no != -1:
            print("moves =", iddfs_moves_no)
            print(end_time - start_time1, 's')
            print(end_time - start_time2, 's')
            iddfs_times.append(end_time - start_time2)
        else:
            print("\nI can not find a path, check your instance data!")
            condition = False

        print('\n{} A* strategy {}'.format(lines, lines), end='')
        start_time = time.time()
        a_star_moves_no = GRAPH.a_star()
        end_time = time.time()
        if condition:
            print("moves =", a_star_moves_no)
            print(end_time - start_time, 's')
            a_star_times.append(end_time - start_time)
        else:
            print("\nI can not find a path, check your instance data!")
            condition = False

        print('\n{} bkt strategy {}'.format(lines, lines), end='')
        if condition:
            start_time = time.time()
            path = [initialize(random_boat_capacity, random_m_no, random_c_no)]
            thread = Thread(target=bktr_strategy, args=(path[0], path))
            thread.start()
            thread.join()
            end_time = time.time()
            print("moves =", len(path))
            print(end_time - start_time, 's')
            bkt_times.append(end_time - start_time)
        else:
            print("\nI can not find a path, check your instance data!")

        print('\n{} random strategy {}'.format(lines, lines), end='')
        if condition:
            if random_m_no <= 10 and random_c_no <= 10:
                start_time = time.time()
                random_moves_no = random_strategy(random_boat_capacity, random_m_no, random_c_no)
                end_time = time.time()
                print("moves =", random_moves_no)
                print(end_time - start_time, 's')
                random_times.append(end_time - start_time)
            else:
                print('\nI can not perform my strategy if there are big values for missionaries and cannibals')
        else:
            print("\nI can not find a path, check your instance data!")

        file.write(file_buffer.getvalue())
        file_buffer.close()

    sys.stdout = old_stdout

    iddfs_time, a_star_time, bkt_time, random_time = 0, 0, 0, 0

    if len(iddfs_times):
        iddfs_time = sum(iddfs_times) / len(iddfs_times)
    if len(a_star_times):
        a_star_time = sum(a_star_times) / len(a_star_times)
    if len(bkt_times):
        bkt_time = sum(bkt_times) / len(bkt_times)
    if len(random_times):
        random_time = sum(random_times) / len(random_times)

    print('\nAvg. time for:')
    print('Iddfs: {}s ({})\nA*: {}s ({})\nBkt: {}s ({})\nRandom: {}s ({})\n'.format(
        iddfs_time, len(iddfs_times),
        a_star_time, len(a_star_times),
        bkt_time, len(bkt_times),
        random_time, len(random_times)
    ))
