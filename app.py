from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

TMDB_API_KEY = "your_actual_tmdb_api_key_here"  # 🔑 Replace this

# Predefined genres you want to show
GENRE_MAP = {
    28: "action",
    12: "adventure",
    16: "animation",
    35: "comedy",
    80: "crime",
    99: "documentary",
    18: "drama",
    10751: "family",
    14: "fantasy",
    36: "history",
    27: "horror",
    10402: "music",
    9648: "mystery",
    10749: "romance",
    878: "sci-fi",
    10770: "tv-movie",
    53: "thriller",
    10752: "war",
    37: "western"
}

@app.route("/movies")
def get_movies():
    """
    Returns all popular movies (first N pages) with genre names.
    Optional query: ?genre=action
    """
    genre_filter = request.args.get("genre", None)
    movies = []

    try:
        # We'll fetch first 5 pages (~100 movies per page)
        for page in range(1, 6):
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={page}"
            response = requests.get(url)
            data = response.json()

            for item in data.get("results", []):
                movie_genres = [GENRE_MAP.get(gid, "other") for gid in item.get("genre_ids", [])]
                # Only take the first genre for simplicity
                genre_name = movie_genres[0] if movie_genres else "other"

                movie_obj = {
                    "id": item.get("id"),
                    "name": item.get("title"),
                    "overview": item.get("overview"),
                    "poster": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}",
                    "url": f"https://vidsrc.me/embed/movie/{item.get('id')}",  # Your embedded player URL
                    "genre": genre_name
                }

                # Optional genre filter
                if genre_filter is None or genre_filter.lower() == genre_name.lower():
                    movies.append(movie_obj)
    except Exception as e:
        print("Error fetching movies:", e)
        movies = []

    return jsonify(movies)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
