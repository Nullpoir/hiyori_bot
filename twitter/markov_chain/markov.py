import re
import MeCab
import pickle
from collections import deque
import random
import json
import os
from twitter.markov_chain.utils import gen_markov_model

class Markov_pass_error(Exception):
    pass

class Markov():
    order = 2
    def __init__(self,file=os.path.dirname(__file__)+"/model.pyd"):
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
        return utils.gen_markov_model(text,order)

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
