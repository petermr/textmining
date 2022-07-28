from pathlib import Path

from test_lens import RESOURCE_DIR
from patent.nltk import AmiTokenizer

class TestNltk:

    def test_words_sentences_1(self):
        ami_tokenizer = AmiTokenizer()
        ami_tokenizer.read_text(Path(RESOURCE_DIR, "desc_1.txt"))
        print(f"sentences {len(ami_tokenizer.sentences)}")
        print(f"words {len(ami_tokenizer.words)}")
        print(f"counter {ami_tokenizer.counter}")
        ami_tokenizer.counter.most_common(10)
        # print(f"most common {ww}")

