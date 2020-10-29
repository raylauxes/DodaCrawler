# coding: utf-8

import os
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
        print user
        password = config.get(section, "password")
        # print(password)
        login_url = self.domain_url + config.get(section, "path")
        # print(login_url)
        payload = {
                "mailAddress": user,
                "password": password,
                # "doLogin": u"同意してログイン",
                "doLogin": "同意してログイン",
                "autoLogin": "checked"
                }
        res = self.post(login_url, payload)

        # ログインの成否を判定
        # bs = BeautifulSoup(res, "html.parser")
        bs = BeautifulSoup(res, "html.parser").encode("utf-8")
        fail_title = config.get(section, "fail").decode("utf-8")
        print bs.find("title")
        if bs.find("title").text == fail_title:
            print (u"ログインに失敗しました。config.iniのuser, passwordを確認してください。")
            raise Exception
        return

    def remove_job_list(self):
        output_path = config.get("output", "path")
        files = os.listdir(output_path)
        for file_name in files:
            # ドットファイルは無視する
            if file_name[0] != ".":
                os.remove(output_path + "/" + file_name)

    def fetch_job_list(self):
        """
        キャリアアドバイザーから紹介される求人の詳細を取得
        """
        section = "referredJobList"
        url = self.domain_url + config.get(section, "path")

        job_urls = []

        # 次ページが存在する分求人URLを取得する
        while True:
            job_list_html = self.get(url)

            # 詳細のURLを取得
            bs = BeautifulSoup(job_list_html, "html.parser")
            res = bs.find_all("a", class_="btnList02")

            for r in res:
                job_urls.append(self.domain_url + r.get("href"))

            # 次ページの存在判定
            next_page = bs.find("li", class_="btn_r last")
            next_page = next_page.find("a")
            if next_page is None:
                break

            url = self.domain_url + next_page.get("href")

        # 求人ページのHTML出力する
        output_path = config.get("output", "path")
        for detail_url in job_urls:
            page = self.get(detail_url)

            with open(output_path + "/" + detail_url.split("=")[-2], "a") as f:
                f.write(page.encode("utf-8"))

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
    c.remove_job_list()
    c.fetch_job_list()


if __name__ == "__main__":
    main()
