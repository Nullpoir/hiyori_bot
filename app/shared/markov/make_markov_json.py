from app.helpers import gen_markov_model
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

    i = open("source.md","r")
    o = open("source.txt","w")

    for line in i.readlines():
        line = line.strip("\n")
        if line[0] == "#":
            pass
        elif line[-1] != "。":
            o.write(line + "。\n")
        else:
            o.write(line + "\n")

    i.close()
    o.close()

    make_markov_json_model("source.txt",int(args[1]))
