import re
import codecs

CLASS_A = "a à á ả ã ạ ă ằ ắ ẳ ẵ ặ â ầ ấ ẩ ẫ ậ af as ax aj ar aa aw aaf afa aas asa aax axa aaj aja aar ara awf afw aws asw  awr arw awx axw awj ajw".split()
CLASS_E = "e è é ẻ ẽ ẹ ê ề ế ể ễ ệ".split()
CLASS_I = "i ì í ỉ ĩ ị".split()
CLASS_O = "o ò ó ỏ õ ọ ô ồ ố ổ ỗ ộ ơ ờ ớ ở ỡ ợ".split()
CLASS_U = "u ù ú ủ ũ ụ ư ừ ứ ử ữ ự".split()
CLASS_Y = "y ỳ ý ỷ ỹ ỵ".split()
CLASS_D = "d đ".split()


# import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

# WORDS = Counter(words(open('big.txt').read()))


def load_telex_rule(path):
    """Load accent vietnamese """
    file = codecs.open(path, 'r', 'utf-8').read()
    f = file.splitlines()
    telex_rule = {line.split()[0] : line.split()[1] for line in codecs.open(path, 'r', 'utf-8').read().splitlines()}
    # rule  = [line.split()[0] for line in codecs.open(path, 'r', 'utf-8').read().splitlines()]
    # rule  = vocab.keys()
    return telex_rule
    
# Load Vietnamese vocab
WORDS = load_telex_rule("vocab.txt")

# def P(word, N=sum(WORDS.values())): 
    # "Probability of `word`."
    # return WORDS[word] / N
    

def load_big_text():
    wordDict = Counter()
    with codecs.open('datatrain.txt','r',encoding='utf-8') as f:
        for line in f:
            wordDict.update(line.strip().split())
        
    # for word, count in wordDict.most_common(): 
        # print (word, count)
    return wordDict

# btext = load_big_text()
# print(btext.most_common(10))

def probability(word):
    btext = load_big_text()
    N = sum(btext.values())
    print(btext[word] / N)
    return btext[word] / N
    
print(probability("băn"))
# print(w for w in btext if "cần" in w)
    
def telex_processor(word):
    "Process text before training"
    # Path to telex rule file
    path_to_telex = "telex2.txt"
    # rule = "af as ax aj ar aa aw aaf afa aas asa aax axa aaj aja aar ara awf afw aws asw  awr arw awx axw awj ajw".split()
    # Possible typo endword in Vietnamese
    ends = "a e o f s r x j w d".split()
    possible_words = []
    telex_rule = load_telex_rule(path_to_telex)
    
    
    if word[:2] in ["dd", "DD"]:
        word = telex_rule[word[:2]]+word[2:]
                
    if word[-2:] in ["oa", "ao", "oe", "eo"]:
        possible_words.append(word) 
                

    if len(word) > 2:
        if word[-2] in ends:  
            # TODO: Consider this error with word_length = 3, loi voi tu oa, ao, oe, eo
            if len(word) == 3:
                if word[0:2] in ["oa", "ao", "oe", "eo"] or word[1:] in ["oa", "ao", "oe", "eo"]:
                    if word[0] + word[2] in telex_rule:
                        chain = word[0] + word[2]
                        temp  = telex_rule[chain] + word[1]
                        possible_words.append(temp)
                    elif word[0] + word[2] in telex_rule:
                        chain = word[1] + word[2]
                        temp  = word [0] + telex_rule[chain]
                        possible_words.append(temp)
                    # else:

                else:
                    chain = str(word[1]+word[2])
                    if chain in telex_rule:
                        temp = word[0]+telex_rule[chain]
                        possible_words.append(temp)
                    else:
                        possible_words.append(word)
            else:
                for i in range(len(word)):
                    #the case dupplicate the cosidering letter
                    # print(word[i])
                    if i < len(word[:-1]) - 1:
                        # print(word[i])
                        # TODO: The case: uow -> ươ
                        if word[i:i+2] == "uo":                       
                            # if (word[i:i+2] + lett for lett in word[i+2:end]) in telex_rule:
                            if (word[i:i+2]+word[-2]+word[-1]) in telex_rule:
                                chain = str(word[i:i+2]+word[-2]+word[-1])
                                temp = word[:i]+telex_rule[chain]+word[i+2:-2]
                                possible_words.append(temp)
                                
                            elif (word[i:i+2]+word[-2]) in telex_rule:
                                chain = str(word[i:i+2]+word[-2])
                                temp = word[:i]+telex_rule[chain]+word[i+2:-2]+word[-1]
                                possible_words.append(temp)
                                
                        if (word[i]+word[-2]+word[-1]) in telex_rule:
                            chain = str(word[i]+word[-2]+word[-1])
                            temp = word[:i]+telex_rule[chain]+word[i+1:-2]
                            possible_words.append(temp)
                            
                        elif (word[i]+word[-2]) in telex_rule:
                            chain = str(word[i]+word[-2])
                            temp = word[:i]+telex_rule[chain]+word[i+1:-2]+word[-1]
                            # print(temp)
                            possible_words.append(temp)
                            
                        elif(word[i] + word[-1]) in telex_rule:
                            chain = str(word[i]+word[-1])
                            temp = word[:i]+telex_rule[chain]+word[i+1:-1]
                            possible_words.append(temp)
                            
                    else:
                        # print(word[i])
                        if(word[i] + word[-1]) in telex_rule:
                            chain = str(word[i]+word[-1])
                            temp = word[:i]+telex_rule[chain]+word[i+1:-1]
                            possible_words.append(temp)
                            
                        else:
                            possible_words.append(word)
                    
        elif word[-1] in ends:
            for i in range(len(word)):
                if (i < len(word)-1):
                    # TODO: The case: uow -> ươ
                    if word[i:i+2] == "uo":                       
                        # if (word[i:i+2] + lett for lett in word[i+2:end]) in telex_rule:
                        if (word[i:i+3]+word[-1]) in telex_rule:
                            chain = str(word[i:i+3]+word[-1])
                            temp = word[:i]+telex_rule[chain]+word[i+3:-1]
                            possible_words.append(temp)
                            
                        elif (word[i:i+2]+word[-1]) == "uow":
                            temp = word[:i]+telex_rule["uow"]+word[i+2:-1]
                            possible_words.append(temp)
                            
                    if (word[i]+word[i+1]+word[-1]) in telex_rule:
                        # print(word[i]+word[i+1]+word[-1])
                        # Chain of letter may be telex
                        chain = str(word[i]+word[i+1]+word[-1])
                        temp = word[:i]+telex_rule[chain]+word[i+2:-1]
                        possible_words.append(temp)
                    elif (word[i]+word[-1]) in telex_rule:
                        chain = str(word[i]+word[-1])
                        # print(word[i]+word[-1])
                        # print(telex_rule[chain])
                        temp = word[:i]+telex_rule[chain]+word[i+1:-1]
                        possible_words.append(temp)
                        # Accept words only end normal
                        # if temp[-1] not in ends:
                        # possible_words.append(temp)
                    else:
                        possible_words.append(word)
                else:
                    pass
            # print("so 2")
        else:
            for i in range(len(word[:-1])):
                if (word[i:i+3]) in telex_rule:
                    chain = str(word[i:i+3])
                    temp = word[:i]+telex_rule[chain]+word[i+3:]
                    possible_words.append(temp)
                if (word[i]+word[i+1]) in telex_rule:
                    chain = str(word[i]+word[i+1])
                    temp = word[:i]+telex_rule[chain]+word[i+2:]
                    possible_words.append(temp)
                    
            possible_words.append(word)
                    
    elif len(word) == 2:
        if str(word) in telex_rule:
            possible_words.append(telex_rule[word])
        else:
            possible_words.append(word)
            
    # Remove unknow words
    possible_words  = know2(possible_words)
    # Remove duplicate
    possible_words = list(dict.fromkeys(possible_words))
    # print(possible_words)
    if possible_words:
        return str(possible_words[0])
    # return possible_words

def correction2(words):
    """ Most probable spelling correction for word """
    return max(words, key=probability)
    
def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)
    
def know2(words):
    possible_words = []
    for w in words:
        if w.lower() in WORDS:
            possible_words.append(w)
    return possible_words

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyzáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    # print("split: \n", splits)
    # print("delete: \n", deletes)
    # print("transposes: \n", transposes)
    # print("replace: \n", replaces)
    # print("insert: \n", inserts)
    # return set(deletes + transposes + replaces + inserts)
    return (deletes + transposes + replaces + inserts)

    
def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# def edit3(word):
    # """All edit that are two edits away from 'word'."""
    # for e1 in edit1(word):
        # for e2 in edit1(e1):
            
# print(len(set(edits2('tón'))))
# print((edits1("yueej")))
# nhap = []
# pword = edits1("bawn")
# print(pword)
# for w in pword:
    # print(telex_processor(pword))
# if "bawn" in pword:
    # print(True)
# else:
    # print(False)
# print(telex_processor(w) for w in pword)

# telex_processor("bawn")
editted_word = []
for word in edits1("khoawn"):
    editted = telex_processor(word)
    if editted:
        editted_word.append(editted)
print(correction2(editted_word))
# telex_processor("nghiengse")
# telex_processor("phetes")
# print(load_rule("telex2.txt"))
# test_sentence = "heo beos if eof xin keos co theo tuis ddeo cheos".split()
# for word in test_sentence:
    # telex_processor(word)
