import re
from bs4 import BeautifulSoup
import requests
import os,sys

os.environ["DJANGO_SETTINGS_MODULE"]='EaglePost.settings'

xEntry={}
full_Entry={}
list_full_Entry=[]
Entries=[]
content=""
response=None


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
    response = get_connections("http://punchng.com") 
    if(response):
        print("Received ",type(response))
        _content=response.text
        return _content

def process_content():
    global xEntry
    global Entries
    global full_Entry
    global list_full_Entry
    content=get_content()
    soup=BeautifulSoup(content,"html.parser")


    block=soup.find_all("div",class_=re.compile("td_module_8|td_module_mx1|td_module_mx2"))

    for entry in block:
        xEntry["headline"]=entry.h3.text
        xEntry["url"]=entry.find("h3",class_="entry-title").find("a").get("href")
        try:
            xEntry["img_src"]=entry.find("div",class_="td-module-thumb").find("img").get("src")
            xEntry["is_feed"]=False;
        except Exception:
            xEntry["is_feed"]=True;
            xEntry["img_src"]=""
        Entries.append(xEntry)
        xEntry={}
        
    
    for i in Entries:
        url=i["url"]
        r=get_connections(url)
        try:
            txt=r.text
            bsoup=BeautifulSoup(txt,"html.parser")
            #bsoup.find("div",class_=re.compile("td-g-rec|td-a-rec")).extract()
            soup_article=bsoup.find("article")
            soup_article1=soup_article.select("div.td-g-rec")
            for i in soup_article1:
                i.extract()
            soup_article2=soup_article.select("div.td-a-rec")
            for i in soup_article2:
                i.extract()
            txt=str(soup_article)
            #print(txt)
            full_Entry["url"]=url
            full_Entry["content"]=txt
            list_full_Entry.append(full_Entry)
            full_Entry={}
        except Exception as e:
            print(e)




    return [Entries,list_full_Entry]

from app.models import *
def insertion_operation():
    

    p=process_content()
    c=Channel.objects.get(pk__icontains="punch")
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


#For Populating Entry Table
#for i in p[0]:
#...     try:
#...         Entry.objects.create(heading=i["headline"],page=i["url"],thumbnail=i["img_src"],date=datetime.datetime.today(),channel=c)
#...     except Exception as e:
#...         print(e)

#for populating story table
#for i in p[1]:
#    try:
#        Story.objects.create(heading=Entry.objects.get(page__icontains=i["url"]),content=i["content"])
#    except Exception as e:
#        print(e)
