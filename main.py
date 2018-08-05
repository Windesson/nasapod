#!/usr/bin/python
# --*-- coding:utf-8 -*-
import urllib.request as request
from string import Template
from bs4 import BeautifulSoup

archive_url = "https://apod.nasa.gov/apod/archivepix.html"
apod_url = "https://apod.nasa.gov/apod/"
img_active = True


def get_img_url(url):
    data = request.urlopen(url).read()
    soup = BeautifulSoup(data, features="html5lib")
    try:
        return apod_url + soup.find_all("img")[0].get('src')
    except IndexError:
        pass


def get_state():
    global img_active
    if img_active:
        img_active = False
        return "active"
    return ""


def get_archives():
    data = request.urlopen(archive_url).read()
    soup = BeautifulSoup(data, features="html5lib")
    return [(apod_url + link.get('href'), link.getText(), get_state()) for link in soup.find_all('a') if
            str(link.get('href')).startswith('ap')]


def main():
    index_template = Template(open("templates/index.html").read())
    carousel_template = Template(open("templates/carousel.html").read())
    archives = get_archives()
    carousel = [carousel_template.substitute(url=get_img_url(link[0]), text=link[1], active=link[2]) for link in
                archives[:40] if get_img_url(link[0])]

    index_html = index_template.substitute(nasa_carousel="\n".join(carousel))

    open("index.html", "w").write(index_html)


if __name__ == "__main__":
    main()
