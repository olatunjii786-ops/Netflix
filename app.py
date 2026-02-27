import requests
from flask import Flask, jsonify, request
import os

app = Flask(__name__)
TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"
BASE_URL = "https://api.themoviedb.org/3"

def process_results(results):
    output = []
    for item in results:
        item_id = str(item.get('id'))
        title = item.get('title') if item.get('title') else item.get('name')
        media_type = "tv" if "name" in item else "movie"
        if item.get('poster_path'):
            output.append({
                "id": item_id,
                "title": title,
                "type": media_type,
                "poster": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}",
                "s1": f"https://vidsrc.to/embed/{media_type}/{item_id}",
                "s2": f"https://vidsrc.me/embed/{media_type}/{item_id}",
                "s3": f"https://v2.vidsrc.me/embed/{media_type}/{item_id}"
            })
    return output

@app.route('/movies')
def get_content():
    data = [
        {"genre": "Trending", "movies": process_results(requests.get(f"{BASE_URL}/trending/all/week?api_key={TMDB_API_KEY}").json().get('results', []))},
        {"genre": "Action", "movies": process_results(requests.get(f"{BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&with_genres=28").json().get('results', []))},
        {"genre": "TV Shows", "movies": process_results(requests.get(f"{BASE_URL}/discover/tv?api_key={TMDB_API_KEY}").json().get('results', []))},
        {"genre": "Asian", "movies": process_results(requests.get(f"{BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&with_original_language=ko|ja").json().get('results', []))},
        {"genre": "Chinese", "movies": process_results(requests.get(f"{BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&with_original_language=zh|cn").json().get('results', []))}
    ]
    return jsonify(data)

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query: return jsonify({"movies": [], "tv": []})
    res = requests.get(f"{BASE_URL}/search/multi?api_key={TMDB_API_KEY}&query={query}").json().get('results', [])
    return jsonify({
        "movies": process_results([r for r in res if r.get('media_type') == 'movie']),
        "tv": process_results([r for r in res if r.get('media_type') == 'tv'])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
