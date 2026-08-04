import sqlite3


class UserBase:
    database_conn: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self, path: str):
        self.database_conn = sqlite3.connect(path)
        self.cur = self.database_conn.cursor()

    def check_password(self, name, password):
        self.cur.execute("SELECT * FROM users where name='{name}'".format(name=name))
        row = self.cur.fetchall()[0]
        if row[2] == password:
            return True
        else:
            return False
