from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import tmdbv3api
import random

app = FastAPI()
tmdb = tmdbv3api.TMDb()
tmdb.api_key = 'YOUR_TMDB_API_KEY' # Replace with your actual key
movie_api = tmdbv3api.Movie()
tv_api = tmdbv3api.TV()

# Mapping Java slugs to TMDB Genre IDs
GENRE_MAP = {
    "trending": "trending",
    "korean-dramas": "ko", # We use 'ko' as a flag for the logic below
    "action-movies": "28",
    "horror-movies": "27",
    "comedy-hits": "35",
    "romance": "10749"
}

@app.get("/api/home")
def get_home():
    genres = []
    # Generate 5 random rows for the home screen
    for name, g_id in GENRE_MAP.items():
        if g_id == "ko":
            results = tv_api.popular(language="ko")[:10]
            m_type = "tv"
        else:
            results = movie_api.popular()[:10] if g_id == "trending" else movie_api.genre(g_id)[:10]
            m_type = "movie"
            
        movies = [{"id": m.id, "title": getattr(m, 'title', getattr(m, 'name', '')), 
                   "poster": f"https://image.tmdb.org/t/p/w500{m.poster_path}", "type": m_type} 
                  for m in results if hasattr(m, 'poster_path') and m.poster_path]
        genres.append({"name": name.replace("-", " ").upper(), "movies": movies})
    return {"genres": genres}

@app.get("/api/genre/{slug}")
def get_genre_infinite(slug: str):
    g_id = GENRE_MAP.get(slug, "28")
    all_movies = []
    # Fetch 3 pages to provide "as much as possible" (60 items)
    for page in range(1, 4):
        if g_id == "ko":
            data = tv_api.popular(page=page, language="ko")
            m_type = "tv"
        else:
            data = movie_api.genre(g_id, page=page)
            m_type = "movie"
        
        for m in data:
            if hasattr(m, 'poster_path') and m.poster_path:
                all_movies.append({
                    "id": m.id, "title": getattr(m, 'title', getattr(m, 'name', 'Unknown')),
                    "poster": f"https://image.tmdb.org/t/p/w500{m.poster_path}", "type": m_type
                })
    return {"movies": all_movies}
