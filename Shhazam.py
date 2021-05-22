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
    def __init__(self, number_of_songs):
        self.k = number_of_songs

    def __split_query__(self, query):
        return query.split()

    # return track id
    def apply_query(self, query):
        results = Score(self.k)
        results.feed_and_query(query)
        rank_list = Sort_Tuple(results.get_list())
        return rank_list[:self.k]
