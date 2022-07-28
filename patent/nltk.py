from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

class AmiTokenizer:
    def __init__(self):
        self.text = None
        self.sentences = None
        self.words = None
        self.counter = Counter()

    def read_text(self, path):
        with open(path, "r") as f:
            self.text = f.read()
        self.tokenize_to_sentences_and_words()

    def tokenize_to_sentences_and_words(self):
        if self.text:
            self.sentences = sent_tokenize(self.text)
            self.words = word_tokenize(self.text)
            for word in self.words:
                self.counter[word] += 1

