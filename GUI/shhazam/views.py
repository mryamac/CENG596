import sqlite3

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from PreProcess import PreProcess
from Shhazam import Shhazam
from StopwordFilter import StopwordFilter
from rank_bm25 import BM25Okapi


class Ranking:
    preprocess = None
    bm25 = None
    conn = None

    def initialize():
        Ranking.preprocess = PreProcess("lancaster")
        Ranking.conn = sqlite3.connect('dataset_v3.db')
        Ranking.corpus = Ranking.preprocess.generate_corpus(Ranking.conn, False)
        Ranking.bm25 = BM25Okapi(Ranking.corpus, k1=1.5, b=0.5)

    def get_ranks(query_str):
        query = Ranking.preprocess.get_words(query_str)
        scores = Ranking.bm25.get_scores(query)
        index = list(range(1, len(scores) + 1))
        result = sorted(zip(scores, index), reverse=True)[:10]

        dict = {}
        resp = []
        for song in result:
            cur = Ranking.conn.cursor()
            for row in cur.execute("SELECT * FROM track_info where track_id =" + str(song[1])):
                song = {'name': row[2], 'lyric': row[3][0: 100]}
                resp.append(song)
        dict["result"] = resp
        return JsonResponse(dict)


# Create your views here.
# This function will return and render the home page when url is http://localhost:8000/to_do/.

def index_page(request):
    # Get the index template file absolute path.
    # index_file_path = PROJECT_PATH + '/pages/home.html'
    # Return the index file to client.
    Ranking.initialize()
    return render(request, 'index.html')


def song_list(request):
    # "cant get you out of my head"
    result = Ranking.get_ranks(request.POST['text'])
    return HttpResponse(result)
