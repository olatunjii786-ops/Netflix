from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"  # Replace with your TMDb API key

@app.route("/movies")
def get_movies():
    # Get genres from TMDb
    genres_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    genres_data = requests.get(genres_url).json()
    genre_map = {g['id']: g['name'] for g in genres_data.get('genres', [])}

    movie_list = []

    # Fetch multiple pages of popular movies
    for page in range(1, 6):  # Fetch first 5 pages (~100 movies)
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page={page}"
        data = requests.get(url).json()
        for m in data.get("results", []):
            genre_ids = m.get("genre_ids", [])
            for gid in genre_ids:
                # Construct a "playable" URL
                movie_list.append({
                    "name": m.get("title"),
                    "poster": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}",
                    "url": f"https://vidsrc.me/embed/movie/{m.get('id')}",  # placeholder for in-app play
                    "genre": genre_map.get(gid, "Other")
                })

    return jsonify(movie_list)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
