from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for Render deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"
BASE_URL = "https://api.themoviedb.org/3"

def get_tmdb(path, params={}):
    params["api_key"] = TMDB_API_KEY
    return requests.get(f"{BASE_URL}{path}", params=params).json()

def format_item(m, m_type="movie"):
    return {
        "id": str(m.get("id")),
        "title": m.get("title") or m.get("name"),
        "poster": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}",
        "type": m_type
    }

@app.get("/api/home")
def get_home():
    # Trending
    trending = [format_item(m, m.get("media_type", "movie")) for m in get_tmdb("/trending/all/day")["results"][:12]]
    
    # K-Dramas (Korean language TV shows)
    k_drama = [format_item(m, "tv") for m in get_tmdb("/discover/tv", {"with_original_language": "ko", "sort_by": "popularity.desc"})["results"][:12]]
    
    # Action (Genre ID 28)
    action = [format_item(m, "movie") for m in get_tmdb("/discover/movie", {"with_genres": "28"})["results"][:12]]
    
    # Comedy (Genre ID 35)
    comedy = [format_item(m, "movie") for m in get_tmdb("/discover/movie", {"with_genres": "35"})["results"][:12]]

    return {
        "genres": [
            {"name": "Trending Now", "movies": trending},
            {"name": "Korean Dramas", "movies": k_drama},
            {"name": "Action Movies", "movies": action},
            {"name": "Comedy Hits", "movies": comedy}
        ]
    }

@app.get("/api/search")
def search(q: str):
    data = get_tmdb("/search/multi", {"query": q})
    results = []
    for m in data.get("results", []):
        if m.get("poster_path"):
            results.append(format_item(m, m.get("media_type", "movie")))
    return {"results": results}

@app.get("/api/movie")
def get_movie_details(id: str, type: str = "movie"):
    # If it's a TV show, we point to the first episode by default
    if type == "tv":
        url = f"https://vidsrc.icu/embed/tv/{id}/1/1"
    else:
        url = f"https://vidsrc.icu/embed/movie/{id}"
    return {"direct_url": url}
