import sqlite3


class IDF:

    def __init__(self):
        pass

    @staticmethod
    def basic_postings(word,limit):
        conn = sqlite3.connect('mxm_dataset.db')
        cur = conn.cursor()
        list = []
        for row in cur.execute("SELECT * FROM lyrics where word='" + word + "' order by mxm_tid asc"):
            list.append((row[1], row[3]))
        conn.close()
        return list
