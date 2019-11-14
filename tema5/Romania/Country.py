from random import randint


class Country:
    def __init__(self):
        self.counties = {
            "A": ["F", "D", "B", "X"],
            "D": ["A", "B", "C", "H"],
            "B": ["A", "D", "C"],
            "C": ["D", "I", "B"],
            "F": ["A", "G"],
            "G": ["F"],
            "H": ["D"],
            "I": ["C"],
            "X": ["A"]
        }

    def counties_with_maximum_neighbours(self):
        maximum_degree = 0
        county = None
        for key, value in self.counties.items():
            if len(value) > maximum_degree:
                maximum_degree = len(value)
                county = [key]
            elif len(value) == maximum_degree:
                county.append(key)
        return county

    def degree(self, county):
        return len(self.counties.get(county))

    def bkt(self, max_colors=3):
        def can_be_colored(_node, _color):
            for n in self.counties.get(_node):
                if _color == colors.get(n):
                    return False
            return True

        popular_neighbours = self.counties_with_maximum_neighbours()
        stack = [popular_neighbours[randint(0, len(popular_neighbours) - 1)]]

        visited = dict()
        for county in self.counties.keys():
            visited.update({county: False})
        visited.update({stack[-1]: True})

        colors = {stack[-1]: 1}

        print('Initial Stack: {}\nInitial Visited: {}\nInitial Colors: {}\n'.format(stack, visited, colors))
        print('__INITIAL END__')

        while stack:
            county = stack[-1]
            color = 1
            i_can_color = False

            neighbours = self.counties.get(county)
            neighbours.sort(key=self.degree, reverse=True)

            print('Neighbours of {}: {}'.format(county, neighbours))

            for neighbour in neighbours:
                if not visited.get(neighbour):
                    print('Neighbours of {}: {}'.format(neighbour, self.counties.get(neighbour)))

                    i_can_color = True
                    while not can_be_colored(neighbour, color) and i_can_color:
                        if color < max_colors:
                            color += 1
                        else:
                            i_can_color = False
                    if i_can_color:
                        visited.update({neighbour: True})
                        colors.update({neighbour: color})
                        stack.append(neighbour)
                        break

            if not i_can_color:
                stack.pop()

            print('Stack: {}\nVisited: {}\nColors: {}'.format(stack, visited, colors))
            print('{} Counties colored (out of {})'.format(len(colors), len(self.counties)))
            print('__ITERATION END__\n')

            if len(colors) == len(self.counties):
                print('Result:', colors)
                break

        return colors

    def other_bkt(self, max_colors=4):
        def can_be_colored(_node, _color):
            for n in self.counties.get(_node):
                if _color == colors.get(n):
                    return False
            return True

        def is_dangerous_color(_node, _color):
            for _ in self.counties.get(_node):
                if _color in dangerous_colors.get(_node):
                    return True
            return False

        def are_all_neighbours_visited(_node, _neighbours=None):
            if _neighbours is None:
                _neighbours = self.counties.get(_node)
            for i in neighbours:
                if not visited.get(i):
                    return False
            return True

        center_county = self.counties_with_maximum_neighbours()

        stack = [{
            'county': center_county[randint(0, len(center_county) - 1)],  # In our case BV
            'color': 1
        }]

        colors = {stack[-1].get('county'): 1}

        dangerous_colors = dict()

        visited = dict()

        for county in self.counties.keys():
            dangerous_colors.update({county: []})
            visited.update({county: False})

        visited.update({stack[-1].get('county'): True})

        print('Stack: {}\nVisited: {}\nColors: {}'.format(stack, visited, colors))
        print('__INITIAL END__')

        county = stack[-1].get('county')
        neighbours = self.counties.get(county)
        neighbours.sort(key=self.degree, reverse=True)

        while stack:
            for neighbour in neighbours:
                if not visited.get(neighbour):
                    color = 1
                    verdict = True
                    while is_dangerous_color(neighbour, color) or not can_be_colored(neighbour, color):
                        if color < max_colors:
                            color += 1
                        else:
                            verdict = False
                            break

                    if verdict:
                        colors.update({neighbour: color})
                        visited.update({neighbour: True})
                        stack.append({'county': neighbour, 'color': color})
                    else:
                        last_county = stack[-1].get('county')
                        temp = dangerous_colors.get(last_county)
                        temp.append(stack[-1].get('color'))

                        if len(stack) > 1:
                            colors.pop(last_county)
                            visited.update({last_county: False})
                            dangerous_colors.update({last_county: temp})
                            stack.pop()
                            break

            index = 0
            check = True
            while index < len(neighbours):
                if not are_all_neighbours_visited(county, neighbours):
                    county = neighbours[index]
                    check = False
                    break
                index += 1
                neighbours = self.counties.get(county)
                neighbours.sort(key=self.degree, reverse=True)

            if check:
                for node, is_visited in visited.items():
                    if not is_visited:
                        neighbours = self.counties.get(node)
                        neighbours.sort(key=self.degree, reverse=True)
                        for n in neighbours:
                            if visited.get(n):
                                county = n
                                break
                        break

            print('Stack: {}\nVisited: {}\nColors: {}'.format(stack, visited, colors))
            print('{} Counties colored (out of {})'.format(len(colors), len(self.counties)))
            print('__ITERATION END__\n')

            if len(colors) == len(self.counties):
                print('Result:', colors)
                break

        return colors


if __name__ == '__main__':
    country = Country()
    country.other_bkt(4)

    # Verify if your graph has all arcs correct
    # for key, value in RO.counties.items():
    #     for county in value:
    #         if key not in RO.counties.get(county):
    #             print(key, value)
    #             print(county, RO.counties.get(county))
