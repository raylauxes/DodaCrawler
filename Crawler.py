# coding: utf-8

import requests
from ConfigParser import SafeConfigParser
from bs4 import BeautifulSoup

config = SafeConfigParser()
config.read('config.ini')


class Crowler(object):
    def __init__(self):
        self.domain_url = config.get("doda", "domain_url")
        self.session = requests.session()
        self.login()

    def login(self):
        """
        DODAにログインします
        """
        section = "login"
        user = config.get(section, "user")
        password = config.get(section, "password")
        login_url = self.domain_url + config.get(section, "path")
        payload = {
                "mailAddress": user,
                "password": password,
                "doLogin": u"同意してログイン",
                "autoLogin": "checked"
                }
        self.post(login_url, payload)

    def fetch_job_list(self):
        """
        キャリアアドバイザーから紹介される求人の詳細を取得
        """
        section = "referredJobList"
        url = self.domain_url + config.get(section, "path")
        html = self.get(url)

        # 詳細のURLを取得
        bs = BeautifulSoup(html, "html.parser")
        res = bs.find_all("a", class_="btnList02")
        for r in res:
            print self.domain_url + r.get("href")

    def post(self, url, payload):
        res = self.session.post(url, data=payload)
        res.raise_for_status()
        return res.text

    def get(self, url):
        res = self.session.get(url)
        res.raise_for_status()
        return res.text


def main():
    c = Crowler()
    c.fetch_job_list()


if __name__ == "__main__":
    main()
