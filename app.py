from fastapi import FastAPI, Query
import tmdbv3api
import random

app = FastAPI()

# --- TMDB SETUP ---
tmdb = tmdbv3api.TMDb()
tmdb.api_key = '80434abc0b053ca70dfdf53b81f46059'  # <-- USE YOUR REAL KEY HERE
movie_api = tmdbv3api.Movie()
tv_api = tmdbv3api.TV()
search_api = tmdbv3api.Search()

# Map Java slugs to TMDB Genre IDs
GENRE_MAP = {
    "trending": "trending",
    "korean-dramas": "ko",
    "action-movies": "28",
    "horror-movies": "27",
    "comedy-hits": "35",
    "romance": "10749"
}

def format_item(m, m_type):
    poster_path = getattr(m, 'poster_path', None)
    return {
        "id": m.id,
        "title": getattr(m, 'title', getattr(m, 'name', 'Unknown')),
        "poster": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster",
        "type": m_type
    }

@app.get("/api/home")
def get_home():
    genres = []
    for slug, g_id in GENRE_MAP.items():
        if g_id == "ko":
            # Fetch popular Korean TV shows (K-Dramas)
            results = tv_api.popular(language="ko")[:12]
            m_type = "tv"
        elif g_id == "trending":
            results = movie_api.popular()[:12]
            m_type = "movie"
        else:
            results = movie_api.genre(g_id)[:12]
            m_type = "movie"
            
        movies = [format_item(m, m_type) for m in results if hasattr(m, 'id')]
        genres.append({"name": slug.replace("-", " ").upper(), "movies": movies})
    return {"genres": genres}

@app.get("/api/genre/{slug}")
def get_genre_infinite(slug: str):
    g_id = GENRE_MAP.get(slug, "28")
    all_movies = []
    # Fetch 3 pages to fill the 3-column grid (approx 60 items)
    for page in range(1, 4):
        if g_id == "ko":
            data = tv_api.popular(page=page, language="ko")
            m_type = "tv"
        else:
            data = movie_api.genre(g_id, page=page)
            m_type = "movie"
        
        for m in data:
            all_movies.append(format_item(m, m_type))
    return {"movies": all_movies}

@app.get("/api/search")
def search_content(q: str = Query(...)):
    # Search both movies and TV shows
    movie_res = search_api.movies({"query": q})
    tv_res = search_api.tv({"query": q})
    
    results = []
    for m in movie_res: results.append(format_item(m, "movie"))
    for t in tv_res: results.append(format_item(t, "tv"))
    
    return {"movies": results}
