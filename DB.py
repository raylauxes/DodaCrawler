# coding: utf-8

from ConfigParser import SafeConfigParser
import sqlite3 as sqlite

config = SafeConfigParser()
config.read('config.ini')


class DodaDB(object):
    def __init__(self, name):
        self.name = name

    def create_company_table(self):
        """
        会社情報テーブルを作成
        """
        with sqlite.connect(self.name) as con:
            sql = config.get("db", "sql_create")
            c = con.cursor()
            c.execute(sql)


def main():
    db = DodaDB(config.get("db", "name"))
    db.create_company_table()


if __name__ == "__main__":
    main()
