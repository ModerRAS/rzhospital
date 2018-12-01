#!/bin/env python
import requests
from bs4 import BeautifulSoup
import os
import time
import subprocess
import re
import config

sleep_time = 60
DIR = config.DIR


def git():
    for i in DIR:
        os.chdir(i)
        try:
            add = subprocess.check_output("git add .", shell=True)
        except subprocess.CalledProcessError as e:
            add = e.output
        pattern = "nothing to commit, working tree clean"
        try:
            commit = subprocess.check_output("git commit -m \"AutoSave --AutoGit\"", shell=True)
        except subprocess.CalledProcessError as e:
            commit = e.output

        if re.search(pattern, commit.decode('utf-8')) is not None:
            return 0
        else:
            print(time.asctime(time.localtime(time.time())))
            print(add.decode('utf-8'))
            print(commit.decode('utf-8'))
            os.system("git push")
            print("One loop end.")
            return 0


def rss_create(data):
    """
    数据格式:列表中每一项都是{title:"",link:"",description:""}
    :param data:
    :return:
    """
    t = time.asctime()
    output = ["<rss version=\"2.0\"><channel>"
              "<title>日照市中医医院通知</title>"
              "<description>Powered by ModerRAS</description>"
              "<link>http://www.rzhtcm.com/mobile/index.php</link>"
              "<generator>Python 3</generator>"
              "<language>zh-cn</language>"
              "<ttl>600</ttl>"
              ]
    for i in data:
        item = ["<item>"
                "<title><![CDATA[ " + i["title"] + " ]]></title>",
                "<description>" + i["description"] + "</description>",
                "<guid>" + i["link"] + "</guid>",
                "<link>" + i["link"] + "</link>",
                "</item>"]
        output.append("".join(item))
    output.append("</channel></rss>")
    return "".join(output)


def rss_save(rss, file):
    with open(file, "w", encoding='utf-8') as f:
        f.write(rss)
    pass


def spider():
    r = requests.get("http://www.rzhtcm.com/mobile/index.php")
    soup = BeautifulSoup(r.text)
    center = soup.select(".tzgg-center")[0].select(".tz-con")
    links = center[0].select("a")
    data = []
    for i in links:
        link = "http://www.rzhtcm.com" + i.get("href")
        description = more_info(link)
        title = i.select(".tz-content")[0].text
        data.append({
            "title": title,
            "description": description,
            "link": link
        })

    return rss_create(data)


def more_info(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    return soup.select(".list-content")[0].prettify()


def loop():
    rss = spider()
    rss_save(rss, "feed.xml")
    git()


if __name__ == '__main__':
    while True:
        loop()
        time.sleep(sleep_time)
