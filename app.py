from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"  # ⚠️ Replace this

GENRE_MAP = {
    28: "action",
    12: "adventure",
    16: "animation",
    35: "comedy",
    80: "crime",
    99: "documentary",
    18: "drama",
    27: "horror",
    10749: "romance",
    878: "sci-fi",
    53: "thriller"
}

@app.route("/movies")
def get_movies():
    movies = []
    try:
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for item in data.get("results", []):
            genre_ids = item.get("genre_ids", [])
            genre_name = GENRE_MAP.get(genre_ids[0], "other") if genre_ids else "other"
            movies.append({
                "id": item.get("id"),
                "name": item.get("title"),
                "poster": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}",
                "url": f"https://vidsrc.me/embed/movie/{item.get('id')}",
                "genre": genre_name
            })
    except Exception as e:
        print("Error fetching movies:", e)
        # Fallback
        movies = [
            {
                "id": 1,
                "name": "Avatar",
                "poster": "https://image.tmdb.org/t/p/w500/kuf6evRbcS3SKEA3oVvznZ10yak.jpg",
                "url": "",
                "genre": "action"
            }
        ]
    return jsonify(movies)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
