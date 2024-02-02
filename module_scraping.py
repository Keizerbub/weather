from bs4 import BeautifulSoup as bs # manipumation des fichiers html
from urllib.request import urlopen as ur, Request as re # manipulation http
import pandas as pd #pour la manioulation des data frames 
import time as t # pour les pauses
import datetime as dt # pour gérer le temps
import json

def downloading_links(url, info):
    if info == True:
        print("---getting to the url---")
        page=re(url,headers={"User-agent":"Mozilla/5.0"})
        html=ur(page)
        soup=bs(html)
        
        
        #getting the APi results
        print("---\ngetting API result---")
        search=soup.find_all("p")
        print("---success:1---")
        
        #transform our html to text, then in json format 
        print("\nsecond part")
        print("---transforming in text---")
        texte=search[0].text
        texte=json.loads(texte)
        print("---success:2---")
        
        #going in our json
        print("\nthird part")
        print("---data---")
        json_data=texte['data']
        print("---success:3---")

        #final step: getting links
        print("\nfourth part")
        print("---getting links---")
        
        #list to keep result
        result=[]
        
        #adding found links to result
        for i in json_data:
            element=i['url']
            result.append(element)
            
        #returning result
        print("---success:4---\n")
        return result
    
    else:
        page=re(url,headers={"User-agent":"Mozilla/5.0"})
        html=ur(page)
        soup=bs(html)
        search=soup.find_all("p")
        texte=search[0].text
        texte=json.loads(texte)
        json_data=texte['data']
        result=[]
        for i in json_data:
            element=i['url']
            result.append(element)
        print("---success::True---\n")
        return result
    
def open_link(url):
    pass


"""
#testing download link
site=r"https://www.data.gouv.fr/api/2/datasets/6569b4473bedf2e7abad3b72/resources/?page=1&page_size=6&type=main&q="
test1=downloading_links(url=site,info=True)
print(test1)
"""