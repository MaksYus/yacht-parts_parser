import requests
from bs4 import BeautifulSoup

path = "https://yacht-parts.ru/catalog/"
req = requests.get(path)

src = req.text
# print(src)

soup = BeautifulSoup(src, 'lxml')
title = soup.title.string

print(title)
