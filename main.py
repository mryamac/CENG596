from rank_bm25 import BM25Okapi

from PreProcess import PreProcess
from Shhazam import Shhazam
from StopwordFilter import StopwordFilter
from datetime import datetime

from TFIDF import TFIDF

preprocess = PreProcess("lancaster")

start = datetime.now()

start_time = start.strftime("%H:%M:%S")

corpus = preprocess.generate_corpus()
bm25 = BM25Okapi(corpus)

query = preprocess.get_words("cant get you out of my head")
print(bm25.get_top_n(query, corpus, n=10))

