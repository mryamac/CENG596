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

    def generate_corpus(self):
        with open("lyrics-data.csv", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[4] == 'ENGLISH':
                    values_to_insert = (line_count + 1, row[0], row[1], row[3])
                    try:
                        line_count += 1
                        self.__add_bow__(row[3], line_count)
                        print(f'Processed {line_count} lines. \tTrack artist: {row[0]} name: {row[1]} {row[2]}')
                    except:
                        print(f'*****SKIP DUBLICATE. \tTrack artist: {row[0]} name: {row[1]} {row[2]}')

        return self.corpus

    def __apply_stemming__(self, word_list, filter):
        new_list = []
        for word in word_list.split():
            stemmed = self.__special_remove__(self.stemmer.stem(word))
            if filter.filter(stemmed) == False:
                new_list.append(stemmed)

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
        self.corpus.append(word_map)
        return
