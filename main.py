from PreProcess import PreProcess
from Shhazam import Shhazam

# method = Shhazam()
# print("start")
# print(method.apply_query("know you and our automobile automatic i"))
# print("finish")

preprocess = PreProcess("lancaster")

print(preprocess.generate_corpus())