import math
import sqlite3


class TFIDF:

    def __init__(self, tf="n", max_tf=1, ave_tf=1, df="n", n=1, norm="n"):
        self.tf_type = tf
        self.max_tf = max_tf
        self.ave_tf = ave_tf

        self.df_type = df
        self.N = n

        self.norm = norm

    def get_term_frequency(self, tf):
        if tf == 0:
            return 0
        if self.tf_type == "l":
            return 1 + math.log10(tf)
        elif self.tf_type == "a":
            return 0.5 + (0.5 * tf) / self.max_tf
        elif self.tf_type == "b":
            return 1 if tf > 0 else 0
        elif self.tf_type == "L":
            return (1 + math.log10(tf)) / (1 + math.log10(self.ave_tf))
        else:
            return tf

    def get_document_frequency(self, df):
        if self.df_type == "t":
            return math.log10(self.N / df)
        elif self.df_type == "p":
            return max(0, math.log10((self.N - df) / df))
        else:
            return 1

    def get_normalization(self, d):
        if self.norm == "c":
            return 1 / d
        else:
            return 1
