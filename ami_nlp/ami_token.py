import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
nltk.download("stopwords")
from nltk.corpus import stopwords
import string

"""Tutorial https://realpython.com/nltk-nlp-python/ """
class AmiTokenizer:
    def __init__(self, use_stopwords=True, remove_punct=True, custom_filter=None):
        self.text = None
        self.sentences = []
        self.words = []
        self.counter = Counter()
        self.stop_words = set() if not use_stopwords else set(stopwords.words("english"))
        self.remove_punct = remove_punct
        self.custom_filters = []

    def add_custom_filter(self, custom_filter):
        if not custom_filter:
            print(f"filter is None")
            return
        self.custom_filters.append(custom_filter)


    def read_text(self, path, custom_filter=None):
        if path.exists():
            with open(path, "r") as f:
                self.text = f.read()
            self.tokenize_to_sentences_and_words()
            self.apply_filters()

    def apply_filters(self, max_hits_list=None):
        """iterates over several filters.
        """
        strings = self.words if self.words else self.sentences
        hits_list = []
        for filter in self.custom_filters:
            hits = filter.search_in_list(strings)
            if hits:
                hits_list.append(hits)
        return hits_list

    def get_filtered_text(self):
        return " ".join(self.words)


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

    def extract_bigrams(self):
        bigrams = list(nltk.bigrams(self.words))
        bigram_freq = Counter()
        for bigram in bigrams:
            bigram_freq[bigram] += 1
        return bigram_freq

    def append(self, ami_tokenizer):
        self.text = ami_tokenizer.text if self.text is None else self.text + ami_tokenizer.text
        self.sentences.extend(ami_tokenizer.sentences)
        self.words.extend(ami_tokenizer.words)
        self.counter += ami_tokenizer.counter
        self.stop_words |= ami_tokenizer.stop_words

