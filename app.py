from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

def fetch_tmdb(endpoint, params={}):
    params['api_key'] = TMDB_API_KEY
    params['language'] = 'en-US'
    url = f"https://api.themoviedb.org/3{endpoint}"
    response = requests.get(url, params=params)
    return response.json()

def format_movie(movie):
    return {
        'id': movie['id'],
        'title': movie['title'],
        'poster': TMDB_IMAGE_BASE + movie['poster_path'] if movie.get('poster_path') else None,
        'year': movie['release_date'][:4] if movie.get('release_date') else None,
        'rating': round(movie['vote_average'], 1) if movie.get('vote_average') else 0,
        'overview': movie.get('overview', '')
    }

@app.route('/api/home')
def home():
    genre_ids = [28, 35, 18, 27, 10749, 878, 53, 16, 99, 9648]
    genre_names = {
        28: 'Action', 35: 'Comedy', 18: 'Drama', 27: 'Horror',
        10749: 'Romance', 878: 'Sci-Fi', 53: 'Thriller', 16: 'Animation',
        99: 'Documentary', 9648: 'Mystery'
    }
    
    result = {'status': 'success', 'genres': []}
    
    for genre_id in genre_ids:
        data = fetch_tmdb('/discover/movie', {
            'with_genres': genre_id,
            'sort_by': 'popularity.desc',
            'page': 1
        })
        
        movies = []
        for movie in data.get('results', [])[:10]:
            movies.append(format_movie(movie))
        
        result['genres'].append({
            'id': genre_id,
            'name': genre_names[genre_id],
            'movies': movies
        })
    
    return jsonify(result)

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'status': 'error', 'message': 'Query required'})
    
    data = fetch_tmdb('/search/movie', {'query': query})
    
    results = []
    for movie in data.get('results', []):
        results.append(format_movie(movie))
    
    return jsonify({
        'status': 'success',
        'query': query,
        'results': results
    })

@app.route('/api/movie')
def movie():
    movie_id = request.args.get('id', '')
    if not movie_id:
        return jsonify({'status': 'error', 'message': 'Movie ID required'})
    
    data = fetch_tmdb(f'/movie/{movie_id}', {'append_to_response': 'videos'})
    
    # Get watch sources (VidSrc URLs)
    watch_sources = [
        {'name': 'VidSrc', 'url': f'https://vidsrc.to/embed/movie/{movie_id}'},
        {'name': 'VidSrc 2', 'url': f'https://vidsrc.in/embed/movie/{movie_id}'},
        {'name': 'Smashy', 'url': f'https://player.smashy.stream/movie/{movie_id}'}
    ]
    
    return jsonify({
        'status': 'success',
        'data': {
            'id': data['id'],
            'title': data['title'],
            'overview': data.get('overview', ''),
            'poster': TMDB_IMAGE_BASE + data['poster_path'] if data.get('poster_path') else None,
            'year': data['release_date'][:4] if data.get('release_date') else None,
            'rating': round(data['vote_average'], 1) if data.get('vote_average') else 0,
            'watch_sources': watch_sources
        }
    })

@app.route('/')
def index():
    return jsonify({'message': 'Netflix Movie API is running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
