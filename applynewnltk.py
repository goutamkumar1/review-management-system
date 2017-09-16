import json
from pprint import pprint
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
import curses
from curses.ascii import isdigit
import nltk
from nltk.corpus import cmudict


with open('data.json') as data_file:
    data = json.load(data_file) 


def syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count=count+1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count


def get_reviewLength_setLength_stopwordsCount(data,product_count):
    reviews_len1 = []   # to get review length
    reviews_len2 = []   # to get set length
    reviews_len3 = []   # to get stop words count
    reviews_lex_div = []
    reviews_wrong_words = []
    stop_words = set(stopwords.words("english"))
    dct=cmudict.dict()
    for i in range(0,product_count):
        #ind_review_data = data[i]["reviews"]
        #j_length = data[i]["reviews"]
        local_list1 = []    # to get review length
        local_list2 = []    # to get set length
        local_list3 = []    # to get stop words count
        local_list4 = []
        local_list5 = []
        for j in range(0,len(data[i]["reviews"])):
            review_t =  word_tokenize(data[i]["reviews"][j]["review_text"])
            local_list1.append(len(review_t))
            a = set()
            cnt =0
            count=0
            for k in review_t:
                a.add(k)
                if k in stop_words:
                    cnt=cnt+1
                if k.lower() not in dct:
                    count=count+1 
            local_list2.append(len(a))
            local_list3.append(cnt)
            lexr=round((float(len(a))/len(review_t)),4)
            local_list4.append(lexr)
            local_list5.append(count)

        reviews_len1.append(local_list1)
        reviews_len2.append(local_list2)
        reviews_len3.append(local_list3)
        reviews_lex_div.append(local_list4)
        reviews_wrong_words.append(local_list5)
    return reviews_len1,reviews_len2,reviews_len3,reviews_lex_div,reviews_wrong_words

def get_dale_list(data,product_count):
    glist1 = []
    glist2 = []
    glist3 = []  #for syllables
    diff_words=set(stopwords.words("dalediffwords"))
    for i in range(0,product_count):
        llist1 = []
        llist2 = []
        llist3 = []
        for j in range(0,len(data[i]["reviews"])):
            rtext=word_tokenize(data[i]["reviews"][j]["review_text"])
            rsentence=sent_tokenize(data[i]["reviews"][j]["review_text"])
            cn=0
            scnt=0
            for k in rtext:
                if k not in diff_words:
                    cn=cn+1
                scnt=scnt+syllables("k")
            llist1.append(cn)
            llist2.append(len(rsentence))
            llist3.append(scnt)
        glist1.append(llist1)
        glist2.append(llist2)
        glist3.append(llist3)
    return glist1,glist2,glist3

def get_dale_and_flesch_result(dw,w,s,sy):#sy for syllable
    glist = []
    glist2=[]
    glen = len(dw)
    for i in range(0,glen):
        llist = []
        llist2=[]
        raw_score = 0
        llen = len(dw[i])
        for j in range(0,llen):
            #for calc dale formula
            raw_score=(0.1579*((dw[i][j]/w[i][j])*100))+(0.0496*(w[i][j]/s[i][j]))
            if raw_score>5:
                raw_score=raw_score+3.6365
            #for calc flesch formula
            asl=w[i][j]/s[i][j]
            asw=sy[i][j]/w[i][j]
            fre=206.84-(1.02*asl)-(84.6*asw)
            llist2.append(round(fre,4))
            llist.append(raw_score)

        glist.append(llist)
        glist2.append(llist2)
    return glist,glist2

"""
def get_uniq_length(data,product_count):
    reviews_len2 = []
    for i in range(0,product_count):
        local_list = []
        for j in range(0,len(data[i]["reviews"])):
            review_t = word_tokenize(data[i]["reviews"][j]["review_text"])
            a = set()
            for k in review_t:
                a.add(k)

            local_list.append(len(a))
        reviews_len2.append(local_list)
    return reviews_len2
def get_stopwords_count(data,product_count):
    reviews_len2 = []
    stop_words = set(stopwords.words("english"))
    for i in range(0,product_count):
        local_list = []
        for j in range(0,len(data[i]["reviews"])):
            review_t = word_tokenize(data[i]["reviews"][j]["review_text"])
            cnt = 0
            for k in review_t:
                if k in stop_words:
                    cnt=cnt+1;
            local_list.append(cnt)
        reviews_len2.append(local_list)
    return reviews_len2

#pprint(data)   To print the whole data within a single quote
"""
"""

#print(len(data[0]["reviews"]))
#################### GET REVIEWS LENGTH AND STORE INTO A LIST ########################
reviews_len = []
reviews_len = get_review_length(data,product_count)
print(reviews_len)

#################### GET REVIEWS LENGTH AND STORE INTO A LIST ########################




#################### GET REVIEWS UNIQUE LENGTH AND STORE INTO A LIST ########################
reviews_unique_words_len = []
reviews_unique_words_len = get_uniq_length(data,product_count)
print(reviews_unique_words_len)

#################### GET REVIEWS UNIQUE LENGTH AND STORE INTO A LIST ########################




stop_words_count = []
stop_words_count = get_stopwords_count(data, product_count)
print(stop_words_count)

"""
product_count = 2
reviews_len,reviews_setLength,reviews_stopwordsCount,lex_diversity,wrong_words = get_reviewLength_setLength_stopwordsCount(data,product_count)
dale_diffwords,dale_sentence,syll=get_dale_list(data,product_count)
dale_result,flesch_result=get_dale_and_flesch_result(dale_diffwords,reviews_len,dale_sentence,syll)
print("Reviews length is :",reviews_len)
print("Reviews set_length is :",reviews_setLength)
print("Reviews stopwords Count is :",reviews_stopwordsCount)
print("Difficult words count is :",dale_diffwords)
print("Sentence count is :",dale_sentence)
print("Dale-Chall formula result :",dale_result)
print("Lex Diversity :",lex_diversity)
print("Wrong words :",wrong_words)
print("Flesch Result :",flesch_result)