#!/bin/env python
import time

import requests
from bs4 import BeautifulSoup


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


def main():
    rss = spider()
    rss_save(rss, "feed.xml")


if __name__ == '__main__':
    main()
