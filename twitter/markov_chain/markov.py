import re
import MeCab
from collections import deque
import random
import json
import os
import pickle
import re
import MeCab
from collections import deque
import json

def gen_markov_model(text,order):
    model = {}
    wordlist = wakati(text)
    queue = deque([], order)
    queue.append("[BOS]")
    for markov_value in wordlist:
        if len(queue) == order:
            if queue[-1] == "。":
                markov_key = tuple(queue)
                if markov_key not in model:
                    model[markov_key] = []
                model[markov_key].append("[BOS]")
                queue.append("[BOS]")

            markov_key = tuple(queue)
            if markov_key not in model:
                model[markov_key] = []
            model[markov_key].append(markov_value)
        queue.append(markov_value)
    return model

def wakati(text):
    t = MeCab.Tagger("-Owakati")
    parsed_text = ""
    for one_line_text in one_sentence_generator(text):
        parsed_text += " "
        parsed_text += t.parse(one_line_text)
    wordlist = parsed_text.rstrip("\n").split(" ")
    return wordlist

def one_sentence_generator(long_text):
    sentences = re.findall(".*?。", long_text)
    for sentence in sentences:
        yield sentence

class Markov_pass_error(Exception):
    pass

class Markov():
    order = 2
    def __init__(self,file):
        ext = os.path.splitext(file)[1]
        if ext == '.txt':
            f = open(file,'r')
            text = f.read()
            f.close()
            self.__model = self.__make_model(text,self.order)
        elif ext == '.pyd':
            f = open(file, 'rb')
            self.__model = pickle.load(f)
        else:
            raise Markov_pass_error('.txtか.jsonファイルでどうぞ')


    def __make_model(self,text,order):
        return gen_markov_model(text,order)

    def make_sentence(self,sentence_num=1, seed="[BOS]", max_words = 1000):
        sentence_count = 0

        key_candidates = [key for key in self.__model if key[0] == seed]
        if not key_candidates:
            print("Not find Keyword")
            return
        markov_key = random.choice(key_candidates)
        queue = deque(list(markov_key), self.order)

        sentence = "".join(markov_key)
        for _ in range(max_words):
            markov_key = tuple(queue)
            next_word = random.choice(self.__model[markov_key])
            sentence += next_word
            queue.append(next_word)

            if next_word == "。":
                sentence_count += 1
                if sentence_count == sentence_num:
                    break
        return sentence.rstrip("。")



if __name__ == "__main__":
    markov = Markov("./model.pyd")
    sentence = markov.make_sentence()
    print(sentence)
