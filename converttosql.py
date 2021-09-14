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
    def __init__(self ,seriaid ,name, cda_url):
        self.seriaid = seriaid
        self.name = name
        self.cda_url = cda_url

engine = create_engine('sqlite:///base.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

import os
from feedparser import parse
plakaty = list()
tytuly = list()
#opisy = list()
listaserii=list()
plakatydowyszukiwarki = list()
listadowyszukiwarki = list() 
listaodcinkow = list() 
id=int()
os.chdir("serie")
listaplikow=list(os.listdir())
def reflash():
    for i in range(len(listaplikow)):
        listaserii.append(parse(listaplikow[i]))
    for i in range(len(listaserii[0].entries)):
        print(listaserii[0].entries[i].get("title"))
    for i in range(len(listaserii)):
        plakaty.append(listaserii[i].feed.image_url)
        tytuly.append(listaserii[i].feed.title)
reflash()
for j in range(len(listaserii)):
	session.add(Seria(listaserii[j].feed.title, listaserii[j].feed.description, listaserii[j].feed.image_url, listaserii[j].feed.rate))
	for i in range(len(listaserii[j].entries)):
		session.add(Odcinek(j+1, listaserii[j].entries[i].title, listaserii[j].entries[i].link))
session.commit()