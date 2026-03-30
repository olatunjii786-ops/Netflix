from fastapi import FastAPI, Query
import requests
import random

app = FastAPI()
TMDB_KEY = "80434abc0b053ca70dfdf53b81f46059"
BASE_URL = "https://api.themoviedb.org/3"

GENRE_MAP = {
    "Actions": {"id": 28, "type": "movie"},
    "Comedy": {"id": 35, "type": "movie"},
    "Anime": {"id": 16, "type": "movie", "keyword": "210024"},
    "K-Dramas": {"id": 10759, "type": "tv", "lang": "ko"},
    "Nollywood": {"id": 18, "type": "movie", "region": "NG"}, # Drama + Nigeria
    "Bollywood": {"id": 18, "type": "movie", "region": "IN"}  # Drama + India
}

def get_tmdb_data(g_name, page=None):
    if not page: page = random.randint(1, 20)
    cfg = GENRE_MAP.get(g_name, {"id": 28, "type": "movie"})
    endpoint = f"{BASE_URL}/discover/{cfg['type']}"
    
    params = {
        "api_key": TMDB_KEY, "page": page,
        "sort_by": "popularity.desc", "include_adult": "false"
    }
    if cfg.get("id"): params["with_genres"] = cfg["id"]
    if cfg.get("lang"): params["with_original_language"] = cfg["lang"]
    if cfg.get("region"): params["region"] = cfg["region"]

    try:
        r = requests.get(endpoint, params=params).json()
        return [{
            "id": i["id"],
            "title": i.get("title") or i.get("name"),
            "poster": f"https://image.tmdb.org/t/p/w500{i['poster_path']}",
            "type": cfg["type"]
        } for i in r.get("results", []) if i.get("poster_path")]
    except: return []

@app.get("/api/home")
def home():
    return {"genres": [{"name": k, "movies": get_tmdb_data(k)[:10]} for k in GENRE_MAP.keys()]}

@app.get("/api/search")
def search(q: str):
    r = requests.get(f"{BASE_URL}/search/multi", params={"api_key": TMDB_KEY, "query": q}).json()
    return {"movies": [{
        "id": i["id"], "title": i.get("title") or i.get("name"),
        "poster": f"https://image.tmdb.org/t/p/w500{i['poster_path']}",
        "type": i.get("media_type", "movie")
    } for i in r.get("results", []) if i.get("poster_path")]}
