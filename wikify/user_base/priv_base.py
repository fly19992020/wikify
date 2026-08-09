import sqlite3


class PrivBase:
    database_conn: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self, path: str):
        self.database_conn = sqlite3.connect(path)
        self.cur = self.database_conn.cursor()

    def check_edit(self, name):
        self.cur.execute("SELECT * FROM privileges where username=?", [name])
        row = self.cur.fetchall()[0]
        if row[1] == 1:
            return True
        else:
            return False
