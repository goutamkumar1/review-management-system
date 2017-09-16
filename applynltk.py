from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

example_sent = "This is a sample sentence, showing off the stop words filtration. tum kya kar rhe ho"

stop_words = set(stopwords.words('english','hindi'))
sw2=set(stopwords.words('hindi'))

word_tokens = word_tokenize(example_sent)

filtered_sentence = [w for w in word_tokens if not w in stop_words]
fs = [w for w in word_tokens if not w in stop_words]

filtered_sentence = []
fs=[]

for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)
    if w not in sw2:
    	fs.append(w)

print word_tokens
print filtered_sentence
print  fs