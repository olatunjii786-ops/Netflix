from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow your Android app to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = "80434abc0b053ca70dfdf53b81f46059"
BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_tmdb(endpoint, params={}):
    params['api_key'] = TMDB_API_KEY
    url = f"https://api.themoviedb.org/3{endpoint}"
    return requests.get(url, params=params).json()

@app.get("/api/home")
def get_home():
    # Fetching Trending movies for the Netflix Home Screen
    data = fetch_tmdb("/trending/movie/day")
    movies = []
    for m in data.get('results', [])[:20]:
        movies.append({
            "id": str(m.get('id')),
            "title": m.get('title'),
            "poster": f"{BASE_IMAGE_URL}{m.get('poster_path')}"
        })
    return {"movies": movies}

@app.get("/api/movie")
def get_movie_details(id: str):
    # This is our active, ad-slayer source
    # We send the embed link which the Java WebView will clean up
    stream_url = f"https://vidsrc.icu/embed/movie/{id}"
    return {
        "id": id,
        "direct_url": stream_url
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
