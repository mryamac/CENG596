import nltk
import csv
import sqlite3
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from rank_bm25 import BM25Okapi
from StopwordFilter import StopwordFilter


class PreProcess:
    def __init__(self, stemmer):
        if stemmer == "lancaster":
            self.stemmer = LancasterStemmer()
        else:
            self.stemmer = PorterStemmer()
        self.filter = StopwordFilter()
        self.filter.set_stop_words(
            {"a", "an", "and", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is", "it", "its", "of", "on",
             "that", "the", "to", "was", "were", "will", "with"})
        self.corpus = []
        self.track_words_map = []
        self.tf_map = {}
        self.df_map = {}

    def generate_corpus(self, con, refillDatabase):
        cur = con.cursor()
        if refillDatabase:
            with open("lyrics-data.csv", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if row[4] == 'ENGLISH':
                        try:
                            values_to_insert = (line_count + 1, row[0], row[1], row[3])
                            cur.execute("""
                                INSERT INTO track_info ('track_id', 'artist', 'track_name', 'lyrics')
                                VALUES (?, ?, ?, ?)""", values_to_insert)
                            line_count += 1
                            self.__add_bow__(row[3], line_count)
                            print(f'Processed {line_count} lines. \tTrack artist: {row[0]} name: {row[1]} {row[2]}')
                        except:
                            print(f'\nSKIP DUBLICATE. \tTrack artist: {row[0]} name: {row[1]} {row[2]}\n')

            print("FILL track_words...")
            cur.executemany("""
                INSERT INTO track_words ('track_id', 'word', 'count')
                VALUES (?, ?, ?);""", self.track_words_map)

            print("FILL posting_list...")
            dictionary_size = len(self.df_map)
            processed = 0
            for term in self.df_map:
                cur.execute("""
                            INSERT INTO posting_list('term', 'doc_frequency', 'term_frequency')
                            VALUES (?, ?, ?);""", (term, self.df_map[term], self.tf_map[term]))
                processed += 1
                progress = 100 * processed / dictionary_size
                print("POSTING LIST COMPLETION: %.2f" % progress, "%")

            con.commit()
            #self.con.close()
        else:
            rows = cur.execute("SELECT track_id, word, count FROM track_words ORDER BY track_id ASC;")
            track_id = 0
            for row in rows:
                if row[0] != track_id:
                    print("TRACK " + str(row[0]) + " ADDED TO CORPUS")
                    track_id = row[0]

                if len(self.corpus) < row[0]:
                    self.corpus.append([])
                
                for i in range (0, row[2]):
                    self.corpus[row[0] - 1].append(row[1])


        return self.corpus

    def __apply_stemming__(self, word_list, filter):
        new_list = {}
        for word in word_list.split():
            stemmed = self.__special_remove__(self.stemmer.stem(word))
            if filter.filter(stemmed) == False:
                value = 0
                if stemmed in new_list:
                    value = new_list.get(stemmed)
                new_list.update({stemmed: (value + 1)})
                #new_list.append(stemmed)


        #bi-gram words
        prev_word = "";
        for word in word_list.split():
            if (prev_word == ""):
                prev_word = word
            else:
                bi_gram = prev_word + "$%$" + word
                value = 0
                if bi_gram in new_list:
                    value = new_list.get(bi_gram)
                new_list.update({bi_gram: (value + 1)})
                prev_word = word

        return new_list

    def get_words(self, text):
        return self.__apply_stemming__(text, self.filter)

    def __special_remove__(self, word):
        # special cases (English...)
        word = word.replace("'m ", " am ")
        word = word.replace("'re ", " are ")
        word = word.replace("'ve ", " have ")
        word = word.replace("'d ", " would ")
        word = word.replace("'ll ", " will ")
        word = word.replace(" he's ", " he is ")
        word = word.replace(" she's ", " she is ")
        word = word.replace(" it's ", " it is ")
        word = word.replace(" ain't ", " is not ")
        word = word.replace("n't ", " not ")
        word = word.replace("'s ", " ")

        # remove boring punctuation and weird signs
        punctuation = (',', "'", '"', ",", ';', ':', '.', '?', '!', '(', ')',
                       '{', '}', '/', '\\', '_', '|', '-', '@', '#', '*')
        for p in punctuation:
            word = word.replace(p, '')

        return word

    def __add_bow__(self, word_list, row_id):
        word_map = self.__apply_stemming__(word_list, self.filter)
        word_list = []
        for w in word_map:
            self.track_words_map.append(((row_id, w, word_map.get(w))))

            tf = word_map.get(w)
            if w in self.tf_map:
                tf += self.tf_map[w]
            self.tf_map[w] = tf

            if w in self.df_map:
                self.df_map[w] = self.df_map[w] + 1
            else:
                self.df_map[w] = 1
            
            for i in range (0, word_map.get(w)):
                word_list.append(w)

        self.corpus.append(word_list)
        return
