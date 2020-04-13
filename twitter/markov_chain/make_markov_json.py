from markov_generate import *
import sys
import pickle

def make_markov_json_model(file,order):
    ifp = open(file)
    ofp = open('./model.pyd', 'wb')
    text = ifp.read()
    json_model = gen_markov_model(text,order)
    print(json_model)
    pickle.dump(json_model,ofp)
    ifp.close()
    ofp.close()

if __name__=='__main__':
    args = sys.argv
    make_markov_json_model(args[1],int(args[2]))
