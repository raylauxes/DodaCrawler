# coding: utf-8

from ConfigParser import SafeConfigParser
import sqlite3 as sqlite



class DodaDB(object):
    def __init__(self, name):
        self.config = SafeConfigParser()
        self.config.read('config.ini')
        self.name = name

    def create_company_table(self):
        """
        会社情報テーブルを作成
        """
        with sqlite.connect(self.name) as con:
            sql = self.config.get("db", "sql_create")
            c = con.cursor()
            c.execute(sql)

    def is_exist_table(self):
        """
        会社情報テーブルが存在するかチェックする
        """
        with sqlite.connect(self.name) as con:
            sql = self.config.get("db", "sql_exist")
            c = con.cursor()
            # 結果集合の1件だけ取り出す
            res = c.execute(sql).fetchone()[0]

        return res

    def delete_company_row(self):
        """
        会社情報テーブルの行を全削除する
        """
        with sqlite.connect(self.name) as con:
            sql = self.config.get("db", "sql_delete")
            c = con.cursor()
            c.execute(sql)


def main():
    config = SafeConfigParser()
    config.read('config.ini')
    db = DodaDB(config.get("db", "name"))
    if not db.is_exist_table():
        db.create_company_table()
    db.delete_company_row()


if __name__ == "__main__":
    main()
