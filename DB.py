# coding: utf-8

from ConfigParser import SafeConfigParser
import sqlite3 as sqlite


class DB(object):
    def __init__(self, name):
        self.name = name

    def connect(self):
        sqlite.connect(self.name)


def main():
    config = SafeConfigParser()
    config.read('config.ini')
    db = DB(config.get("db", "name"))
    db.connect()


if __name__ == "__main__":
    main()
