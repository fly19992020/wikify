import sqlite3

from flask import render_template_string
from markupsafe import Markup, escape


class PageBase:
    database_conn: sqlite3.Connection = None
    cur: sqlite3.Cursor = None
    prefix: str = ""

    def __init__(self, path: str, prefix: str):
        self.database_conn = sqlite3.connect(path)
        self.cur = self.database_conn.cursor()
        self.prefix = prefix

    def get_source_path(self, name: str):
        self.cur.execute("SELECT * FROM pages WHERE name = '{name}'".format(name=name))
        rows = self.cur.fetchall()
        if len(rows) == 0:
            return None
        row = rows[0]
        return row[1]

    def get_type(self, name: str):
        self.cur.execute("SELECT * FROM pages WHERE name = '{name}'".format(name=name))
        rows = self.cur.fetchall()
        if len(rows) == 0:
            return None
        row = rows[0]
        return row[2]

    def __del__(self):
        self.cur.close()
        self.database_conn.close()

    def get_page(self, name):
        f = self.get_source(name)
        if self.get_type(name) == "text/plain":
            with open("templates/country.html") as t:
                return render_template_string(t.read(),
                                              Title="Wikify",
                                              Home=Markup("<a href=\"/\">Home</a>"),
                                              Body=f
                                              )
        return f

    def write_page(self, name: str, content: str):
        s = self.get_source_path(name)
        if s is None:
            self.create_page(name, "text/plain")
            self.write_page(name, content)
            return
        f = open(self.prefix + s, "w")
        f.write(content)

    def get_source(self, name: str):
        s = self.get_source_path(name)
        f = open(self.prefix + s)
        return f.read()

    def create_page(self, name, mime):
        self.cur.execute("SELECT MAX(id) FROM pages")
        c_id = self.cur.fetchall()[0][0] + 1
        if mime == "text/plain":
            source = "{}.txt".format(c_id)
            open(source, "w").close()
            print("INSERT INTO pages VALUES ({id}, '{source}', '{mime}', '{name}')"
                  .format(id=c_id, source=source, mime=mime, name=name))
            self.cur.execute("INSERT INTO pages VALUES ({id}, '{source}', '{mime}', '{name}')"
                         .format(id=c_id, source=source, mime=mime, name=name))
            self.database_conn.commit()
