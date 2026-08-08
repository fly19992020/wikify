import sqlite3
import time


class HistoryBase:
    database_conn: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self, path: str):
        self.database_conn = sqlite3.connect(path)
        self.cur = self.database_conn.cursor()

    def add_history(self, user, page):
        self.cur.execute("SELECT MAX(id) FROM histories")
        c_id = self.cur.fetchall()[0][0] + 1
        timestamp = int(time.time())
        self.cur.execute("INSERT INTO histories VALUES(?, ?, ?, ?)",
                         [c_id, user, page, timestamp])
        self.database_conn.commit()
