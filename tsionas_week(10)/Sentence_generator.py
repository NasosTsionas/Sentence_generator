# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import itertools
import nltk.corpus
import nltk
from nltk import trigrams
from nltk.text import Text
import random
import os

def ngrams_wrapper(sent):
    return list(nltk.ngrams(sent, 2, pad_right=True, pad_left=True, left_pad_symbol="$$", right_pad_symbol="$$"))

def ngrams_wrapper_3(sent):
    return list(nltk.ngrams(sent, 3,pad_right=True, pad_left= True, left_pad_symbol="$$", right_pad_symbol="$$"))




# first three letters are: ï»¿
# f = open("books/planet_named_joe.txt", "r")
# book = f.readline()
# book = book[3:-1]
book = ""


list_of_books = os.listdir("books/")

avoid_Gutenberg_Notes = True
license_start = "*** END OF "

cut_start_or = True
authors_credits_end = "*** START OF"


print(len(book))


"""
cut_start_or => if true then it will read the book after he finds the words '*** START OF'
each book in Gutenberg has first authors info etc.


avoid_Gutenberg_Notes => in end of the book there is the info about license etc.


"""
for i in list_of_books:
    read_path = "books/" + i
    print("Opening:  ", read_path)
    f = open(read_path, "r")
    cut_start = cut_start_or


    for j in f:
        if license_start in j and avoid_Gutenberg_Notes:
            break
        if cut_start:
            if authors_credits_end in j:
                cut_start = False
                print("    >>> parsing ", end="")
                continue
            else:
                continue

        j = j.replace("--", "")
        j = j.replace("_", "")
        book = book + j
    print(len(book))
    print()


print(len(book))
print()

#region unigramms

words = nltk.word_tokenize(book)
unigram = nltk.ngrams(words, 1)

freq_dist_un = nltk.FreqDist(unigram)
prob_dist_un = nltk.MLEProbDist(freq_dist_un)
# number_of_unigrams = prob_dist_un.N()

if False:
    for i in freq_dist_un:
        print(i," ", freq_dist_un[i], " ", prob_dist_un.prob(i))


#endregion


#region bigramms

sentences = nltk.sent_tokenize(book)
tokenized = map(nltk.tokenize.word_tokenize, sentences)

bigrams = map(ngrams_wrapper, tokenized)
bigram = list(itertools.chain.from_iterable(bigrams))



freq_dist_bi = nltk.FreqDist(bigram)

prob_dist_bi = nltk.MLEProbDist(freq_dist_bi)
number_of_bigrams = freq_dist_bi.N()


if False:
    for i in freq_dist:
        print(i," ", freq_dist_bi[i], " ", prob_dist_bi.prob(i))


#endregion


#region trigramms

sentences = nltk.sent_tokenize(book)
tokenized = map(nltk.tokenize.word_tokenize, sentences)

trigams = map(ngrams_wrapper_3, tokenized)
trigram = list(itertools.chain.from_iterable(trigams))




freq_dist_tri = nltk.FreqDist(trigram)
prob_dist_tri = nltk.MLEProbDist(freq_dist_tri)
number_of_trigramms = freq_dist_tri.N()

if False:
    for i in freq_dist_tri:
        print(i," ", freq_dist_tri[i], " ", prob_dist_tri.prob(i))



#endregion



# to check and find words propablities

# t = ["$$", "Our"]
#
# for i in trigram:
#     if i[0] == t[-2] and i[1] == t[-1]:
#         print(i," ", freq_dist_tri[i], " ", prob_dist_tri.prob(i))
#





"""
checks so first letter of bigramm is upper case and if exist the second is lower case. 
    -> Avoiding sentences with all capitals
    
also remove sentences with "." in them 

choose one at random and it is the initialization of the sentence
"""
def initial_sentence_2(bi):
    my_sentence = ""

    initial_bi = []
    for i in bi:
        if i[0] == "$$":
            initial_bi.append(i)


    x = random.randrange(len(initial_bi))
    my_sentence += initial_bi[x][0]
    my_sentence += " "
    my_sentence += initial_bi[x][1]
    return my_sentence



"""
generated_method [0,1]

0: sentences will be first generated through trigrams and if there is no matching trigram will bigram used

1: sentences will be generated through both trigram and bigram with the 'list_of_candidates' =>
in list there are all candidates of how the sentence can proceed. In the list are inserted  nltk.FreqDist[ngram] times each 
possible candidate. 

'bi_tri_balance' is how many times to input each trigram in the list. If 'bi_tri_balance = 1' then each trigram is inserted 1 time and has the same
weight as a bigram 'bi_tri_balance = 2' each trigram has double the weight and so on

"""
def find_possible_subSentences(sen, bi, tri,generate_method = 0, bi_tri_balance = 2):
    bi_sub_gen = []
    tri_sub_gen = []
    splited_sen = sen.split(" ")

    list_of_candidates = []

    for i in bi:
        if i[0] == splited_sen[-1]:
            bi_sub_gen.append(i)
            list_of_candidates.append(i[-1])


    for i in tri:
        if i[0] == splited_sen[-2] and i[1] == splited_sen[-1]:
            tri_sub_gen.append(i)
            for j in range(bi_tri_balance):
                list_of_candidates.append(i[-1])

    if False:
        for i in sorted(bi_sub_gen):
            print(i)
        print("==================\n\n")
        for i in tri_sub_gen:
            print(i)



    if generate_method == 0:
        if len(tri_sub_gen) <= 0:
            if len(list_of_candidates) > 0:
                x = random.randrange(len(list_of_candidates))
                to_add = list_of_candidates[x]
            else:
                to_add = "..."
        else:
            x = random.randrange(len(tri_sub_gen))
            to_add = tri_sub_gen[x][2]
    elif generate_method == 1:
        if len(list_of_candidates) > 0:
            x = random.randrange(len(list_of_candidates))
            to_add = list_of_candidates[x]
        else:
            to_add = "..."


    to_add = " " + str(to_add)
    return to_add


def generate_a_sentence_2(bi, tri, max_sentence_length = 120, ge_meth = 0, bi_tri_bal = 2):
    gen_sen = initial_sentence_2(bi)
    # print(gen_sen)
    # print("\n")

    while gen_sen.split()[-1] != "$$" and len(gen_sen) < max_sentence_length:
        gen_sen = gen_sen + find_possible_subSentences(gen_sen, bi, tri, ge_meth, bi_tri_bal)

        if len(gen_sen) >= max_sentence_length and gen_sen[-1] != "$$":
            gen_sen = gen_sen + "[.....]"
    # print(gen_sen)
    return gen_sen




for i in range(10):
    print(i, end=": ")
    my_sen = generate_a_sentence_2(bigram, trigram, 140, 1, 1)
    my_sen = my_sen.replace("$$", "")
    print(my_sen)
    print()

