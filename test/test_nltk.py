import unittest
from pathlib import Path
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
# local
from test_lens import RESOURCE_DIR, TEMP_DIR
from ami_nlp.ami_token import AmiTokenizer


class TestAmiTokenizer:

    def test_words_sentences_1(self):
        """read a single (patent) text and extract sentences and (commonest) words"""
        ami_tokenizer = AmiTokenizer()
        ami_tokenizer.read_text(Path(RESOURCE_DIR, "desc_1.txt"))
        with open(Path(RESOURCE_DIR, "desc_1.txt")) as f:
            text = f.read()
        assert text[:500] == "CROSS-REFERENCES TO RELATED APPLICATIONS This application claims the priority of" \
                             " Chinese patent application filed with the Chinese Patent Office on Jul. 16, 2019," \
                             " with the application number 2019106445393, entitled" \
                             " “Virus and Tumor Therapeutic Drug for Specifically Killing Tumor cells”," \
                             " the entire content of which is incorporated by reference in this application." \
                             " TECHNICAL FIELD The present disclosure relates to the field of biotechnology," \
                             " in particular, to virus and tumor therapeutic drug for s"
        print(f"sentences {len(ami_tokenizer.sentences)}, words {len(ami_tokenizer.words)}")
        print(f"counter {ami_tokenizer.counter}")
        print(f"common {ami_tokenizer.counter.most_common(50)}")

    @unittest.skip("too long")
    def test_words_sentences_100(self):
        """read 100 patents , find sentences, commonest words, bigrams
        (30 sec)
        """
        total_tokenizer = AmiTokenizer()
        for i in range(1, 100):
            ami_tokenizer = AmiTokenizer()
            ami_tokenizer.read_text(Path(TEMP_DIR, f"desc_{i}.txt"))
            ami_tokenizer.apply_filters()
            if ami_tokenizer.sentences:
                total_tokenizer.append(ami_tokenizer)
        assert len(total_tokenizer.sentences) == 104637
        assert len(total_tokenizer.words) == 1740996
        assert total_tokenizer.extract_bigrams().most_common(50)[:3] == [
            (('SEQ', 'ID'), 8203),
            (('nucleic', 'acid'), 7610),
            (('amino', 'acid'), 3298)
        ]

    def test_words_sentences_3_patents(self):
        """read 100 patents , find sentences, commonest words, bigrams
        (30 sec)
        """
        total_counter = Counter()
        total_tokenizer = AmiTokenizer()
        hits = 3
        for i in range(1, 10):
            ami_tokenizer = AmiTokenizer()
            ami_tokenizer.read_text(Path(TEMP_DIR, f"desc_{i}.txt"))
            if ami_tokenizer.sentences:
                total_tokenizer.append(ami_tokenizer)
                hits -= 1
                if hits == 0:
                    break
        assert len(total_tokenizer.sentences) == 3675
        assert len(total_tokenizer.words) == 53607
        assert total_tokenizer.extract_bigrams().most_common(50)[:3] == [
 (('biological', 'component'), 493),
 (('polymer', 'matrix'), 450),
 (('fluidic', 'device'), 359)
        ]

    def test_bigrams(self):
        """read single patent text and extract bigrams"""
        ami_tokenizer = AmiTokenizer()
        ami_tokenizer.read_text(Path(RESOURCE_DIR, "desc_1.txt"))
        common50bigrams = ami_tokenizer.extract_bigrams().most_common(50)
        assert common50bigrams[0:3] == [(('oncolytic', 'virus'), 51), (('tumor', 'cells'), 45), (('essential', 'gene'), 42)]

    def test_scikit_tfidf(self):
        corpus = []
        # dirx = RESOURCE_DIR
        dirx = TEMP_DIR
        for i in range(1, 101):

            path = Path(dirx, f"desc_{i}.txt")
            if path.exists():
                with open(path, "r") as f:
                    corpus.append(f.read())
        # corpus = [
        #     'This is the first document.',
        #     'This document is the second document.',
        #     'And this is the third one.',
        #     'Is this the first document?',
        # ]
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(corpus)
        # print(f"X {X}")
        features = vectorizer.get_feature_names_out()

        print(X.shape)
        print(f"features {features}")


# probably ignore
#     def test_tfidf(self):
#         import math
#
#         from nltk import sent_tokenize, word_tokenize, PorterStemmer
#         from nltk.corpus import stopwords
#
#         '''
#         We already have a sentence tokenizer, so we just need
#         to run the sent_tokenize() method to create the array of sentences.
#         '''
#         # 1 Sentence Tokenize
#         sentences = sent_tokenize(text)
#         total_documents = len(sentences)
#         # print(sentences)
#
#         # 2 Create the Frequency matrix of the words in each sentence.
#         freq_matrix = _create_frequency_matrix(sentences)
#         # print(freq_matrix)
#
#         '''
#         Term frequency (TF) is how often a word appears in a document, divided by how many words are there in a document.
#         '''
#         # 3 Calculate TermFrequency and generate a matrix
#         tf_matrix = _create_tf_matrix(freq_matrix)
#         # print(tf_matrix)
#
#         # 4 creating table for documents per words
#         count_doc_per_words = _create_documents_per_words(freq_matrix)
#         # print(count_doc_per_words)
#
#         '''
#         Inverse document frequency (IDF) is how unique or rare a word is.
#         '''
#         # 5 Calculate IDF and generate a matrix
#         idf_matrix = _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
#         # print(idf_matrix)
#
#         # 6 Calculate TF-IDF and generate a matrix
#         tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)
#         # print(tf_idf_matrix)
#
#         # 7 Important Algorithm: score the sentences
#         sentence_scores = _score_sentences(tf_idf_matrix)
#         # print(sentence_scores)
#
#         # 8 Find the threshold
#         threshold = _find_average_score(sentence_scores)
#         # print(threshold)
#
#         # 9 Important Algorithm: Generate the summary
#         summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)
#         print(summary)
#
#     def _generate_summary(sentences, sentenceValue, threshold):
#         sentence_count = 0
#         summary = ''
#
#         for sentence in sentences:
#             if sentence[:15] in sentenceValue and sentenceValue[sentence[:15]] >= (threshold):
#                 summary += " " + sentence
#                 sentence_count += 1
#
#         return summary
#     def _find_average_score(sentenceValue) -> int:
#         """
#         Find the average score from the sentence value dictionary
#         :rtype: int
#         """
#         sumValues = 0
#         for entry in sentenceValue:
#             sumValues += sentenceValue[entry]
#
#         # Average value of a sentence from original summary_text
#         average = (sumValues / len(sentenceValue))
#
#         return average
#
#     def _score_sentences(tf_idf_matrix) -> dict:
#         """
#         score a sentence by its word's TF
#         Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
#         :rtype: dict
#         """
#
#         sentenceValue = {}
#
#         for sent, f_table in tf_idf_matrix.items():
#             total_score_per_sentence = 0
#
#             count_words_in_sentence = len(f_table)
#             for word, score in f_table.items():
#                 total_score_per_sentence += score
#
#             sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence
#
#         return sentenceValue
#
#     def _create_tf_idf_matrix(tf_matrix, idf_matrix):
#         tf_idf_matrix = {}
#
#         for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
#
#             tf_idf_table = {}
#
#             for (word1, value1), (word2, value2) in zip(f_table1.items(),
#                                                         f_table2.items()):  # here, keys are the same in both the table
#                 tf_idf_table[word1] = float(value1 * value2)
#
#             tf_idf_matrix[sent1] = tf_idf_table
#
#         return tf_idf_matrix
#
#     def _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
#         idf_matrix = {}
#
#         for sent, f_table in freq_matrix.items():
#             idf_table = {}
#
#             for word in f_table.keys():
#                 idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))
#
#             idf_matrix[sent] = idf_table
#
#         return idf_matrix
#
#     def _create_documents_per_words(freq_matrix):
#         word_per_doc_table = {}
#
#         for sent, f_table in freq_matrix.items():
#             for word, count in f_table.items():
#                 if word in word_per_doc_table:
#                     word_per_doc_table[word] += 1
#                 else:
#                     word_per_doc_table[word] = 1
#
#         return word_per_doc_table
#
#     def _create_tf_matrix(freq_matrix):
#         tf_matrix = {}
#
#         for sent, f_table in freq_matrix.items():
#             tf_table = {}
#
#             count_words_in_sentence = len(f_table)
#             for word, count in f_table.items():
#                 tf_table[word] = count / count_words_in_sentence
#
#             tf_matrix[sent] = tf_table
#
#         return tf_matrix
#
#     def _create_frequency_matrix(sentences):
#         frequency_matrix = {}
#         stopWords = set(stopwords.words("english"))
#         ps = PorterStemmer()
#
#         for sent in sentences:
#             freq_table = {}
#             words = word_tokenize(sent)
#             for word in words:
#                 word = word.lower()
#                 word = ps.stem(word)
#                 if word in stopWords:
#                     continue
#
#                 if word in freq_table:
#                     freq_table[word] += 1
#                 else:
#                     freq_table[word] = 1
#
#             frequency_matrix[sent[:15]] = freq_table
#
#         return frequency_matrix