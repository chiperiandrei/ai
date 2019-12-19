from part2 import *

# 04.
# achieved in part2.py


def get_first_noun_synset(word):
    synsets = wn.synsets(word, 'n')
    if len(synsets):
        return synsets[0]
    return None


def get_maximum_semantic_distance(synsets):
    length = len(synsets)
    distances = set()
    for i in range(0, length - 1):
        for j in range(i + 1, length):
            d = synsets[i].shortest_path_distance(synsets[j])
            print(synsets[i], synsets[j], d)
            distances.add(d)
    print()
    if len(distances):
        return max(distances)
    return None


def start(file, backup=None):
    if backup is not None:
        override_file(file, backup)

    path_temp_dir = os.path.join(os.getcwd(), 'temp')
    path_temp_file = os.path.join(path_temp_dir, 'temp.txt')

    os.mkdir(path_temp_dir)

    with open(file) as input_file, open(path_temp_file, 'w') as temp_file:
        for line in input_file:
            words = str_tok(line)
            separators = str_tok(line, r'\w+')
            synsets = list()
            replacements = dict()
            line = ""

            for word in words:
                synset = get_first_noun_synset(word)
                if synset is not None:
                    synsets.append(synset)
                    hypernym = get_first_noun_hypernym(word)
                    if hypernym is not None:
                        replacements.update({word: hypernym})

            for index, word in enumerate(words):
                replacement = replacements.get(word)
                if replacement is not None:
                    word = replacement
                line += word
                if index < len(separators) - 1:
                    line += separators[index]

            if len(separators) == len(words):
                max_distance = get_maximum_semantic_distance(synsets)
                if max_distance is not None:
                    line += ' {}\n'.format(max_distance)

            if len(separators) > len(words):
                line += separators[-1]

            temp_file.write(line)

    override_file(file, path_temp_file)
    os.remove(path_temp_file)
    os.rmdir(path_temp_dir)


if __name__ == '__main__':
    # start(file='data/input.txt')
    start(file='data/input.txt', backup='data/backup.txt')
