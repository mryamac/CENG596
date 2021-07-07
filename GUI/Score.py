import heapq
import math
import sqlite3
from _heapq import heappush, heappushpop

from TFIDF import TFIDF


class Score:
    def __init__(self, k):
        self.k = k
        self.song_list = []
        self.conn = sqlite3.connect('dataset_v3.db')

        self.query_tf = "l"
        self.query_df = "t"
        self.query_norm = "c"
        self.doc_tf = "l"
        self.doc_df = "n"
        self.doc_norm = "c"

    def __del__(self):
        self.conn.close()

    def __get_number_of_terms__(self):
        cur = self.conn.cursor()
        res = 0
        for row in cur.execute("SELECT count(*) FROM track_info;"):
            res = row[0]
        return res

    def __get_term_frequency__(self, word):
        cur = self.conn.cursor()
        res = 0
        for row in cur.execute("SELECT term_frequency FROM posting_list where term ='" + word + "'"):
            res = row[0]
        return res

    def __get_doc_frequency__(self, word):
        cur = self.conn.cursor()
        res = 0
        for row in cur.execute("SELECT doc_frequency FROM posting_list where term ='" + word + "'"):
            res = row[0]
        return res

    def __get_per_doc_frequency__(self, doc, word):
        cur = self.conn.cursor()
        res = 0
        for row in cur.execute("SELECT count from track_words where word ='" + word + "' and track_id =" + str(doc)):
            res = row[0]
        return res

    def __get_per_doc_frequency__(self, word):
        cur = self.conn.cursor()
        res = 0
        new_list = {}
        for row in cur.execute("SELECT track_id, count from track_words where word ='" + word + "'"):
            new_list.update({row[0]: row[1]})
        return new_list

    def __get_doclist_with_frequency__(self, word_list):
        cur = self.conn.cursor()
        new_list = []
        query = "SELECT distinct(track_id) from track_words where 1=0 "
        for word in word_list:
            query = query + "or word ='" + word + "'"

        for row in cur.execute(query):
            new_list.append(row[0])
        return new_list

    def set_query_tfidf(self, text):
        self.query_tf = text[0]
        self.query_df = text[1]
        self.query_norm = text[2]

    def set_doc_tfidf(self, text):
        self.doc_tf = text[0]
        self.doc_df = text[1]
        self.doc_norm = text[2]

    def merge_list(self, plist):
        j = 0
        i = 0
        while True:
            if len(self.song_list) <= i:
                heappush(self.song_list, plist[j])
                j += 1
            elif len(plist) <= j:
                break
            elif plist[j][0] == self.song_list[i][0]:
                self.song_list[i] = (self.song_list[i][0], self.song_list[i][1] + plist[j][1])
                i += 1
                j += 1
            elif plist[j][0] > self.song_list[i][0]:
                i += 1
            else:
                heappush(self.song_list, plist[j])
                j += 1

    def feed_and_query(self, word_list):
        N = self.__get_number_of_terms__()

        docTFIDF = TFIDF(tf=self.doc_tf, df=self.doc_df, norm=self.doc_norm, n=N)
        queryTFIDF = TFIDF(tf=self.query_tf, df=self.query_df, norm=self.query_norm, n=N)

        query_scores = []
        query_norm = 0
        for word in word_list:
            score = queryTFIDF.get_term_frequency(word_list[word]) \
                    * queryTFIDF.get_document_frequency(self.__get_doc_frequency__(word))
            query_scores.append(score)
            query_norm += (score * score)

        query_scores_n = []
        for score in query_scores:
            query_scores_n.append(score * queryTFIDF.get_normalization(math.sqrt(query_norm)))

        doclist = self.__get_doclist_with_frequency__(word_list)

        processed = 0
        docSize = len(doclist)

        doc_freq = []
        for word in word_list:
            doc_freq.append(self.__get_doc_frequency__(word))

        tf_list = []
        for word in word_list:
            tf_list.append(self.__get_per_doc_frequency__(word))

        for doc in doclist:
            doc_scores = []
            doc_norm = 0
            for i, word in enumerate(word_list):
                if doc in tf_list[i]:
                    dscore = docTFIDF.get_term_frequency(tf_list[i][doc]) \
                             * docTFIDF.get_document_frequency(doc_freq[i])
                else:
                    dscore = 0
                doc_scores.append(dscore)
                doc_norm += (dscore * dscore)

            doc_score = 0
            for i, score in enumerate(doc_scores):
                doc_score += (score * docTFIDF.get_normalization(math.sqrt(doc_norm)) * query_scores_n[i])


            self.song_list.append((doc, doc_score))
            processed += 1
            progress = 100 * processed / docSize
            print("Calculating document scores : %.2f" % progress, "%")

    def get_list(self):
        return self.song_list
