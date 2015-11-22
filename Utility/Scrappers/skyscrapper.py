import re
from bs4 import BeautifulSoup
import requests
import os,sys

os.environ["DJANGO_SETTINGS_MODULE"]='EaglePost.settings'

xEntry={}
full_xEntry={}
list_full_xEntry=[]
Entries=[]
content=""
response=None
base_url="http://news.sky.com/"

def get_connections(path):
    try:
        print("Trying........................... ",path)
        r=requests.get(path)
        print(r," of ",type(r))
        return r
    except Exception:
        print(Exception)
        get_connections(path)



def get_content():
    response = get_connections("http://news.sky.com/") 
    if(response):
        print("Received ",type(response))
        _content=response.text
        return _content



def process_content():
    global xEntry
    global Entries
    global full_xEntry
    global list_full_xEntry
    content=get_content()
    soup=BeautifulSoup(content,"html.parser")


    for n in soup.select(".section-top-stories"):
        for m in n.select(".headline--section-top-stories"):
            xEntry["headline"]=m.text
            xEntry["url"]=base_url+m.find_parent("a").attrs["href"]
            xEntry["img_src"]=m.find_parent("li").find("img").attrs["src"]
            Entries.append(xEntry)
            xEntry={}

    for i in Entries:
        url=i["url"]
        r=get_connections(url)
        try:
            txt=r.text
            bsoup=BeautifulSoup(txt,"html.parser")
            #bsoup.find("div",class_=re.compile("td-g-rec|td-a-rec")).extract()
            soup_article=bsoup.select(".content-column")[0]
            
            txt=str(soup_article)
            #print(txt)
            full_xEntry["url"]=url
            full_xEntry["content"]=txt
            list_full_xEntry.append(full_xEntry)
            full_xEntry={}
        except Exception as e:
            print(e)




    return [Entries,list_full_xEntry]


from app.models import *
def insertion_operation():
    

    p=process_content()
    c=Channel.objects.get(pk__icontains="bbc")
    for i in p[0]:
         try:
             Entry.objects.create(heading=i["headline"],page=i["url"],thumbnail=i["img_src"],date=datetime.datetime.today(),channel=c)
         except Exception as e:
             print(e)


    for i in p[1]:
        try:
            Story.objects.create(heading=Entry.objects.get(page__icontains=i["url"]),content=i["content"])
        except Exception as e:
            print(e)




if __name__=="__main__":
    insertion_operation()