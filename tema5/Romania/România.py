from random import randint
import pygame
import os


class Country:
    def __init__(self):
        self.counties = {
            "B": ["IF"],
            "AB": ["AR", "BH", "CJ", "HD", "MS", "SB", "VL"],  # Alba
            "AR": ["AB", "BH", "HD", "TM"],  # Arad
            "AG": ["BV", "DB", "OT", "SB", "TR", "VL"],  # Argeș
            "BC": ["CV", "HR", "NT", "VN", "VS"],  # Bacău
            "BH": ["AB", "AR", "CJ", "SJ", "SM"],  # Bihor
            "BN": ["CJ", "MM", "MS", "SV"],  # Bistrița-Năsăud
            "BT": ["IS", "SV"],  # Botoșani
            "BV": ["AG", "BZ", "CV", "DB", "HR", "MS", "PH", "SB"],  # Brașov
            "BR": ["BZ", "CT", "GL", "IL", "TL", "VN"],  # Brăila
            "BZ": ["BR", "BV", "CV", "IL", "PH", "VN"],  # Buzău
            "CS": ["GJ", "HD", "MH", "TM"],  # Caraș-Severin
            "CL": ["CT", "GR", "IF", "IL"],  # Călărași
            "CJ": ["AB", "BH", "BN", "MM", "MS", "SJ"],  # Cluj
            "CT": ["BR", "CL", "IL", "TL"],  # Constanța
            "CV": ["BC", "BV", "BZ", "HR", "VN"],  # Covasna
            "DB": ["AG", "BV", "GR", "IF", "PH", "TR"],  # Dâmbovița
            "DJ": ["GJ", "MH", "OT", "VL"],  # Dolj
            "GL": ["BR", "TL", "VN", "VS"],  # Galați
            "GR": ["CL", "DB", "IF", "TR"],  # Giurgiu
            "GJ": ["CS", "DJ", "HD", "MH", "VL"],  # Gorj
            "HR": ["BC", "BV", "CV", "NT", "MS", "SV"],  # Harghita
            "HD": ["AB", "AR", "CS", "GJ", "TM", "VL"],  # Hunedoara
            "IL": ["BR", "BZ", "CL", "CT", "IF", "PH"],  # Ialomița
            "IS": ["BT", "NT", "SV", "VS"],  # Iași
            "IF": ["B", "CL", "DB", "GR", "IL", "PH"],  # Ilfov
            "MM": ["BN", "CJ", "SJ", "SM", "SV"],  # Maramureș
            "MH": ["CS", "DJ", "GJ"],  # Mehedinți
            "MS": ["AB", "BN", "BV", "CJ", "HR", "SB", "SV"],  # Mureș
            "NT": ["BC", "HR", "IS", "SV", "VS"],  # Neamț
            "OT": ["AG", "DJ", "TR", "VL"],  # Olt
            "PH": ["BV", "BZ", "DB", "IF", "IL"],  # Prahova
            "SM": ["BH", "MM", "SJ"],  # Satu Mare
            "SJ": ["BH", "CJ", "MM", "SM"],  # Sălaj
            "SB": ["AB", "AG", "BV", "MS", "VL"],  # Sibiu
            "SV": ["BN", "BT", "HR", "IS", "MM", "MS", "NT"],  # Suceava
            "TR": ["AG", "DB", "GR", "OT"],  # Teleorman
            "TM": ["AR", "CS", "HD"],  # Timiș
            "TL": ["BR", "CT", "GL"],  # Tulcea
            "VS": ["BC", "GL", "IS", "NT", "VN"],  # Vaslui
            "VL": ["AB", "AG", "DJ", "GJ", "HD", "OT", "SB"],  # Vâlcea
            "VN": ["BC", "BR", "BZ", "CV", "GL", "VS"],  # Vrancea
        }

        self.screen = None

    """
    :returns a list of the counties that have the most neighbors
    """
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

    """
    :returns the number of neighbors of a county
    """
    def degree(self, county):
        return len(self.counties.get(county))

    """
    :returns a dictionary witch have:
    the keys equal with county
    the values equal with a number, representing the index of a color
    
    this bkt visits most popular county (with maximum number of neighbours)
    then it visits the most popular neighbours, and so on
    """
    def bkt1(self, max_colors):
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

    """
    :returns a dictionary witch have:
    the keys equal with county
    the values equal with a number, representing the index of a color
    
    this bkt visits most popular county (with maximum number of neighbours)
    then it visits all the neighbours of the most popular county
    then it select another popular county and visits their neighbours, and so on
    """
    def bkt2(self, max_colors=4):
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

    def map(self, colors, delay):
        county_position = {
            "B": [377, 358],
            "AB": [205, 195],  # Alba
            "AR": [100, 190],  # Arad
            "AG": [285, 300],  # Argeș
            "BC": [410, 180],  # Bacău
            "BH": [120, 120],  # Bihor
            "BN": [265, 105],  # Bistrița-Năsăud
            "BT": [410, 50],  # Botoșani
            "BV": [310, 240],  # Brașov
            "BR": [470, 295],  # Brăila
            "BZ": [410, 285],  # Buzău
            "CS": [105, 295],  # Caraș-Severin
            "CL": [440, 375],  # Călărași
            "CJ": [205, 145],  # Cluj
            "CT": [515, 365],  # Constanța
            "CV": [360, 225],  # Covasna
            "DB": [325, 315],  # Dâmbovița
            "DJ": [205, 380],  # Dolj
            "GL": [475, 235],  # Galați
            "GR": [360, 390],  # Giurgiu
            "GJ": [190, 305],  # Gorj
            "HR": [330, 170],  # Harghita
            "HD": [165, 240],  # Hunedoara
            "IL": [445, 343],  # Ialomița
            "IS": [445, 105],  # Iași
            "IF": [373, 340],  # Ilfov
            "MM": [230, 62],  # Maramureș
            "MH": [156, 360],  # Mehedinți
            "MS": [270, 168],  # Mureș
            "NT": [380, 130],  # Neamț
            "OT": [262, 370],  # Olt
            "PH": [365, 305],  # Prahova
            "SM": [168, 59],  # Satu Mare
            "SJ": [190, 105],  # Sălaj
            "SB": [250, 230],  # Sibiu
            "SV": [345, 70],  # Suceava
            "TR": [310, 390],  # Teleorman
            "TM": [70, 235],  # Timiș
            "TL": [525, 310],  # Tulcea
            "VS": [470, 170],  # Vaslui
            "VL": [240, 300],  # Vâlcea
            "VN": [415, 235],  # Vrancea
        }

        pygame.init()
        self.screen = pygame.display.set_mode((637, 480))
        self.screen.fill((255, 255, 255))

        pygame.display.set_caption('România', '')
        icon = pygame.image.load(os.path.join(os.getcwd(), '.assets', 'Icon.png'))
        pygame.display.set_icon(icon)

        image = pygame.image.load(os.path.join(os.getcwd(), '.assets', 'România.png'))
        self.screen.blit(image, (0, 0))

        font = pygame.font.Font(pygame.font.get_default_font(), 20)

        color_mapping = [
            (200, 0, 0),
            (0, 150, 0),
            (0, 0, 200),
            (200, 200, 0),
        ]

        for county, color_index in colors.items():
            text = font.render(county, False, color_mapping[color_index - 1])
            position = county_position.get(county)
            self.screen.blit(text, (position[0], position[1]))
            pygame.display.update()

            for i in range(60):
                pygame.time.wait(delay)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


if __name__ == '__main__':
    România = Country()
    România.map(România.bkt2(max_colors=4), delay=3)
