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
