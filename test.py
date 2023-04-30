from multiprocessing import Pool
from bs4 import BeautifulSoup
import requests
import os

def CreateMD(url):
    path = url.replace("https://companieslogo.com/","")
    os.makedirs(path, exist_ok=True)

    x = requests.get(url)
    response = x.text
    xml = BeautifulSoup(response, features="html.parser")

    output = ""

    title = xml.find("h1", class_="h1-title").text
    output = "# " + title + "\n\n"
    
    subheading = xml.find_all("h2", class_="logo-title")
    c = 0
    for a in xml.find_all("div", class_="download-button-container"):
        output += "## "+subheading[c].text+"\n\n"

        for link in a.find_all("a"):
            output += "### "+subheading[c].text.strip()+" "+link.text.strip()+"\n\n"
            output += "!["+subheading[c].text.strip()+" "+link.text.strip()+"]("+(link["href"].split("?")[0])+")\n\n"

            # Image Folder Make AND Download Image
            imgPath = link["href"].split("?")[0].split("/")
            imgPath.pop(0)
            imgURL = "https://companieslogo.com/"+"/".join(imgPath)
            imgPath.pop()
            imgPath = "/".join(imgPath)
            os.makedirs(imgPath, exist_ok=True)
            r = requests.get(imgURL, allow_redirects=True)
            open(imgURL.replace("https://companieslogo.com/",""), 'wb').write(r.content)

        c += 1




    about = xml.findAll("div", class_="logo-section")
    aboutHTML = about[len(about)-1].find_next_sibling("div")
    output += "## "+aboutHTML.find("h2").text+"\n\n"
    output += ""+aboutHTML.find("p").text+"\n\n"
    li = 1
    for ul in aboutHTML.find("ul"):
        output += str(li)+". "+ul.text+"\n"
        li += 1
    
    output += "\n\n## Categories\n"
    for category in xml.findAll(class_="category-badge"):
        output += "- [x] "+category.text.strip()+"\n"
    #print(output)
    
    f = open(path+"README.MD", "w")
    f.write(output)
    f.close()

url = "https://companieslogo.com/sitemap.xml"

x = requests.get(url)
response = x.text#urllib.request.urlopen(url)
xml = BeautifulSoup(response, features="xml")

urls = xml.find_all("url")
df = []
for url in urls:
    loc = url.findNext("loc").text
    df.append(loc)


with Pool(50) as p:
  outputs = p.map(CreateMD, df)