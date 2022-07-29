from pathlib import Path

from test_lens import RESOURCE_DIR, TEMP_DIR
from patent.nltk import AmiTokenizer
from collections import Counter

class TestNltk:

    def test_words_sentences_1(self):
        ami_tokenizer = AmiTokenizer()
        ami_tokenizer.read_text(Path(RESOURCE_DIR, "desc_1.txt"))
        with open(Path(RESOURCE_DIR, "desc_1.txt")) as f:
            text = f.read()
        print(f"text: {text[:500]}...")
        print(f"sentences {len(ami_tokenizer.sentences)}, words {len(ami_tokenizer.words)}")
        print(f"counter {ami_tokenizer.counter}")
        print(f"common {ami_tokenizer.counter.most_common(10)}")

    def test_words_sentences_100(self):
        total_counter = Counter()
        for i in range(1,100):
            ami_tokenizer = AmiTokenizer()

            ami_tokenizer.read_text(Path(TEMP_DIR, f"desc_{i}.txt"))
            if ami_tokenizer.sentences:
                print(f"sentences {len(ami_tokenizer.sentences)}, words {len(ami_tokenizer.words)}")
                print(f"commonest {ami_tokenizer.counter.most_common(50)}")
                total_counter += ami_tokenizer.counter
        print(f"total counter {total_counter}")


