class StopwordFilter:

    stop_words = {"i", "could", "feel", "at", "the", "time", "as"}

    def __init__(self):
        pass

    def set_stop_words(self, stop_word_list):
        self.stop_words = stop_word_list
        return

    def filter(self, word_map):

        for w in self.stop_words:
            word_map = list(filter((w).__ne__, word_map))

        return word_map

    def filter(self, word):
        return self.stop_words.__contains__(word)