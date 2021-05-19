import heapq
from _heapq import heappush, heappushpop

from IDF import IDF


class Score:
    def __init__(self, k):
        self.k = k
        self.song_list = []

    def merge_list(self, plist):
        j = 0
        i = 0
        while True:
            if len(self.song_list) <= i:
                heappush(self.song_list, plist[j])
                j += 1
            elif len(plist) <= j:
                break
            elif plist[j][0] == self.song_list[i][0]:
                self.song_list[i] = (self.song_list[i][0], self.song_list[i][1] + plist[j][1])
                i += 1
                j += 1
            elif plist[j][0] > self.song_list[i][0]:
                i += 1
            else:
                heappush(self.song_list, plist[j])
                j += 1

    def feed_and_query(self, word_list):
        for word in word_list:
            postings_list = IDF.basic_postings(word, self.k)
            self.merge_list(postings_list)

    def get_list(self):
        return self.song_list
