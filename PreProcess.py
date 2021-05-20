import nltk
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer


class PreProcess:
    def __init__(self, stemmer):
        if stemmer == "lancaster":
            self.stemmer = LancasterStemmer()
        else:
            self.stemmer = PorterStemmer()

    def generate_corpus(self):
        # read doc.. get line .. get lyrics
        word_list = self.__get_words__(
            "I could feel at the time. There was no way of knowing. "
            "Fallen leaves in the night. Who can say where they're blowing. "
            "As free as the wind. Hopefully learning. Why the sea on the tide. "
            "Has no way of turning. More than this. You know there's nothing. "
            "More than this. Tell me one thing. More than this. "
            "You know there's nothing. It was fun for a while. "
            "There was no way of knowing. Like a dream in the night. "
            "Who can say where we're going. No care in the world. Maybe I'm learning. "
            "Why the sea on the tide. Has no way of turning. More than this. "
            "You know there's nothing. More than this. Tell me one thing. More than this. "
            "You know there's nothing. More than this. You know there's nothing. "
            "More than this. Tell me one thing. More than this. There's nothing.")
        word_list = self.__apply_stemming__(word_list)

        return word_list

    def __apply_stemming__(self, word_list):
        new_list = []
        for word in word_list:
            new_list.append(self.__special_remove__(self.stemmer.stem(word)))
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
