import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
nltk.download("stopwords")
from nltk.corpus import stopwords
import string

"""Tutorial https://realpython.com/nltk-nlp-python/ """
class AmiTokenizer:
    def __init__(self, use_stopwords=True, remove_punct=True):
        self.text = None
        self.sentences = []
        self.words = []
        self.counter = Counter()
        self.stop_words = set() if not use_stopwords else set(stopwords.words("english"))
        self.remove_punct = remove_punct


    def read_text(self, path):
        if path.exists():
            with open(path, "r") as f:
                self.text = f.read()
            self.tokenize_to_sentences_and_words()


    SYMBOLS = ['±', '“']
    def tokenize_to_sentences_and_words(self):
        if self.text:
            self.sentences = sent_tokenize(self.text)
            self.words = word_tokenize(self.text)
            self.words = [word for word in self.words if word.casefold() not in self.stop_words]
            if self.remove_punct:
                self.words = [word for word in self.words if not word in string.punctuation]
            self.words = [word for word in self.words if not word.isnumeric()]
            self.words = [word for word in self.words if word not in self.SYMBOLS]
            for word in self.words:
                self.counter[word] += 1

