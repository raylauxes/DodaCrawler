# coding: utf-8

import requests
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')


class Crowler(object):
    def __init__(self):
        self.session = requests.session()
        self.login()

    def login(self):
        section = "login"
        user = config.get(section, "user")
        password = config.get(section, "password")
        login_url = config.get(section, "url")
        payload = {
                "mailAddress": user,
                "password": password,
                "doLogin": u"同意してログイン",
                "autoLogin": "checked"
                }
        self.post(login_url, payload)

    def post(self, url, payload):
        res = self.session.post(url, data=payload)
        res.raise_for_status()
        print res.text


def main():
    Crowler()


main()
