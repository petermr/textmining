import unittest
from pathlib import Path
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics

from time import time

# local
from ami_nlp.lens import Lens
from ami_nlp.ami_token import AmiTokenizer

TEST_DIR = Path(__file__).parent
RESOURCE_DIR = Path(TEST_DIR, "resources")
TEMP_DIR = Path(Path(__file__).parent.parent, "temp")

class TestLens(unittest.TestCase):


    def test_read_lens(self):
        print(f"parent {TEST_DIR}")

        json_path = Path(RESOURCE_DIR, "p_1_100.json")

        lens = Lens()
        lens.read_write(json_path)


    def test_sklearn(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        corpus = [
            'This is the first document.',
            'This document is the second document.',
            'And this is the third one.',
            'Is this the first document?',
        ]
        # true_k = 13 # unknown at present
        true_k = 99 # unknown at present
        labels = [f"lab{i}" for i in range(0, true_k + 1)]
        # labels = ["lab0", "lab1", "lab2", "lab3", "lab4", "lab5", "lab6", "lab7", "lab8", "lab9", "lab10",
        #           "lab11", "lab12", "lab13", "lab14"]
        corpus = []
        for i in range(0, true_k + 1):
            inpath = Path(TEMP_DIR, f"desc_{i + 1}.txt")
            ami_tokenizer = AmiTokenizer()
            ami_tokenizer.read_text(inpath)
            filtered_text = ami_tokenizer.get_filtered_text()
            # print(f">>filtered: {filtered_text[:100]}")
            corpus.append(filtered_text)
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(corpus)
        vectorizer.get_feature_names_out()

        print(X.shape)

        km = KMeans(
            n_clusters=true_k,
            init="k-means++",
            max_iter=100,
            n_init=1,
            verbose=True,
        )

        print("Clustering sparse data with %s" % km)
        t0 = time()
        km.fit(X)
        print("done in %0.3fs" % (time() - t0))
        print()

        # %%
        # Performance metrics
        # -------------------

        print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
        print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
        print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
        print("Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(labels, km.labels_))
        print(
            "Silhouette Coefficient: %0.3f"
            % metrics.silhouette_score(X, km.labels_, sample_size=1000)
        )

        print()

        # %%

        # if not opts.use_hashing:
        if True:
            print("Top terms per cluster:")

            # if opts.n_components:
            if False:
                original_space_centroids = svd.inverse_transform(km.cluster_centers_)
                order_centroids = original_space_centroids.argsort()[:, ::-1]
            else:
                order_centroids = km.cluster_centers_.argsort()[:, ::-1]

            terms = vectorizer.get_feature_names_out()
            for i in range(true_k):
                print("Cluster %d:" % i, end="")
                for ind in order_centroids[i, :10]:
                    print(" %s" % terms[ind], end="")
                print()
