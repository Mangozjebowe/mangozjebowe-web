#Flask
from flask import render_template, Flask ,redirect, request, session as flasksession, url_for, abort, jsonify, flash
app = Flask(__name__)
app.secret_key = 'TajnYSecretKeyYYYY2137'
#Pierdoły
import requests
import youtube_dl
# from bs4 import BeautifulSoup
# from soupsieve.css_match import RE_DATE
# from datetime import timedelta

# komponenty
from db import *
from api import *
from scraper import *
#zmienne dotyczące logowania
logged_user = ""

@app.before_request
def make_session_permanent():
    flasksession.permanent = True 
@app.before_request
def logged():
	global logged_user
	try:
		logged_user = db.session.query(User).filter(User.id == flasksession["user_id"]).first()
	except:
		logged_user = None
@app.route("/login", methods=["GET", "POST"])
def login():
	try:
	    flasksession.pop("user_id")
	except:
	    None
	if request.method == "GET":
		return render_template('login.html')
	elif request.method == "POST":
		user = db.session.query(User).filter(User.name == request.form["nick"], User.password==request.form["password"]).first()
		if not user == None:
			flasksession['user_id'] = user.id
			return redirect('/')
		else:
			flash('Błędny login lub hasło')
			return(render_template("login.html"))

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if request.method == "GET":
		return render_template('register.html')
	else:
		user = User(name = request.form['nick'], password = request.form['password'])
		db.session.add(user)
		db.session.commit()
		return redirect('/login')
@app.route('/manage/users')
def manage_users():
	users = db.session.query(User).all()
	return(render_template('manageUsers.html', users = users))
@app.route('/manage/users/delete/<id>')
def remove(id):
	if logged_user.admin:
		user = db.session.query(User).filter(User.id == id).first()
		db.session.delete(user)
		db.session.commit()
		return jsonify({'succes': True})
	else:
		raise PermissionError("this user don't have permission to ban user")
		return jsonify({'succes': True})
@app.route('/logout')
def logout():
	try:
		flasksession.pop('user_id')
	except:
		None
	return redirect('/')
@app.route('/')
def index():
	pinned_animes = []
	if request.args.get('q') == None:
		search = False
		last_added = db.session.query(Anime).order_by(Anime.id.desc()).limit(6)
		animes = db.session.query(Anime).order_by(Anime.title).all()
	else:
		search = True
		last_added = []
		animes = db.session.query(Anime).filter(Anime.title.like("%{}%".format(request.args.get('q')))).order_by(Anime.title).all()
	if logged_user == None:
		logged = False
		pinned = None
	else:
		for i in reversed(logged_user.pinned):
			if len(pinned_animes)==6:
				break
			pinned_animes.append(db.session.query(Anime).filter(Anime.id == i.anime).order_by(Anime.id.desc()).first())
		logged = True

	return render_template('index.html',
	 animes=animes,
	  user=logged_user,
	   logged=logged,
	    last_added = last_added,
	     pinned = pinned_animes,
	      search = search)
@app.route('/anime/<id>')
def anime(id):
	if logged_user == None:
		logged = False
	else:
		logged = True

	anime = db.session.query(Anime).filter(Anime.id==id).first()
	try:
		anime.pinned[0].id
		pinned = True
	except:
		pinned = False
	adders = []
	for i in anime.comments:
		adders.append(db.session.query(User).filter(User.id == i.autor).first())

	return render_template('anime.html',anime=anime, pinned = pinned, logged=logged, user = logged_user, adders = adders, len = len(anime.comments))
@app.route('/episode/<id>')
def episode(id):
	episode = db.session.query(Episode).filter(Episode.id == id).first()
	anime = db.session.query(Anime).filter(Anime.id == episode.anime).first()
	episode.url = episode.url.replace('www.cda.pl/video/', 'ebd.cda.pl/620x395/')
	print(anime.episodes)
	return render_template('episode.html', episode=episode, anime=anime)
@app.route('/pin/<id>')
def pin(id):
	try:
		anime = db.session.query(Anime).filter(Anime.id == id).first()
		db.session.add(Pinned(anime = anime.id, user = logged_user.id))
		db.session.commit()
		return jsonify({'succes': True})
	except:
		return jsonify({'succes': False})
@app.route('/delete/<id>')
def delete(id):
		if logged_user.admin:
			anime = db.session.query(Anime).filter(Anime.id == id).first()
			pinned = db.session.query(Pinned).filter(Pinned.anime == id)
			pinned.delete()
			db.session.delete(anime)
			db.session.commit()
			return jsonify({'succes': True})
		else:
			raise PermissionError("this user don't have permission to delete")
			return jsonify({'succes': False}), 403
@app.route('/unpin/<id>')
def unpin(id):
	# try:
		pinned = db.session.query(Pinned).filter(Pinned.anime == id).first()
		db.session.delete(pinned)
		db.session.commit()
		return jsonify({'succes': True})
	# except:
		# return jsonify({'succes': False})
@app.route('/pinned')
def pinned():
	pinned_animes = []
	for i in logged_user.pinned:
		pinned_animes.append(db.session.query(Anime).filter(Anime.id == i.anime).first())
	return render_template('pinned.html', pinned = pinned_animes)
@app.route('/addcomment/<id>', methods=['POST'])
def add_comment(id):
	text = request.form['text']
	comment = Comment(
		text = text,
		autor = logged_user.id,
		anime = id,
	)
	db.session.add(comment)
	db.session.commit()
	return('succes')
	# try:
	# 	if not logged_user is None:
	# 		db.session.add(Comment(
	# 			text = text,
	# 			autor = logged_user,
	# 			anime = db.session.query(Anime).filter(Anime.id == id).first(),
	# 		))
	# 		db.session.commit()
	# 	else:
	# 		return jsonify({ 'succes': False, 'error': 'Użytkownik nie jest zalogowany' })
	# except:
	# 	return jsonify({ 'succes': False, 'error': 'Nie znany błąd' })
@app.route('/add', methods=['POST', 'GET'])
def add():
	if request.method == 'GET':
		return render_template('add.html')
	else:
		if logged_user.admin:
			link = request.form["link"]
			title = request.form["title"]
			anime = scrap(link=link, title=title)
			odcinki = []
			for i in anime['Episodes']:
				episode = Episode(url = i['player'], title=i['title'])
				db.session.add(episode)
				odcinki.append(episode)
			animeToDB = Anime(
				title = anime['Metadata']['title'],
				mal_id = anime['Metadata']['mal_id'],
				image_url = anime['Metadata']['image_url'],
				sources = json.dumps(anime['Metadata']['sources']),
				type = anime['Metadata']['type'],
				planned_episodes = anime['Metadata']['episodes'],
				score = anime['Metadata']['score'],
				rated = anime['Metadata']['rated'],
				synonyms = json.dumps(anime['Metadata']['synonyms']),
				airing = bool(anime['Metadata']['airing']),
				synopsis = anime['Metadata']['synopsis'],
				added_by = logged_user.id,
				orginal_url = link
				)
			animeToDB.episodes = odcinki
			db.session.add(animeToDB)
			db.session.commit()
			return redirect('/')

app.run(host="0.0.0.0")






