import requests
from flask import Flask, jsonify

app = Flask(__name__)
# Replace with your TMDB API Key from themoviedb.org
TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"
BASE_URL = "https://api.themoviedb.org/3"

# Mapping Genres to TMDB IDs
GENRES = {
    "Trending": "trending/movie/week",
    "Action": "28",
    "Drama": "18",
    "TV Shows": "10763", # News/TV
    "Asian": "10749",    # Romance often covers Asian content
    "Chinese": "10749"   # You can adjust IDs as needed
}

def fetch_movies(genre_key):
    try:
        if genre_key == "Trending":
            url = f"{BASE_URL}/{GENRES[genre_key]}?api_key={TMDB_API_KEY}"
        else:
            url = f"{BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&with_genres={GENRES[genre_key]}"
        
        response = requests.get(url).json()
        movies = []
        for m in response.get('results', []):
            # Using TMDB ID for the video link
            movie_id = str(m.get('id', ''))
            movies.append({
                "title": m.get('title', 'Unknown'),
                "poster": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}",
                "s1": f"https://vidsrc.to/embed/movie/{movie_id}",
                "s2": f"https://vidsrc.me/embed/movie/{movie_id}",
                "s3": f"https://v2.vidsrc.me/embed/movie/{movie_id}"
            })
        return movies
    except:
        return []

@app.route('/movies')
def get_movies():
    data = []
    for g in GENRES.keys():
        data.append({"genre": g, "movies": fetch_movies(g)})
    return jsonify(data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
