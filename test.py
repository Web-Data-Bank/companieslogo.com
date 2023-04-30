from __future__ import division
from multiprocessing import Pool
from bs4 import BeautifulSoup
import requests
import sys
import os

def ListLogo(ulink, t = False):
  x = requests.get(ulink)
  response = x.text
  xml = BeautifulSoup(response, features="lxml")

  urls = xml.find_all("div", class_="list-item-sq-small")
  for url in urls:
    img = url.find("img")["src"].split("?")[0].strip()
    # Image Folder Make AND Download Image
    imgPath = url.find("img")["src"].split("?")[0].strip().split("/")
    imgPath.pop(0)
    imgURL = "https://companieslogo.com/"+"/".join(imgPath)
    imgPath.pop()
    imgPath = "/".join(imgPath)
    
    os.makedirs(imgPath, exist_ok=True)
    r = requests.get(imgURL, allow_redirects=True)
    open(imgURL.replace("https://companieslogo.com/",""), 'wb').write(r.content)
    
  next = xml.find("a", class_="page-link")
  if next:
    ListLogo("https://companieslogo.com"+next["href"])

  return 0


#a = ListLogo("https://companieslogo.com/logos/investment/")
#print(a)
home = requests.get("https://companieslogo.com/")
homexml = BeautifulSoup(home.text, features="lxml")
homeurls = homexml.find(class_="table-container").find_all("a", class_="dropdown-item")

e = 1
for i in homeurls:
  f = ListLogo("https://companieslogo.com"+i["href"], True)
  print(str(e)+"/"+str(len(homeurls)))
  e += 1
  #print(f)
  #break

# p = Pool(50)
# for i, _ in enumerate(p.imap_unordered(ListLogo, homeurls), 1):
#     sys.stderr.write('\rdone {0:%}'.format(i/len(homeurls)))