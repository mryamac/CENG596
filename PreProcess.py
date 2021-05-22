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
        self.con = sqlite3.connect("dataset_v2.db")

    def generate_corpus(self):
        cur = self.con.cursor()
        with open("lyrics-data.csv", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[4] == 'ENGLISH':
                    line_count += 1
                    values_to_insert = (line_count, row[0], row[1], row[3])
                    cur.execute("""
                        INSERT INTO track_info ('track_id', 'artist', 'track_name', 'lyrics')
                        VALUES (?, ?, ?, ?)""", values_to_insert)
                    
                    self.con.commit()
                    self.__add_bow__(cur, row[3], line_count)
                    print(f'Processed {line_count} lines. \tTrack artist: {row[0]} name: {row[1]} {row[2]}')
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

    def __get_words__(self, lyrics):
        return lyrics.split()

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
            cur.execute("""
                        INSERT INTO track_words ('track_id', 'word', 'count')
                        VALUES (?, ?, ?);""", (row_id, w, word_map.get(w)))

            cur.execute("""
                        SELECT term_frequency FROM posting_list WHERE term = ?;""", (w,))
            
            result = cur.fetchall()
            tf = word_map.get(w)
            if len(result) != 0:
                tf += result[0][0]
            
            cur.execute("""
                        REPLACE INTO posting_list('term', 'term_frequency')
                        VALUES (?, ?);""", (w, tf))

        self.con.commit()
        return
