from __main__ import *
@app.route("/api/series/search/<fraza>")
def search_api(fraza):
    response=list()
    # name, opis, image_url, rate, orginalurl, autorid, airing
    response = list()
    tytuly=session.query(Seria).filter(Seria.name.like("%{}%".format(fraza))).all()
    for i in tytuly:
        response.append({
            "title": i.name,
            "image_url": i.image_url,
            "id": i.id
            })
    return jsonify(response)

@app.route("/api/series/id/<id>")
def series_api(id):
    response=dict()
    epizodes=list()
    odcinki = session.query(Odcinek).filter(Odcinek.seriaid == id)
    seria=session.query(Seria).filter(Seria.id==id).first()
    for i in odcinki:
        epizodes.append(
            {
                "title":i.name,
                "cda_url":i.cda_url
            }
        )

    response={
        "metadata":{
            "title": seria.name,
            "description": seria.opis,
            "image_url": seria.image_url,
            "airing": seria.airing,
            "score": seria.rate,
            "added_by": seria.autorid
            },
        "epizodes": epizodes
        }
    return jsonify(response)
@app.route("/api/series")
def listallseries():
    response={}
    response["serie"]=list()
    limit=request.args.get('limit')
    offset=request.args.get('offset')
    if limit is None:
        limit=30
    if offset is None:
        offset=0
    ilosczmiennoprzecinkowa=len(session.query(Seria).all())/int(limit)
    iloscstron=int(ilosczmiennoprzecinkowa)
    if ilosczmiennoprzecinkowa > iloscstron: iloscstron+=1 
    tytuly=session.query(Seria).order_by(Seria.name).offset(offset).limit(limit)
    for i in tytuly:
        response["serie"].append({
            "title": i.name,
            "image_url": i.image_url,
            "id": i.id
        })
    response["pages"]=iloscstron
    return(jsonify(response))
@app.route('/api/series/lastadded')
def lastadded():
    response=list()
    limit=request.args.get('limit')
    serie=session.query(Seria).order_by(Seria.id.desc()).limit(limit)
    for i in serie:
        response.append({
            "title": i.name,
            "image_url": i.image_url,
            "id": i.id
        })
    return jsonify(response)
@app.route('/api/pinned')
def lastwached():
    response=list()
    userid=flasksession["user_id"]
    limit=request.args.get('limit')
    serie=session.query(Pinned).filter(Pinned.user==flasksession["user_id"]).limit(limit)
    print(serie)
    for i in serie:
        print("Seria  ",i.seria,"User  ",i.user)
        seria=session.query(Seria).filter(Seria.id==i.seria).first()
        print(seria)
        response.append({
            "title": seria.name,
            "image_url": seria.image_url,
            "id":seria.id
        })
    return(jsonify(response))

@app.route('/api/comments')
def commentsall():
    response=list()
    comments_list = session.query(Comment).filter_by(**request.args.to_dict()).all()
    for i in comments_list:
        # comments_var = session.query(Comment).filter(Comment.postid == i.postid).first()
        response.append({
            "comment_id": i.id,
            "author_id": i.autorid,
            "series_id": i.postid,
            "content": i.tresc
        })
    return(jsonify(response))
@app.route('/api/user/search/<arg>')
def usersearch(arg):
    response=list()
    user_list = session.query(Users).filter(Users.name.like("%{}%".format(arg))).all()
    for i in user_list:
        user_var = session.query(Users).filter(Users.name == i.name).first()    
        response.append({
            "username": user_var.name,
            "id": user_var.id
        })
    return(jsonify(response))

@app.route('/api/series/episode/id/<arg>')
def searchepisodebyid(arg):
    response=list()
    episode_list = session.query(Odcinek).filter(Odcinek.id == arg).all()
    for i in episode_list:
        episode_var = session.query(Odcinek).filter(Odcinek.name == i.name).first()
        response.append({
            "id": episode_var.id,
            "series_id": episode_var.seriaid,
            "name": episode_var.name,
            "cda_url": episode_var.cda_url
        })
    return(jsonify(response))