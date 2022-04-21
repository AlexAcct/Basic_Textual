def get_nword(doc):
    text = re.sub(r'\s+', ' ', str(doc))
    words = tokenizer.tokenize(text)
    num_words = len(words)
    return num_words

def get_ncword(doc):
    text = re.sub(r'\s+', ' ', str(doc))
    words = tokenizer.tokenize(text)
    vowels = "aeiouy"
    num_complex = 0
    for w in words:
        syl = 0
        count = 0
        while count < len(w):
            if w[count] in vowels:
                syl += 1
                count += 1
            count += 1
        if w[-1] == "e" and w[-2:] != "le":
            syl -= 1
        if syl >= 3:
            num_complex += 1
    return num_complex

def get_nsent(doc):
    text = re.sub(r'\s+', ' ', str(doc))
    sentences = nltk.sent_tokenize(text)
    sentences = [s for s in sentences if len(s.split(' '))>3]
    num_sentences = len(sentences)
    return num_sentences

import pandas as pd
import re
import requests
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
neg_words = pd.read_excel('LoughranMcDonald_SentimentWordLists_2018.xlsx', sheet_name='Negative', header=None)
neg_words = neg_words.rename(columns={0: "token"})
neg_words['token'] = neg_words['token'].str.lower()
pos_words = pd.read_excel('LoughranMcDonald_SentimentWordLists_2018.xlsx', sheet_name='Positive', header=None)
pos_words = pos_words.rename(columns={0: "token"})
pos_words['token'] = pos_words['token'].str.lower()


def get_counts(text):
    text = text.lower()
    tokens = word_tokenize(text)

    counts = Counter(tokens)
    df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
    df = df.rename(columns={"index": "token", 0: "count"})

    df = df.sort_values(by=["count"], ascending=[False])
    return df


def get_pos(text):
    df = get_counts(text)
    data = pd.merge(df, pos_words, on='token', how='left', indicator=True)
    data['pos'] = 0
    data.loc[data._merge == 'both', 'pos'] = 1
    data = data.drop(columns=['_merge'])
    num_pos = data[data.pos == 1]['count'].sum()
    return num_pos


def get_neg(text):
    df = get_counts(text)
    data = pd.merge(df, neg_words, on='token', how='left', indicator=True)
    data['neg'] = 0
    data.loc[data._merge == 'both', 'neg'] = 1
    data = data.drop(columns=['_merge'])
    num_neg = data[data.neg == 1]['count'].sum()
    return num_neg