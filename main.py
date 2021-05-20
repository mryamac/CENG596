from PreProcess import PreProcess
from Shhazam import Shhazam
from StopwordFilter import StopwordFilter

# method = Shhazam()
# print("start")
# print(method.apply_query("know you and our automobile automatic i"))
# print("finish")

preprocess = PreProcess("lancaster")

corpus = preprocess.generate_corpus()
print(corpus)

filter = StopwordFilter()
filter.set_stop_words({"a", "an", "and", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"})
print("AFTER STOP WORD FILTERING")
print(filter.filter(corpus))