from flask import Flask, jsonify
import requests

app = Flask(__name__)
TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"

# TMDB Genre IDs
GENRES = {
    "Trending": "trending",
    "Action": "28",
    "Comedy": "35",
    "Horror": "27",
    "Sci-Fi": "878",
    "Animation": "16",
    "Romance": "10749",
    "Documentary": "99"
}

@app.route('/movies')
def get_movies():
    structured_data = []
    for name, g_id in GENRES.items():
        if g_id == "trending":
            url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
        else:
            url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={g_id}"
        
        # Get 15 movies per genre to allow for "View More" exploration
        res = requests.get(url).json().get('results', [])[:15] 
        
        genre_movies = []
        for m in res:
            m_id = str(m.get('id'))
            genre_movies.append({
                "title": m.get('title'),
                "poster": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}",
                "s1": f"https://vidsrc.to/embed/movie/{m_id}",
                "s2": f"https://vidsrc.me/embed/movie/{m_id}",
                "s3": f"https://www.2embed.cc/embed/{m_id}"
            })
        structured_data.append({"genre": name, "movies": genre_movies})
        
    return jsonify(structured_data)
