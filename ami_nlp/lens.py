import re
import json
from pathlib import Path
# local
from ami_nlp.ami_token import AmiTokenizer

TEST_DIR = Path(Path(__file__).parent.parent, "test")
RESOURCES = Path(TEST_DIR, "resources")
TEMP_DIR = Path(Path(__file__).parent.parent, "temp")

class Lens:


    def __init__(self):
        pass

    def read_write(self, json_path):
        print(f"json {json_path}")
        with open(str(json_path)) as f:
            p1 = json.load(f)
        top_keys = p1.keys()
        print(f"top {top_keys}")
        data = p1["data"]
        print(f"ld {len(data)}")
        data0 = data[0]
        for i, datax in enumerate(data):
            self.read_process_patent(datax, i)

    def read_process_patent(self, patent_json, serial):
        """read single ami_nlp from JSON aggregate from Lens
        :param patent_json: JSON from Lens.org
        :param serial: number within json
        """
        print(f"\n\n d {patent_json.keys()}")
        biblio_ = patent_json['biblio']
        print(f"bib {biblio_.keys()} \n "
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
            for sent in ami_tokenizer.sentences:
                # print(f"sent: {sent}")
                aa1 = re.match("(.*)\s([ACDEFGHIKLMNPQRSTVWY]\d{1,4}[ACDEFGHIKLMNPQRSTVWY])\s(.*)", sent)
                if aa1:
                    print(f"+++++aa1: {aa1.group(1)} :: {aa1.group(2)} :: {aa1.group(3)}")
                aa3 = re.findall("\s(Ala|Cys|Asp|Glu|Phe|Gly|His|Ile|Lys|Leu|Met|Asn|Pro|Gln|Arg|Ser|Thr|Val|Trp|Tyr)\s",
                                 sent)
                if aa3:
                    print(f"***** aa3: {aa3}")

