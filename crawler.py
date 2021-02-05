import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import json
import datetime
# Time
def full():
    n = datetime.datetime.now()
    y = n.year
    m = n.month
    d = n.day
    h = n.hour
    mi = n.minute
    s = n.second
    da = "-"
    string = str(y)+da+str(m)+da+str(d)+da+str(h)+da+str(mi)+da+str(s)
    return string
# Format JSON
t = str(full())
oi = {'dictionary': {}}
# Get sitemap
print("Downloading main sitemap...")
html =  urlopen("https://www.dictionary.com/dictionary-sitemap/sitemap.xml")
# Format sitemap
print("Formatting sitemap...")
sitemap = html.read()
bs = BeautifulSoup(sitemap, 'html.parser')
urllist = bs.find_all("loc")
# Get sitemap
try:
    print("Downloading sitemap...")
    for loc in urllist:
        uri = loc.get_text()
        print("Downloading " + uri + "...")
        os.system("curl -O -L " + uri)
except:
    print("Skipped download.")
# Extract sitemap
smn = os.listdir(os.getcwd())
try:   
    os.chdir("/home/runner/dictionary_crawler_project/sm")
    obj = open("/home/runner/dictionary_crawler_project/dict/" + str(t) + "-dictionary.json", 'w')
    for gz in smn:
        print("Extracting " + gz + "...")
        os.system("gzip -d " + gz)
        # Crawling
        xml = gz.replace(".gz", "")
        if "-additional" in xml:
            print("Skipped " + xml)
        elif "-supplemental" in xml:
            print("Skipped " + xml)
        elif "-list" in xml:
            print("Skipped " + xml)
        else:
            print("Trying to crawl " + xml)
        x = open(xml).read()
        bsxml = BeautifulSoup(x, 'html.parser')
        link = bsxml.find_all("loc")
        for lnk in link:
            lk = lnk.get_text()
            print("Crawling " + lk + " ...")
            h = urlopen(lk)
            bsd = BeautifulSoup(h.read(), 'html.parser')
            magele = bsd.find(class_='luna-pos')
            mag = magele.get_text()
            print("Part of speech: " + str(mag))
            wordele = bsd.find(class_='css-2m2rhw e1wg9v5m4')
            word = wordele.get_text()
            print("Word: " + str(word))
            defele = bsd.find(class_='css-1o58fj8 e1hk9ate4')
            defi = defele.get_text()
            print("Definition: " + str(defi))
            print("\nStoring...")
            o = {"word": str(word), "part of speech": str(mag),"definition": str(defi)}
            oi['dictionary'][word] = o
            print("\n\n\n")
except:
    json.dump(oi, obj)
    obj.close()
    
print("Mission accomplished.")
print("Quitting.")
exit
