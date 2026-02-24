import requests
from flask import Flask, jsonify
import os

app = Flask(__name__)
TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_data(path, params={}):
    default_params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    default_params.update(params)
    try:
        response = requests.get(f"{BASE_URL}/{path}", params=default_params).json()
        results = response.get('results', [])
        
        output = []
        for item in results:
            item_id = str(item.get('id'))
            # TV shows use 'name', Movies use 'title'
            title = item.get('title') if item.get('title') else item.get('name')
            
            # Determine if it's a movie or tv show for the embed link
            media_type = "tv" if "name" in item else "movie"
            
            output.append({
                "title": title,
                "poster": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}",
                "s1": f"https://vidsrc.to/embed/{media_type}/{item_id}",
                "s2": f"https://vidsrc.me/embed/{media_type}/{item_id}",
                "s3": f"https://v2.vidsrc.me/embed/{media_type}/{item_id}"
            })
        return output
    except:
        return []

@app.route('/movies')
def get_content():
    data = [
        {"genre": "Trending", "movies": fetch_data("trending/all/week")},
        {"genre": "Action", "movies": fetch_data("discover/movie", {"with_genres": "28"})},
        {"genre": "TV Shows", "movies": fetch_data("discover/tv", {"with_genres": "18"})}, # Drama TV
        {"genre": "Chinese", "movies": fetch_data("discover/movie", {"with_original_language": "zh"})},
        {"genre": "Asian (Korean)", "movies": fetch_data("discover/movie", {"with_original_language": "ko"})}
    ]
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
