import nltk
import csv
import sqlite3
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer

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
        self.con = sqlite3.connect("dataset_v3.db")
        self.track_words_map = []
        self.tf_map = {}
        self.df_map = {}

    def generate_corpus(self):
        cur = self.con.cursor()
        with open("lyrics-data.csv", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[4] == 'ENGLISH':
                    values_to_insert = (line_count + 1, row[0], row[1], row[3])

                    try:
                        cur.execute("""
                            INSERT INTO track_info ('track_id', 'artist', 'track_name', 'lyrics')
                            VALUES (?, ?, ?, ?)""", values_to_insert)

                        line_count += 1
                        # self.con.commit()
                        self.__add_bow__(cur, row[3], line_count)
                        print(f'Processed {line_count} lines. \tTrack artist: {row[0]} name: {row[1]} {row[2]}')
                    except:
                        print(f'*****SKIP DUBLICATE. \tTrack artist: {row[0]} name: {row[1]} {row[2]}')

        print("FILL track_words...")
        cur.executemany("""
            INSERT INTO track_words ('track_id', 'word', 'count')
            VALUES (?, ?, ?);""", self.track_words_map)

        # self.con.commit()
        print("FILL posting_list...")
        dictionary_size = len(self.df_map)
        processed = 0
        for term in self.df_map:
            cur.execute("""
                        REPLACE INTO posting_list('term', 'doc_frequency', 'term_frequency')
                        VALUES (?, ?, ?);""", (term, self.df_map[term], self.tf_map[term]))
            # self.con.commit()
            processed += 1
            progress = 100 * processed / dictionary_size
            print("POSTING LIST COMPLETION: %.2f" % progress, "%")

        self.con.commit()
        self.con.close()
        return

    def __apply_stemming__(self, word_list, filter):
        new_list = {}
        for word in word_list.split():
            stemmed = self.__special_remove__(self.stemmer.stem(word))
            if filter.filter(stemmed) == False:
                value = 0
                if stemmed in new_list:
                    value = new_list.get(stemmed)
                new_list.update({stemmed: (value + 1)})
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

    def __add_bow__(self, cur, word_list, row_id):
        word_map = self.__apply_stemming__(word_list, self.filter)
        rows = []
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
        return
