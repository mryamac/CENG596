from PreProcess import PreProcess
from Shhazam import Shhazam
from StopwordFilter import StopwordFilter
from datetime import datetime

from TFIDF import TFIDF

preprocess = PreProcess("lancaster")

start = datetime.now()

start_time = start.strftime("%H:%M:%S")
# corpus = preprocess.generate_corpus()
finish = datetime.now()
finish_time = finish.strftime("%H:%M:%S")
print("Start Time =", start_time)
print("Finish Time =", finish_time)

shhazam = Shhazam(10, "lnc.ltc", preprocess)
print(shhazam.apply_query("Jenny whistle I"))
