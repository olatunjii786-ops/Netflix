from flask import Flask, jsonify
import requests

app = Flask(__name__)

CONSUMET_BASE = "https://apiconsumetorg-production-085d.up.railway.app"

# Categories mapping
CATEGORIES = ["trending", "popular", "top-rated", "latest"]
GENRES = ["action", "romance", "comedy", "horror", "scifi", "thriller"]

@app.route("/movies/<category>")
def movies(category):
    try:
        # Determine endpoint
        if category in GENRES:
            url = f"{CONSUMET_BASE}/genres/flixhq/{category}"
        elif category in CATEGORIES:
            url = f"{CONSUMET_BASE}/movies/flixhq/{category}"
        else:
            return jsonify([])

        resp = requests.get(url)
        data = resp.json()
        results = data.get("results", [])

        movies = []
        for m in results[:50]:  # send up to 50 items
            movies.append({
                "title": m.get("title"),
                "poster": m.get("image"),
                "url": m.get("url"),
                "type": m.get("type"),
                "releaseDate": m.get("releaseDate", "N/A")
            })

        return jsonify(movies)

    except Exception as e:
        print(e)
        return jsonify([])

@app.route("/stream/<title>")
def stream(title):
    try:
        url = f"{CONSUMET_BASE}/movies/flixhq/{title}"
        resp = requests.get(url)
        data = resp.json()
        # Make the response compatible with DetailsActivity
        sources = []
        for s in data.get("sources", []):
            sources.append({"url": s.get("url")})
        return jsonify({"sources": sources})
    except:
        return jsonify({"sources": []})

@app.route("/")
def home():
    return "🔥 Backend running for Netflix clone"
