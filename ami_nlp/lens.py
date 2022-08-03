import re
import json
from pathlib import Path
# local
from ami_nlp.ami_token import AmiTokenizer
from ami_nlp.custom_filter import Aa1Filter

TEST_DIR = Path(Path(__file__).parent.parent, "test")
RESOURCES = Path(TEST_DIR, "resources")
TEMP_DIR = Path(Path(__file__).parent.parent, "temp")

class Lens:


    def __init__(self):
        pass

    def read_write(self, json_path):
        """exploratory; reads patent descrions and searches for aminoacid mutations
        :param json_path: json for complete patent from TheLens
        """
        print(f"json {json_path}")
        with open(str(json_path)) as f:
            p1 = json.load(f)
        top_keys = p1.keys()
        print(f"top {top_keys}")
        data = p1["data"]
        print(f"ld {len(data)}")
        data0 = data[0]
        filters = [
            Aa1Filter()
        ]
        for i, datax in enumerate(data):
            self.read_process_patent(datax, i)
            self.apply_filters(filters)

    def read_process_patent(self, patent_json, serial):
        """read single ami_nlp from JSON aggregate from Lens
        :param patent_json: JSON from Lens.org
        :param serial: number within json
        """
        # print(f"\n\n d {patent_json.keys()}")
        biblio_ = patent_json['biblio']
        print(f""
              # f"bib {biblio_.keys()} \n "
              f"APPLICATION REF: {biblio_['application_reference'] }\n"
              f"TITLE: {biblio_['invention_title'][0]['text']}")
              # ")
        if "description" in patent_json:
            text_ = patent_json['description']['text']
            print(f"text {len(text_)}: {text_[:70]} ...")
            outpath = Path(TEMP_DIR, f"desc_{serial + 1}.txt")
            with open(outpath, "w") as f:
                f.write(text_)
            ami_tokenizer = AmiTokenizer()
            ami_tokenizer.text = text_
            ami_tokenizer.tokenize_to_sentences_and_words()

    def apply_filters(self, filters=None):
        if filters:
            for filter in filters:
                filter.apply_filters(self.words)
        pass


