from fastapi import FastAPI, Query
import requests
import random

app = FastAPI()
TMDB_KEY = "80434abc0b053ca70dfdf53b81f46059"
BASE_URL = "https://api.themoviedb.org/3"

# Mapping for your specific categories
GENRE_MAP = {
    "Actions": {"id": 28, "type": "movie"},
    "Comedy": {"id": 35, "type": "movie"},
    "Anime": {"id": 16, "type": "movie", "keyword": "210024|287501"},
    "K-Dramas": {"id": 10759, "type": "tv", "lang": "ko"},
    "Nollywood": {"id": 0, "type": "movie", "region": "NG"},
    "Bollywood": {"id": 0, "type": "movie", "region": "IN"}
}

def get_tmdb_data(g_name, page=None):
    if not page:
        page = random.randint(1, 10) # Rotates content on every refresh
    
    cfg = GENRE_MAP.get(g_name, {"id": 28, "type": "movie"})
    endpoint = f"{BASE_URL}/discover/{cfg['type']}"
    
    params = {
        "api_key": TMDB_KEY,
        "page": page,
        "sort_by": "popularity.desc",
        "include_adult": "false"
    }
    
    if cfg.get("id"): params["with_genres"] = cfg["id"]
    if cfg.get("lang"): params["with_original_language"] = cfg["lang"]
    if cfg.get("region"): params["region"] = cfg["region"]
    if cfg.get("keyword"): params["with_keywords"] = cfg["keyword"]

    try:
        r = requests.get(endpoint, params=params).json()
        results = []
        for item in r.get("results", []):
            if item.get("poster_path"):
                results.append({
                    "id": item["id"],
                    "title": item.get("title") or item.get("name"),
                    "poster": f"https://image.tmdb.org/t/p/w500{item['poster_path']}",
                    "type": cfg["type"]
                })
        return results
    except:
        return []

@app.get("/api/home")
def home():
    data = []
    for g in GENRE_MAP.keys():
        data.append({"name": g, "movies": get_tmdb_data(g)[:10]})
    return {"genres": data}

@app.get("/api/view-more")
def view_more(genre: str, page: int = 1):
    return {"movies": get_tmdb_data(genre, page)}

@app.get("/api/search")
def search(q: str):
    r = requests.get(f"{BASE_URL}/search/multi", params={"api_key": TMDB_KEY, "query": q}).json()
    results = []
    for item in r.get("results", []):
        if item.get("poster_path"):
            results.append({
                "id": item["id"],
                "title": item.get("title") or item.get("name"),
                "poster": f"https://image.tmdb.org/t/p/w500{item['poster_path']}",
                "type": item.get("media_type", "movie")
            })
    return {"movies": results}
