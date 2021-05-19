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
    def __init__(self):
        pass

    def __split_query__(self, query):
        return query.split()

    # return track id
    def apply_query(self, query):
        word_list = self.__split_query__(query)

        results = Score(10)
        results.feed_and_query(word_list)
        list = Sort_Tuple(results.get_list())
        return list[:10]
