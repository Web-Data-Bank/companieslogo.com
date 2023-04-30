from __future__ import division
from multiprocessing import Pool
from bs4 import BeautifulSoup
import requests
import os
import hashlib

def download_image(img_url, img_path):
    if os.path.exists(img_path):
        return
    try:
        r = requests.get(img_url, allow_redirects=True, timeout=10)
        open(img_path, 'wb').write(r.content)
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

def process_page(ulink):
    try:
        x = requests.get(ulink, timeout=10)
        response = x.text
        xml = BeautifulSoup(response, features="lxml")
    except Exception as e:
        print(f"Failed to process {ulink}: {e}")
        return

    urls = xml.find_all("div", class_="list-item-sq-small")
    for url in urls:
        img_url = url.find("img")["src"].split("?")[0].strip()
        img_path = img_url.replace("https://companieslogo.com/","")
        img_md5 = hashlib.md5(img_path.encode()).hexdigest()
        img_path = os.path.join("images", img_md5[:2], img_md5[2:4], img_md5)
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        download_image(img_url, img_path)
    
    next = xml.find("a", class_="page-link")
    if next:
        process_page("https://companieslogo.com"+next["href"])

    return 0

if __name__ == '__main__':
    home = requests.get("https://companieslogo.com/")
    homexml = BeautifulSoup(home.text, features="lxml")
    homeurls = homexml.find(class_="table-container").find_all("a", class_="dropdown-item")

    p = Pool(50)
    for i, _ in enumerate(p.imap_unordered(process_page, ["https://companieslogo.com" + i["href"] for i in homeurls]), 1):
        print('\r{0:%} done'.format(i/len(homeurls)), end='')

