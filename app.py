from flask import Flask, jsonify
import requests

app = Flask(__name__)

CONSUMET_BASE = "https://apiconsumetorg-production-085d.up.railway.app"

# -------- MOVIES BY CATEGORY --------
@app.route("/movies/<category>")
def get_movies(category):
    try:
        url = f"{CONSUMET_BASE}/movies/flixhq/{category}"
        response = requests.get(url)
        data = response.json()

        results = data.get("results", [])

        formatted = []

        for movie in results:
            formatted.append({
                "title": movie.get("title"),
                "poster": movie.get("image"),   # rename image → poster
                "url": movie.get("id")          # VERY IMPORTANT
            })

        return jsonify(formatted)  # RETURN PURE ARRAY

    except Exception as e:
        print(e)
        return jsonify([])


# -------- STREAM ENDPOINT --------
@app.route("/stream/<movie_id>")
def stream(movie_id):
    try:
        url = f"{CONSUMET_BASE}/movies/flixhq/info?id={movie_id}"
        response = requests.get(url)
        data = response.json()

        sources = data.get("sources", [])

        return jsonify({
            "sources": sources
        })

    except Exception as e:
        print(e)
        return jsonify({"sources": []})


@app.route("/")
def home():
    return "🔥 Netflix Backend Running"
