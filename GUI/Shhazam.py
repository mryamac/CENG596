from Score import Score


# Python program to sort a list of
# tuples by the second Item using sort()

# Function to sort hte list by second item of tuple
def Sort_Tuple(tup):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    tup.sort(key=lambda x: x[1], reverse=True)
    return tup


class Shhazam:
    def __init__(self, number_of_songs, idf, preprocessor):
        self.k = number_of_songs
        self.score = Score(self.k)
        idfs = idf.split(".")
        self.score.set_doc_tfidf(idfs[1])
        self.score.set_query_tfidf(idfs[0])
        self.preprocessor = preprocessor

    # return track id
    def apply_query(self, query):
        query = self.preprocessor.get_words(query)
        self.score.feed_and_query(query)
        rank_list = Sort_Tuple(self.score.get_list())
        return rank_list[:self.k]
