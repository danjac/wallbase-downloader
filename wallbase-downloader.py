import sys
import requests
import pathlib

from html.parser import HTMLParser
from urllib.parse import urlparse


class WallbaseParser(HTMLParser):

    def handle_starttag(self, tag: str, attrs: list):
        if tag == "img":
            attrs_dct = dict(attrs)
            if attrs_dct.get("id") == "wallpaper" and "src" in attrs_dct:
                url = "https:" + attrs_dct["src"]
                download_image(url)


def download_image(url: str):
    print("found image", url)
    name = urlparse(url).path.split("/")[-1]
    target = pathlib.Path.home() / "Pictures" / "Wallpapers" / name
    print("writing to", target)
    response = requests.get(url)
    with open(target, "wb") as fp:
        fp.write(response.content)


def download(url: str):
    print("downloading", url)
    response = requests.get(url)
    parser = WallbaseParser()
    parser.feed(response.text)


if __name__ == "__main__":
    urls = sys.argv[1:]
    for url in urls:
        download(url)
