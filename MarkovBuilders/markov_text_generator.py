import random
from MarkovBuilders import hashmap_open_resizable



def make_hashtable():
    words = hashmap_open_resizable.HashMap()
    f = "I hope to learn a ton this year. I would like to learn about a civilization from the past year."
    for word in f.split():
        word = word.strip(",.\"\';:-!?()").lower()
        if hashmap_open_resizable.contains(words, word):
            hashmap_open_resizable.put(words, word, hashmap_open_resizable.get(words, word) + 1)
        else:
            hashmap_open_resizable.put(words, word, 1)

    word = hashmap_open_resizable.put(words, "test", 1)
    if hashmap_open_resizable.contains(words, "test"):
        print(words)


def make_hashtable_depth2():
    words = hashmap_open_resizable.HashMap()
    sentence = []
    with open("sex.txt") as f:
        for line in f:
            new_line = line.split()
            for i in range(0, len(new_line)):
                new_line[i] = new_line[i].strip(",.\"\';:-!?()").lower()
                sentence.append(new_line[i])
    with open("bible.txt") as f:
        for line in f:
            new_line = line.split()
            for i in range(0, len(new_line)):
                new_line[i] = new_line[i].strip(",.\"\';:-!?()").lower()
                sentence.append(new_line[i])
    for i in range(0, len(sentence)):
        word = sentence[i]
        try:
            if hashmap_open_resizable.contains(words, word):
                following = hashmap_open_resizable.get(words, word)
                if hashmap_open_resizable.contains(following, sentence[i+1]):
                    second = hashmap_open_resizable.get(following, sentence[i+1])
                    second.append(sentence[i+2])
                else:
                    second = [sentence[i+2]]
                hashmap_open_resizable.put(following, sentence[i + 1], second)
                hashmap_open_resizable.put(words, word, following)
            else:
                following = hashmap_open_resizable.HashMap()
                second = [sentence[i+2]]
                hashmap_open_resizable.put(following, sentence[i+1], second)
                hashmap_open_resizable.put(words, word, following)
        except IndexError:
            return words


def make_hashtable_depth3():
    words = hashmap_open_resizable.HashMap()
    sentence = []
    with open("alice.txt") as f:
        for line in f:
            new_line = line.split()
            for i in range(0, len(new_line)):
                new_line[i] = new_line[i].strip(",.\"\';:-!?()").lower()
                sentence.append(new_line[i])
    for i in range(0, len(sentence)):
        word = sentence[i]
        try:
            if hashmap_open_resizable.contains(words, word):
                following = hashmap_open_resizable.get(words, word)
                if hashmap_open_resizable.contains(following, sentence[i+1]):
                    second = hashmap_open_resizable.get(following, sentence[i+1])
                    if hashmap_open_resizable.contains(second, sentence[i+2]):
                        third = hashmap_open_resizable.get(second, sentence[i+2])
                        third.append(sentence[i+3])
                    else:
                        third = [sentence[i+3]]
                else:
                    second = hashmap_open_resizable.HashMap()
                    third = [sentence[i+3]]
                hashmap_open_resizable.put(second, sentence[i + 2], third)
                hashmap_open_resizable.put(following, sentence[i + 1], second)
                hashmap_open_resizable.put(words, word, following)
            else:
                following = hashmap_open_resizable.HashMap()
                second = hashmap_open_resizable.HashMap()
                third = [sentence[i+3]]
                hashmap_open_resizable.put(second, sentence[i+2], third)
                hashmap_open_resizable.put(following, sentence[i+1], second)
                hashmap_open_resizable.put(words, word, following)
        except IndexError:
            return words


def seed_text(sentence, filename):
    with open(filename) as f:
        for line in f:
            new_line = line.split()
            for i in range(0, len(new_line)):
                new_line[i] = new_line[i].strip(",.\"\';:-!?()").lower()
                sentence.append(new_line[i])
    print(sentence)
    return sentence


def make_hashtable_depth(n: int, sentence):
    words = hashmap_open_resizable.HashMap()
    for word in range(0, len(sentence)):
        try:
            make_hashtable_rec(n, words, 0, sentence, word)
        except IndexError:
            print("Out of range.")
    return words


def make_hashtable_rec(n:int, words, l:int, sentence:list, word:int):
    if n == 0:
        return [(sentence[word + l])]
    else:
        if hashmap_open_resizable.contains(words, sentence[word+l]):
            following = hashmap_open_resizable.get(words, sentence[word + l])
            if type(following) == list:
                hashmap_open_resizable.put(words, sentence[word + l], following + (make_hashtable_rec(n-1, words, l+1, sentence, word)))
                return words
            else:
                hashmap_open_resizable.put(words, sentence[word + l], make_hashtable_rec(n-1, following, l+1, sentence, word))
                return words
        else:
            if n > 1:
                following = hashmap_open_resizable.HashMap()
            else:
                following = []
            hashmap_open_resizable.put(words, sentence[word + l], following)
            return make_hashtable_rec(n, words, l, sentence, word)


def make_hashtable_nback(n: int, sentence):
    words = hashmap_open_resizable.HashMap()
    for word in range(0, len(sentence) - n):
        phrase = ""
        for i in range(0, n):
            phrase += sentence[word + i] + " "
        if hashmap_open_resizable.contains(words, phrase):
            following = hashmap_open_resizable.get(words, phrase)
            following.append(sentence[word + n])
            hashmap_open_resizable.put(words, phrase, following)
        else:
            hashmap_open_resizable.put(words, phrase, [sentence[word + n]])
    return words


def make_hashtable_list():
    words = hashmap_open_resizable.HashMap()
    sentence = []
    with open('atotc.txt') as f:
        for line in f:
            new_line = line.split()
            for i in range(0, len(new_line)):
                new_line[i] = new_line[i].strip(",.\"\';:-!?()").lower()
                sentence.append(new_line[i])
    for i in range(0, len(sentence)):
        word = sentence[i]
        try:
            if hashmap_open_resizable.contains(words, word):
                following = hashmap_open_resizable.get(words, word)
                following.append(sentence[i+1])
            else:
                following = [sentence[i+1]]
            hashmap_open_resizable.put(words, word, following)
        except IndexError:
            return words


def predict_next(words, word)->str:
    following = hashmap_open_resizable.get(words, word)
    return following[random.randint(0,len(following)-1)]


def predict_next_2back(words, word, word2)->str:
    following = hashmap_open_resizable.get(words, word)
    second = hashmap_open_resizable.get(following, word2)
    return second[random.randint(0,len(second)-1)]


def predict_next_3back(words, word, word2, word3):
    following = hashmap_open_resizable.get(words, word)
    second = hashmap_open_resizable.get(following, word2)
    third = hashmap_open_resizable.get(second, word3)
    return third[random.randint(0, len(third)-1)]


def predict_next_nback(words, sequence:list):
    following = hashmap_open_resizable.get(words, sequence[0])
    sequence.pop(0)
    if type(following) == list:
        return following[random.randint(0, len(following)-1)]
    else:
        return predict_next_nback(following, sequence)


"""
def predict_next_nback(words,sequence):
    phrase = ""
    for i in range(0, len(sequence)):
        phrase += sequence[i] + " "
    following = hashmap_open_resizable.get(words, phrase)
    return following[random.randint(0, len(following)-1)]
"""


def build_sentence(words, word, length):
    sentence = ""
    for i in range(0, length):
        word = predict_next(words, word)
        sentence += word + " "
    return sentence


def build_sentence_2back(words, word, word2, length):
    sentence = ""
    for i in range(0, length):
        temp = word2
        word2 = predict_next_2back(words, word, word2)
        word = temp
        sentence += word + " "
    return sentence


def build_sentence_3back(words, word, word2, word3, length):
    sentence = ""
    for i in range(0, length):
        temp = word3
        word3 = predict_next_3back(words, word, word2, word3)
        word = word2
        word2 = temp
        sentence += word + " "
    return sentence


def build_sentence_nback(words, sequence, seqlen, length):
    sentence = ""
    for i in range(0, length):
        seq = sequence[:]
        sequence.append(predict_next_nback(words, seq))
        if len(sequence) > seqlen:
            sequence.pop(0)
            sentence += sequence[len(sequence)-1] + " "
    return sentence


def main():
    sentence = seed_text([], 'books/atotc.txt') + seed_text([], 'books/alice.txt')
    seed = ['it', 'was', 'the']
    nback = 3
    words = make_hashtable_depth(nback, sentence)
    cont = 1
    while cont != 0:
        print(build_sentence_nback(words, seed, nback, 25))
        cont = int(input())

main()