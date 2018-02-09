# coding: UTF-8

import requests
from bs4 import BeautifulSoup
import csv
import re
import time

url = "https://content-tokyo2018.tems-system.com/eguide/jp/list"

html = requests.get(url).content

soup = BeautifulSoup(html,"html5lib")

exs = soup.find_all(class_="exhibitor_list_article clearfix")

result=[]
num=0

def getnexttext(soup, key):
    search_re = re.compile(key)
    text = soup.find(text=search_re)
    if text is None:
       return ""
    return list(text.parent.parent.stripped_strings)[1].encode("utf8")

for ex in exs:
  for li in ex.find_all("li"):
    if li is not None:
       cm = list(li.stripped_strings)
       cm = [ v.encode('utf8') for v in cm ]
       subresult=[cm[0],cm[1]]
       num+=1
       print(num)
       print(cm[0])
       time.sleep(1)

       a = li.find("a")
       if a is None:
          subresult.append("")
          subresult.append("")
          result.append(subresult)
          continue
       pre1 = a["id-name"] 
       pre2 = a["val-id"]
       suburl = "https://content-tokyo2018.tems-system.com/eguide/jp/"+pre1+"/details?id="+pre2
       r = requests.get(suburl)
       subhtml = r.text.encode(r.encoding)
       subsoup = BeautifulSoup(subhtml,"html5lib")
       
       if "CR" in pre1:
          zone = subsoup.find(style="font-size: 12px;").text.encode("utf8")
       else:
          zone = getnexttext(subsoup,u"出展ゾーン名") 
       print(zone)
       url = getnexttext(subsoup,u"URL") 
       print(url)

       subresult.append(zone)
       subresult.append(url)
       result.append(subresult)

f = open('contenttokyolist.csv', 'w')
writer = csv.writer(f, lineterminator='\n') 
writer.writerows(result)
