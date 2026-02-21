import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "80434abc0b053ca70dfdf53b81f46059")

@app.route('/movies')
def get_movies():
    try:
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        cleaned_movies = []
        for item in data.get('results', []):
            cleaned_movies.append({
                "id": str(item.get('id')),
                "title": item.get('title'),
                "poster": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}",
                "play_url": f"https://vidsrc.to/embed/movie/{item.get('id')}"
            })
        return jsonify(cleaned_movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
