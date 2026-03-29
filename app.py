from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059" 
BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_from_tmdb(endpoint, params={}):
    params['api_key'] = TMDB_API_KEY
    url = f"https://api.themoviedb.org/3{endpoint}"
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception:
        return {"error": "TMDB Down"}

@app.get("/api/home")
def get_home():
    categories = [
        {"id": "28", "name": "Action Hits"},
        {"id": "27", "name": "Horror Night"},
        {"id": "878", "name": "Sci-Fi Universe"}
    ]
    home_structure = {"genres": []}
    for cat in categories:
        data = fetch_from_tmdb("/discover/movie", {"with_genres": cat["id"], "sort_by": "popularity.desc"})
        movies_list = []
        for movie in data.get('results', [])[:10]:
            movies_list.append({
                "id": str(movie.get('id')),
                "title": movie.get('title'),
                "poster": f"{BASE_IMAGE_URL}{movie.get('poster_path')}"
            })
        home_structure["genres"].append({"name": cat["name"], "movies": movies_list})
    return home_structure

@app.get("/api/movie")
def get_movie_details(id: str):
    # SMASHYSTREAM: Best alternative for ad-free native playback
    stream_url = f"https://player.smashy.stream/movie/{id}"
    return {
        "id": id,
        "direct_url": stream_url,
        "watch_sources": [{"name": "Premium High-Speed", "url": stream_url}]
    }

@app.get("/api/search")
def search_movie(q: str):
    data = fetch_from_tmdb("/search/movie", {"query": q})
    results = []
    for item in data.get('results', [])[:15]:
        results.append({
            "id": str(item.get('id')),
            "title": item.get('title'),
            "poster": f"{BASE_IMAGE_URL}{item.get('poster_path')}"
        })
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
