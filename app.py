import random
import requests
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from flask import jsonify # Note: In FastAPI we usually use JSONResponse or dicts

app = FastAPI()

# Enable CORS so your Android app can connect from any network
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"
BASE_URL = "https://api.themoviedb.org/3"

# Mapping names from Java "slugs" to TMDB Genre IDs
GENRE_MAP = {
    "trending-now": "trending",
    "korean-dramas": "ko",
    "action-movies": "28",
    "comedy-hits": "35",
    "horror-nights": "27"
}

# --- HELPERS ---

def get_tmdb(path, params=None):
    if params is None:
        params = {}
    params["api_key"] = TMDB_API_KEY
    try:
        response = requests.get(f"{BASE_URL}{path}", params=params, timeout=10)
        return response.json()
    except Exception as e:
        return {"results": []}

def format_item(m, m_type="movie"):
    """Formats TMDB raw data into the Watch-ify standard"""
    return {
        "id": str(m.get("id")),
        "title": m.get("title") or m.get("name"),
        "poster": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}",
        "type": m_type
    }

# --- ROUTES ---

@app.get("/api/home")
def get_home():
    """Returns 4 rows of 12 movies each, randomized every request"""
    
    # Pick 4 random pages between 1 and 15 to ensure the user never sees the same list twice
    p1, p2, p3, p4 = random.sample(range(1, 16), 4)

    # 1. Trending (Random Page)
    trending_raw = get_tmdb("/trending/all/week", {"page": p1})
    trending = [format_item(m, m.get("media_type", "movie")) for m in trending_raw.get("results", [])[:12]]

    # 2. K-Dramas (Random Page - Filtered by Language)
    kdrama_raw = get_tmdb("/discover/tv", {
        "with_original_language": "ko", 
        "sort_by": "popularity.desc", 
        "page": p2
    })
    k_drama = [format_item(m, "tv") for m in kdrama_raw.get("results", [])[:12]]

    # 3. Action (Random Page - Genre 28)
    action_raw = get_tmdb("/discover/movie", {"with_genres": "28", "page": p3})
    action = [format_item(m, "movie") for m in action_raw.get("results", [])[:12]]

    # 4. Comedy (Random Page - Genre 35)
    comedy_raw = get_tmdb("/discover/movie", {"with_genres": "35", "page": p4})
    comedy = [format_item(m, "movie") for m in comedy_raw.get("results", [])[:12]]

    return {
        "genres": [
            {"name": "Trending Now", "movies": trending},
            {"name": "Korean Dramas", "movies": k_drama},
            {"name": "Action Movies", "movies": action},
            {"name": "Comedy Hits", "movies": comedy}
        ]
    }

@app.get("/api/genre/{slug}")
def get_full_genre(slug: str):
    """Fetches 60+ movies for the 3-column infinite grid view"""
    results = []
    # Fetch 3 pages of data (20 movies per page = 60 total)
    # We randomize the starting page so the 'View More' is also fresh
    start_page = random.randint(1, 5)
    
    for page in range(start_page, start_page + 3):
        params = {"page": page}
        
        if slug == "korean-dramas":
            params.update({"with_original_language": "ko", "sort_by": "popularity.desc"})
            data = get_tmdb("/discover/tv", params)
            m_type = "tv"
        elif slug == "trending-now":
            data = get_tmdb("/trending/all/week", params)
            m_type = "movie"
        else:
            genre_id = GENRE_MAP.get(slug, "28")
            params.update({"with_genres": genre_id})
            data = get_tmdb("/discover/movie", params)
            m_type = "movie"

        for m in data.get("results", []):
            if m.get("poster_path"):
                results.append(format_item(m, m_type))

    # Shuffle the results locally for extra chaos
    random.shuffle(results)
    return {"movies": results}

@app.get("/api/search")
def search(q: str):
    """Standard search functionality"""
    data = get_tmdb("/search/multi", {"query": q})
    results = []
    for m in data.get("results", []):
        if m.get("poster_path"):
            results.append(format_item(m, m.get("media_type", "movie")))
    return {"results": results}

@app.get("/api/movie")
def get_movie_details(id: str, type: str = "movie"):
    """Points to the external embed player"""
    if type == "tv":
        url = f"https://vidsrc.icu/embed/tv/{id}/1/1"
    else:
        url = f"https://vidsrc.icu/embed/movie/{id}"
    return {"direct_url": url}

if __name__ == "__main__":
    import uvicorn
    # Use the PORT environment variable provided by Render
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
