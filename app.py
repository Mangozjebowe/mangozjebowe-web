#/usr/bin/python3
from flask import render_template, Flask ,redirect, request, session as flasksession, url_for, abort, jsonify
import flask
import flask_monitoringdashboard as dashboard
from flask_cors import CORS
from sqlalchemy.sql.schema import ForeignKey
app = Flask(__name__, static_folder='static')
dashboard.config.init_from(file='config.cfg')
dashboard.bind(app)
CORS(app)
app.secret_key = 'SECRET_KEY'
import requests
import os
from scraper import wbijam as scraperwbijam 
users=list()
import bcrypt
import youtube_dl
ydl_opts = {
    'quiet': True
}
listamp4 = dict()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date
import requests
from bs4 import BeautifulSoup
from soupsieve.css_match import RE_DATE
Base = declarative_base()
class Seria(Base):
    __tablename__="serie"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    opis = Column(String)
    image_url = Column(String)
    rate = Column(Integer)
    orginalurl = Column(String)
    autorid = Column(Integer)
    add_date=Column(Date, server_default=func.current_date())
    airing = Column(Boolean)

    def __init__(self, name, opis, image_url, rate, orginalurl, autorid, airing):
        self.name = name
        self.opis = opis
        self.image_url = image_url
        self.rate = rate
        self.orginalurl = orginalurl
        self.autorid = autorid
        self.airing = airing
class Odcinek(Base):
    __tablename__="odcinki"
    id = Column(Integer, primary_key=True)
    seriaid = Column(Integer)
    name = Column(String)
    cda_url = Column(String)

    def __init__(self, seriaid, name, cda_url):
        self.seriaid= seriaid
        self.name = name
        self.cda_url = cda_url
        
class Users(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)
    admin = Column(Boolean)
    def __init__(self, name ,password, admin):
        super(Users, self).__init__()
        self.name = name
        self.password = password
        self.admin = admin
class Comment(Base):
    __tablename__ = "komentarze"
    id = Column(Integer, primary_key=True)
    autorid = Column(Integer)
    postid = Column(Integer)
    tresc = Column(String)
    def __init__(self, autorid, postid, tresc):
        self.autorid = autorid
        self.postid = postid
        self.tresc = tresc
class Pinned(Base):
    __tablename__="Pinned"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey(Users.id))
    seria = Column(Integer, ForeignKey(Seria.id))
    def __init__(self, user, seria):
        self.user=user
        self.seria=seria
def islogged():
    try:
        flasksession["user_id"]
        logged = True
    except:
        logged = False

    try:
        admin = bool(session.query(Users).filter(Users.id == flasksession["user_id"]).first().admin)
    except:
        admin = False
    return [logged, admin]
class Dodajserie():
    def getmetadata(tytul):
        response = requests.get("https://api.jikan.moe/v3/search/anime?q="+str(tytul))
        data=response.json()
        return {
            "tytulzapi": data["results"][0]["title"],
            "opis": data["results"][0]["synopsis"],
            "obrazek":data["results"][0]["image_url"],
            "score": data["results"][0]["score"],
            "pegi":data["results"][0]["rated"],
            "wychodzoncy":data["results"][0]["airing"],
            "iloscodcinkow":data["results"][0]["episodes"]
        }
    def cda(tytul, linkdocda, iloscstron):
        odcinki=list()
        for i in range(iloscstron):
            strona = requests.get(linkdocda+"/"+str(i+1))
            soup = BeautifulSoup(strona.content, 'html.parser')
            linki=list(soup.find_all("a", {"class":"link-title-visit"}, href=True))
            for a in linki:
                odcinki.append(
                {
                    "name":    a.get_text(), 
                    "player":     "https://www.cda.pl"+a['href']}
                )
        try:
            tytuly.clear()
            linki.clear()
        except:
            None
        metadata=Dodajserie.getmetadata(tytul)
        return {
            "metadata": metadata,
            "id":       session.query(Seria).order_by(Seria.id.desc()).first().id+1,
            "odcinki":  odcinki
        }
        session.commit()
    def wbijam(tytul, link):
        metadata=Dodajserie.getmetadata(tytul)
        try:
            odcinki.clear()
            print("cleared")
        except:
            None
        odcinki=scraperwbijam(link)
        return {
        "metadata": metadata,
        "id":       session.query(Seria).order_by(Seria.id.desc()).first().id,
        "odcinki":  odcinki
        }
def cdatomp4(link):
    try:
        listamp4.clear()
        print("cleared")
    except:
        None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(link, download=False) 
    try:
        for i in range(len(meta['formats'])):
            listamp4[meta['formats'][i]['height']]=meta['formats'][i]['url']
    except:
        listamp4["idk"]=meta['url']
    return(listamp4)

engine = create_engine('sqlite:///base.db', echo=True,
     connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
#API
from api import *
@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        flasksession.pop("user_id")
    except:
        None
    if request.method == "GET":
        return(render_template("login.html"))
    elif request.method == "POST":
        success=False
        flasksession.pop('user_id', None)
        nick=request.form["nick"]
        password=request.form["password"]
        urzyszkodnik=session.query(Users).order_by(Users.id).first()
        if urzyszkodnik.name == nick and password == urzyszkodnik.password:
            flasksession['user_id'] = urzyszkodnik.id
            success=True
        if success:
            return(redirect(url_for("index")))
        else:
            return("Failed")
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return(render_template("register.html"))
    else:
        session.add(Users(request.form['imie'], request.form['password'], False))
        session.commit()
        return redirect(url_for("index"))
@app.route("/")
def index():
    tytuly=session.query(Seria).order_by(Seria.name).all() 
    return render_template("index.html", tytuly=tytuly, logged=islogged())
@app.route("/anime/<id>")
def animesite(id):
    seria = session.query(Seria).filter(Seria.id == id).first()
    zrodlo = seria.orginalurl is not None
    odcinki = session.query(Odcinek).filter(Odcinek.seriaid == id)
    komentarze = session.query(Comment).filter(Comment.postid == id).all()
    badges=list()
    users.clear()
    autor = session.query(Users).filter(Users.id == seria.autorid).first()
    badges.append("Dodane przez: "+autor.name)
    # print("AUTORRRRR:", autor)
    for i in range(len(komentarze)):
        users.append(session.query(Users).filter(Users.id == komentarze[i].autorid).first().name)
    if seria.airing and seria.airing is not None :
        badges.append("wychodzący")
    elif seria.airing is not None:
        badges.append("zakończony")
    if seria.add_date is not None:
        badges.append("Dodane w: "+seria.add_date)
    return render_template("animesite.html",
        odcinki = odcinki,
        seria = seria,
        users=users,
        ilosckomentarzy=len(komentarze),
        komentarze=komentarze,
        logged=islogged(),
        zrodlo = zrodlo,
        badges=badges
        )
@app.route("/anime/<id>/pin")
def pin(id):
    session.add(Pinned(flasksession['user_id'], id))
    session.commit()
    return "succes"
@app.route("/anime/<id>/unpin")
def unpin(id):
    seria=session.query(Pinned).filter(Pinned.seria==id).first()
    session.delete(seria)
    if seria is None:
        return(jsonify(False))
    else:
        return(jsonify(True))

@app.route("/anime/<id>/refresh")
def refreshseries(id):
    seria=session.query(Seria).filter(Seria.id==id).first()
    if "wbijam" in seria.orginalurl:
        seriaupdated=Dodajserie.wbijam(seria.name, seria.orginalurl)
    elif "cda" in seria.orginalurl:
        iloscstron = int((session.query(Odcinek).filter(Odcinek.seriaid == seria.id).count())/36)+1
        # print("*0*0*0*0*0*0*0*", seria.name, seria.orginalurl, iloscstron)
        seriaupdated=Dodajserie.cda(seria.name, seria.orginalurl, iloscstron)
    # print("wychodzoncy: *****"+seriaupdated["metadata"]["wychodzoncy"])
    for i in session.query(Odcinek).filter(Odcinek.seriaid == id).all():
        session.delete(i)
    for i in seriaupdated["odcinki"]:
        session.add(Odcinek(
            seria.id,
            i["name"],
            i["player"]))
    if seriaupdated["metadata"]["wychodzoncy"]:
        ongoing=1
    elif seriaupdated["metadata"]["wychodzoncy"] is None:
        ongoing=0
    else:
        ongoing=0
    print(seriaupdated)
    session.query(Seria).filter(Seria.id == id).\
    update({Seria.airing: ongoing}, synchronize_session = False)

    session.commit()
    return redirect(url_for('animesite', id=id))

@app.route("/anime/<animeid>/add", methods=['POST'])
def addcomment(animeid):
    session.add(Comment(flasksession["user_id"], animeid, request.form["tresc"]))
    session.commit()
    return redirect(url_for('animesite', id = animeid))
@app.route("/anime/<id>/", methods=['POST'])
def addepizod(id):
    session.add(Odcinek(
        id,
        request.form["nazwa"], 
        request.form["linkdocda"]))
    session.commit()
    return redirect(url_for('animesite', id=id))
@app.route("/admin/<id>/remove")
def removeseries(id):
    if islogged()[1]:
        # open("logi", 'a').write(flasksession["user_id"]+" usunął "+session.query(Seria).filter(Seria.id == id).first().name + "/n")
        for i in session.query(Odcinek).filter(Odcinek.seriaid == id).all():
            session.delete(i)
        session.delete(session.query(Seria).filter(Seria.id == id).first())
        session.commit()
        return redirect(url_for('index'))
    else:
        abort(403)
@app.route("/epizod/<odcid>/remove")
def removeepizod(odcid):
    if islogged()[1]:
        odcinek = session.query(Odcinek).filter(Odcinek.id == odcid).first()
        seria = session.query(Seria).filter(Seria.id == odcinek.seriaid).first().id
        session.delete(odcinek)
        session.commit()
        return(redirect(url_for('animesite', id = seria)))
    else:
        abort(403)
@app.route("/epizod/<odcid>")
def odcinek(odcid):
    try:
        linki.clear()
    except:
        None
    odcinek = session.query(Odcinek).filter(Odcinek.id == odcid).first()
    listaodcinkow = session.query(Odcinek).filter(Odcinek.seriaid == odcinek.seriaid).all()
    linki = cdatomp4(odcinek.cda_url)
    return render_template("odcinek.html",
        odcinek=odcinek,
        listaodcinkow=listaodcinkow,
        linki=linki,
        klucze=linki.keys()
        )
@app.route('/szukajka', methods=['POST'])
def search():
    fraza=request.form['fraza']
    tytuly=session.query(Seria).filter(Seria.name.like("%{}%".format(fraza))).all()
    return render_template("index.html",
    logged=islogged(),
    tytuly=tytuly
    )
@app.route('/dodaj')
def handle_dataa():
    if islogged()[1]:
        return render_template("dodaj.html")
    else:
        abort(403)
@app.route('/dodaj/cda', methods=['POST'])
def dodajcda():
    if islogged()[1]:
        tytul=request.form["tytul"]
        linkdocda=request.form["link"]
        iloscstron=request.form["iloscstron"]
        seria=Dodajserie.cda(str(tytul),str(linkdocda), int(iloscstron))
        session.add(Seria(
            seria["metadata"]['tytulzapi'], 
            seria["metadata"]['opis'], 
            seria["metadata"]['obrazek'], 
            seria["metadata"]['score'],
            linkdocda,
            flasksession["user_id"],
            seria['metadata']['wychodzoncy']))
        for i in seria["odcinki"]:
            session.add(Odcinek(
                seria["id"],
                i["name"],
                i["player"]))
        session.commit()
        return redirect(url_for('index'))
    else:
        abort(403)
@app.route('/dodaj/wbijam', methods=['POST'])
def dodajwbijam():
    if islogged()[1]:
        tytul=request.form["tytul"]
        linkdowbijam=request.form["link"]
        seria=Dodajserie.wbijam(str(tytul), str(linkdowbijam))
        session.add(Seria(
            seria["metadata"]['tytulzapi'], 
            seria["metadata"]['opis'], 
            seria["metadata"]['obrazek'], 
            seria["metadata"]['score'],
            linkdowbijam,
            flasksession["user_id"],
            seria['metadata']['wychodzoncy']))
        for i in seria["odcinki"]:
            session.add(Odcinek(
                seria["id"],
                i["name"],
                i["player"]
            ))
        session.commit()
        return redirect(url_for('index'))
    else:
        abort(403)

@app.route('/profile/<id>')
def profilepage():
    return render_template("profile.html")

app.run(host="0.0.0.0")