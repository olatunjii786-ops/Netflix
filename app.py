from flask import Flask, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

TMDB_API_KEY = "YOUR_TMDB_API_KEY"  # Replace this with your key

# TMDb genres
tmdb_genres = {
    "action": 28, "thriller": 53, "comedy": 35, "horror": 27,
    "romance": 10749, "sci-fi": 878, "drama": 18, "animation": 16
}

# Sample playable URLs (MP4/HLS)
sample_videos = [
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4"
]

def fetch_movies_by_genre(genre_name, page=1):
    genre_id = tmdb_genres.get(genre_name.lower())
    if not genre_id:
        return []

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&page={page}"
    resp = requests.get(url)
    data = resp.json()
    movies = []

    for item in data.get("results", []):
        movies.append({
            "name": item.get("title"),
            "poster": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get('poster_path') else "",
            "url": random.choice(sample_videos),  # Replace with real stream if available
            "genre": genre_name
        })
    return movies

@app.route("/movies")
def get_movies():
    all_movies = []
    for genre in tmdb_genres.keys():
        all_movies += fetch_movies_by_genre(genre, page=1)
    return jsonify(all_movies)

@app.route("/")
def home():
    return "Netflix Clone Backend ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
