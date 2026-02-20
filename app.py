from flask import Flask, jsonify
import requests

app = Flask(__name__)

TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"
CONSUMET_BASE = "https://apiconsumetorg-production-085d.up.railway.app"

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# 🎬 Genre Mapping
GENRE_MAP = {
    "action": 28,
    "romance": 10749,
    "comedy": 35,
    "horror": 27,
    "scifi": 878,
    "thriller": 53
}

# 🔥 Main Categories Mapping
CATEGORY_ENDPOINTS = {
    "trending": "trending/movie/week",
    "popular": "movie/popular",
    "top-rated": "movie/top_rated",
    "latest": "movie/now_playing"
}


@app.route("/movies/<category>")
def get_movies(category):

    # ✅ Genre Section
    if category in GENRE_MAP:
        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": GENRE_MAP[category],
            "sort_by": "popularity.desc"
        }

    # ✅ Main Sections
    elif category in CATEGORY_ENDPOINTS:
        url = f"https://api.themoviedb.org/3/{CATEGORY_ENDPOINTS[category]}"
        params = {"api_key": TMDB_API_KEY}

    else:
        return jsonify({"error": "Invalid category"}), 400

    response = requests.get(url, params=params)
    data = response.json()
    results = data.get("results", [])

    movies = []

    for movie in results[:20]:
        poster_path = movie.get("poster_path")
        poster_url = TMDB_IMAGE_BASE + poster_path if poster_path else ""

        movies.append({
            "title": movie.get("title"),
            "poster": poster_url,
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average")
        })

    return jsonify(movies)


# ▶ STREAM FROM CONSUMET
@app.route("/stream/<title>")
def stream_movie(title):

    try:
        search_url = f"{CONSUMET_BASE}/movies/flixhq/{title}"
        response = requests.get(search_url)
        data = response.json()

        return jsonify(data)

    except:
        return jsonify({"error": "Stream not found"}), 404


@app.route("/")
def home():
    return "🔥 Netflix-Style Backend Running"
