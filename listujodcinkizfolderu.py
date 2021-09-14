import re
import requests
import jinja2
from bs4 import BeautifulSoup
from soupsieve.css_match import RE_DATE
import sys
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()

class Seria(Base):
    __tablename__="serie"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    opis = Column(String)
    image_url = Column(String)
    rate = Column(Integer)
    def __init__(self, name, opis, image_url, rate):
        self.name = name
        self.opis = opis
        self.image_url = image_url
        self.rate = rate

class Odcinek(Base):
    __tablename__="odcinki"
    id = Column(Integer, primary_key=True)
    seriaid = Column(Integer)
    name = Column(String)
    cda_url = Column(String)

    def __init__(self, seriaid, name, cda_url):
        self.seriaid = seriaid
        self.name = name
        self.cda_url = cda_url

engine = create_engine('sqlite:///base.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


tytuly=list()
links=list()
opis=str()
def addserie(tytul, linkdocda, iloscstron):
    for i in range(iloscstron):
        strona = requests.get(linkdocda+"/"+str(i+1))
        soup = BeautifulSoup(strona.content, 'html.parser')
        linki=list(soup.find_all("a", {"class":"link-title-visit"}, href=True))
        for a in linki:
            session.add(Odcinek(session.query(Seria).order_by(Seria.id.desc()).first().id+1, a.get_text(), "https://www.cda.pl"+a['href']))
    response = requests.get("https://api.jikan.moe/v3/search/anime?q="+str(tytul))
    data=response.json()
    #data=json.load(plik)
    tytulzapi=data["results"][0]["title"]
    opis=data["results"][0]["synopsis"]
    obrazek=data["results"][0]["image_url"]
    score=data["results"][0]["score"]
    pegi=data["results"][0]["rated"]
    wychodzoncy=data["results"][0]["airing"]
    iloscodcinkow=data["results"][0]["episodes"]
    #wydanie=str(data["results"][0]["start_date"]+"-"+["results"][0]["end_date"])
    linki.clear()
    tytuly.clear()
    session.add(Seria(tytulzapi, opis, obrazek, score))
    session.commit()