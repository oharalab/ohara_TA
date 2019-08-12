import math

def score_BLUE(first, second):
    first = first.lower()
    second = second.lower()

def split_sentence(sentence, delimiter):
    return sentence.split(delimiter)

def split_document(doc):
    return doc.split("\n")

def split_string(string, delimiter=" ",method="doc"):
    # スペース，タブ は表現の幅が広すぎるので，対象外
    string = string.lower().replace(" ", "").replace("\t", "")
    #string = string.replace("-", "").replace(".", " .").replace(",", " ,")\
    #        .replace("(", " ( ").replace(")", " ) ").replace("[", " [ ").replace("]", " ] ")
    doc = split_document(string)
    stop_words = ["\n", "\r", ""]
    morphs = []
    for sentence in doc:
        sentence = split_sentence(sentence, delimiter)
        sentence = [word for word in sentence if word not in stop_words]
        #print(sentence)
        if method == "doc": # split document (all sentence)
            morphs.extend(sentence)
        else: # split every sentence
            morphs.append(sentence)

    return morphs

def calc_information(worddict, method):
    if method == "Huffman":
        all_num = sum([value for value in worddict.values()])
        keys = set(worddict.keys())
        info = sum([len(key)*worddict[key]/all_num for key in keys])
    else: # average word length
        info = sum([len(key)*value for key,value in worddict.items()])
    info = 1 / (info + 0.000001)
    return info

def calc_maxindex(information):
    max_info = 0
    index = 0
    for i,info in enumerate(information):
        if info > max_info:
            max_info = info
            index = i
    return index

def make_worddict(words):
    word_dict = dict()
    for word in words:
        if word not in word_dict.keys():
            word_dict[word] = 1
        else:
            word_dict[word] += 1
    return word_dict

def select_delimiter(doc, method = "Huffman"):
    candidates = [" ", ":", ";", "=", "\"", "/", "+", "*"] + [chr(i) for i in range(97,97+26)]
    information = []
    for cand in candidates:
        words = [word for sent in doc for word in sent.split(cand)]
        word_dict = make_worddict(words)
        info = calc_information(word_dict, method)
        information.append(info)

    index = calc_maxindex(information)
    delimiter = candidates[index]
    return delimiter

def make_ngram(morphs, N):
    return ["".join(morphs[i:i+N]) for i in range(0, len(morphs)-N+1)]

def BP(c, r): # penaltiy
    if c > r:
        return 1
    else:
        c += 0.00001
        return math.exp(1-r/c)

def compare(pre, ans, method="full"):
    if method == "full":
        if pre == ans:
            return 1
        else:
            return 0
    else: # similar to multiple 1-gram score
        mol = sum([1 if p == a else 0 for p in pre for a in ans])
        den = len(pre) * len(ans)
        return mol/den

def calc_BLEU(first, second, delimiter, weights = 5, N=4, method="doc"): # N value is normally 4
    first = split_string(first, delimiter, method)
    second = split_string(second, delimiter, method)
    #print("first", first)
    #print("second", second)
    if method=="doc":
        scores = []
        pena = BP(len(first), len(second))
        for n in range(1, N+1):
            first = make_ngram(first, n)
            second = make_ngram(second, n)
            pairs = [[f, s] for f in first for s in second]
            #print(pairs)
            mol = sum([compare(pair[0], pair[1]) for pair in pairs])
            den = len(first) * len(second)
            mol += 0.01 ** 2
            den += 0.01
            #print(mol, den, mol/den)
            scores.append(math.log(mol/den*weights)/N)
        #print(pena)
        #print(scores)
        #print(sum(scores))
        #print(math.exp(sum(scores)))
        return pena*math.exp(sum(scores))#- pena * math.exp(sum([math.log(0.000001)/n for n in range(1, N+1)]))
    else:
        print("sorry, it is not made yet")
        #return [first, second]
