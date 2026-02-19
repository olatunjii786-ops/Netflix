import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

@app.route('/movies')
def get_popular():
    try:
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        movie_list = []

        for item in data.get('results', []):
            poster_path = item.get('poster_path')
            poster_url = (
                f"https://image.tmdb.org/t/p/w500{poster_path}"
                if poster_path else ""
            )

            movie_list.append({
                "id": item.get('id'),
                "name": item.get('title'),
                "overview": item.get('overview'),
                "poster": poster_url
            })

        return jsonify(movie_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)