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

  output = ""

  if(t):
    output += "# "+xml.find("h1").text+"\n\n"
    output += "| Logo | Name  | Link |\n"
    output += "| ---- | ----  | ---- |\n"

  urls = xml.find_all("div", class_="list-item-sq-small")
  for url in urls:
      img = url.find("img")["src"].split("?")[0].strip()
      name = url.find(class_="name").text.strip()
      link = url.find("a")["href"][1:].strip()
      output += "| !["+name+"]("+img+") | "+name+" | ["+name+"]("+link+")\n"

  next = xml.find("a", class_="page-link")
  if next:
    output += ListLogo("https://companieslogo.com"+next["href"])

  if t:
    path = ulink.replace("https://companieslogo.com/", "")
    print(path)
    os.makedirs(path, exist_ok=True)
    f = open(path+"README.MD", "w")
    f.write(output)
    f.close()

  return output


#a = ListLogo("https://companieslogo.com/logos/investment/")
#print(a)
home = requests.get("https://companieslogo.com/")
homexml = BeautifulSoup(home.text, features="lxml")
homeurls = homexml.find(class_="table-container").find_all("a", class_="dropdown-item")

for i in homeurls:
  f = ListLogo("https://companieslogo.com"+i["href"], True)
  #print(f)
  #break

# p = Pool(50)
# for i, _ in enumerate(p.imap_unordered(ListLogo, homeurls), 1):
#     sys.stderr.write('\rdone {0:%}'.format(i/len(homeurls)))