import pandas as pd
import re
import os
import csv
import nltk

nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')


def get_fog(doc):
    text = re.sub(r'\s+', ' ', str(doc))
    words = tokenizer.tokenize(text)
    num_words = len(words)
    sentences = nltk.sent_tokenize(text)

    num_sentences = len(sentences)
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
    if num_words > 0:
        if num_sentences > 0:
            words_per_sentence = num_words / num_sentences
            percent_complex = (num_complex / num_words) * 100
            fog = 0.4 * (words_per_sentence + percent_complex)
        if num_sentences == 0:
            fog = "NaN"
    if num_words == 0:
        fog = "NaN"
    return fog