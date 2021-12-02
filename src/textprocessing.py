
import nltk
import re
nltk.download('stopwords')
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

from nltk.stem.porter import *
stemmer = PorterStemmer()

# Improve tokenization
def tokenize(s):
    token_list = s.split()
    return(token_list)

# Stop word removal
def stop_words_removal(word_tokens):
    processed_text = [w for w in word_tokens if not w in STOPWORDS]
    return(processed_text)

# Case folding
def case_folding(word_tokens):
    processed_text = [w.casefold() for w in word_tokens]
    return(processed_text)

# Stemming / Lemmatization
def stemming(word_tokens):
    # stems = []
    # for w in word_tokens:
    #     stems.append(stemmer.stem(w))
    stems = [stemmer.stem(w) for w in word_tokens]
    return(list(set(stems)))


def textprocessor(s):
    # word_tokens = s.split()
    # processed_text = stop_words_removal(word_tokens)
    # proceseed_text = list(set([stemmer.stem(w) for w in processed_text]))
    # return(processed_text,word_tokens))
    s = re.sub(r'\W+', ' ', s)
    #print(s)
    word_tokens = s.lower().split()
    #processed_text = stop_words_removal(word_tokens)
    processed_text = [w for w in word_tokens if not w in STOPWORDS]
    #proceseed_text  = stemming(processed_text)
    #proceseed_text = list(set([stemmer.stem(w) for w in processed_text]))
    proceseed_text = [stemmer.stem(w) for w in processed_text]
    return(processed_text,word_tokens)



    