from __main__ import *
@app.route('/api/series')
def series():
    return_series = list()
    args = request.args.to_dict()
    try:
        args.pop('limit')
        limit=request.args.get('limit')
    except:
        limit=200000
    series = db.session.query(Anime).filter_by(**args).limit(limit)
    for i in series:
        return_series.append({
            'title': i.title,
            "id": i.id,
            'image_url': i.image_url,
            'airing': i.airing,
            'planned_episodes': i.planned_episodes,
            'score': i.score,
            'synonyms': i.synonyms,
            'tags': []
        })
        try:
            [ return_series[len(return_series)-1]['tags'].append(j.tag) for j in i.tags ]
        except:
            return_series[len(return_series)-1]['tags'] = []
    return(jsonify(return_series))
@app.route("/api/series/id/<id>")
def series_api(id):
    anime = db.session.query(Anime).filter(Anime.id==id).first()
    episodes = []
    comments = []
    for i in anime.episodes:
        episodes.append({
            'id': i.id,
            'url': i.url,
            'title': i.title,
            })
    for i in anime.comments:
        autor = db.session.query(User).filter(User.id==i.id).first()
        comments.append({
            'autor': autor.name,
            'autorID': autor.id,
            'add_date': i.add_date,
            'text': i.text,
            })
    if anime is None:
        return {}
    else:
        response = {
            "mal_id": anime.mal_id,
            "image_url": anime.image_url,
            "airing": bool(anime.airing),
            "type": anime.type,
            "score": anime.score,
            "add_date": anime.add_date,
            "synonyms": anime.synonyms,
            "orginal_url": anime.orginal_url,
            "id": anime.id,
            "sources": anime.sources,
            "title": anime.title,
            "synopsis": anime.synopsis,
            "planned_episodes": anime.planned_episodes,
            "added_by": db.session.query(User).filter(anime.added_by==User.id).first().name,
            "rated": anime.rated,
            "tags": [],
            'episodes': episodes,
            'comments': comments,
        }
        for i in anime.tags:
            response['tags'].append(i.tag)
        return(jsonify(response))
@app.route('/api/tags/autocomplete')
def autocomplete():
    search = request.args.get('q')
    limit = request.args.get('limit')
    if limit is None:
        limit = 100000
    tags = db.session.query(Tag).filter(Tag.tag.like("%{}%".format(search))).order_by(Tag.id).limit(limit)
    return_tags = []
    for i in tags:
        if not i.anime is None:
            return_tags.append({
                "text": i.tag,
                "id": i.id,
            })
    return jsonify(return_tags)