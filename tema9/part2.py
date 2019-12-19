import os
import re
from nltk.corpus import wordnet as wn

# 03.
# achieved in part2.py


def str_tok(string, separators=r" .,:!?='\-\"\r\n"):
    regex = r"[{}]".format(separators)
    return [word for word in re.split(regex, string) if len(word) > 0]


def get_first_noun_hypernym(word):
    synsets = wn.synsets(word, 'n')
    if len(synsets):
        hypernyms = synsets[0].hypernyms()
        if len(hypernyms):
            return hypernyms[0].name().split('.', 1)[0]
    return None


def override_file(file_destination, file_source):
    with open(file_destination, 'w') as target, open(file_source) as backup:
        for line in backup:
            target.write(line)


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
            replacements = dict()
            # print(line.strip())
            line = ""

            for word in words:
                hypernym = get_first_noun_hypernym(word)
                if hypernym is not None:
                    replacements.update({word: hypernym})

            for index, word in enumerate(words):
                replacement = replacements.get(word)
                if replacement is not None:
                    word = replacement
                line += word + separators[index]
            if len(separators) > len(words):
                line += separators[-1]

            # print(line.strip())
            print(replacements)

            temp_file.write(line)

    override_file(file, path_temp_file)

    os.remove(path_temp_file)
    os.rmdir(path_temp_dir)


if __name__ == '__main__':
    # start(file='data/input.txt')
    start(file='data/input.txt', backup='data/backup.txt')