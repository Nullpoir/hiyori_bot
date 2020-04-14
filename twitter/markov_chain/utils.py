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
