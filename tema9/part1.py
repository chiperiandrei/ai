from nltk.corpus import wordnet

# 01.
# 02.
# achieved in part1.py


if __name__ == '__main__':
    separator = "="
    word = "cat"
    synsets = wordnet.synsets(word)
    print("input", separator, word)
    print("synsets", separator, synsets, "\n")

    for synset in synsets:
        print("synset", separator, synset)
        print("name", separator, synset.name().split('.', 1)[0])
        print("definition", separator, synset.definition())
        print("hypernyms", separator, synset.hypernyms())
        print("first hypernym synset", separator, synset.hypernyms()[0])
        print("first hypernym lemma", separator, synset.hypernyms()[0].lemmas()[0])
        print("hyponyms", separator, synset.hyponyms())
        if len(synset.hyponyms()):
            print("first hyponyms synset", separator, synset.hyponyms()[0])
            print("first hyponyms lemma", separator, synset.hyponyms()[0].lemmas()[0])
        print()
