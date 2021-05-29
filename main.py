import sqlite3

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
#"cant get you out of my head"

conn = sqlite3.connect('dataset_v3.db')
while True:
    # input
    print("Enter a query \n")
    print("------------------------- \n")
    string = str(input())

    query = preprocess.get_words(string)
    scores = bm25.get_scores(query)
    index = list(range(1, len(scores) + 1))
    result = sorted(zip(scores, index), reverse=True)[:3]

    for song in result:
        cur = conn.cursor()
        res = 0
        for row in cur.execute("SELECT * FROM track_info where track_id =" + str(song[1])):
            print(row[2])
            print(row[3])
            print("\n")
