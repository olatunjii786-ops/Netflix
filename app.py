from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS so your Android app can connect without issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURATION ---
# Put your TMDB API Key here directly
TMDB_API_KEY = "YOUR_TMDB_API_KEY_HERE" 
BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_from_tmdb(endpoint, params={}):
    params['api_key'] = TMDB_API_KEY
    url = f"https://api.themoviedb.org/3{endpoint}"
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/home")
def get_home():
    # Blueprint: 10 movies per genre
    # Genres: 28 (Action), 27 (Horror), 10749 (Romance), 878 (Sci-Fi)
    categories = [
        {"id": "28", "name": "Action Hits"},
        {"id": "27", "name": "Horror Night"},
        {"id": "878", "name": "Sci-Fi Universe"}
    ]
    
    home_structure = {"genres": []}
    
    for cat in categories:
        data = fetch_from_tmdb("/discover/movie", {
            "with_genres": cat["id"],
            "sort_by": "popularity.desc"
        })
        
        movies_list = []
        # Get exactly 10 movies for each row
        results = data.get('results', [])[:10]
        
        for movie in results:
            movies_list.append({
                "id": str(movie.get('id')),
                "title": movie.get('title'),
                "poster": f"{BASE_IMAGE_URL}{movie.get('poster_path')}",
                "overview": movie.get('overview'),
                "year": movie.get('release_date', '0000')[:4]
            })
            
        home_structure["genres"].append({
            "name": cat["name"],
            "movies": movies_list
        })
        
    return home_structure

@app.get("/api/movie")
def get_movie_details(id: str):
    # This provides the high-quality stream links
    return {
        "watch_sources": [
            {"name": "Server 1", "url": f"https://vidsrc.to/embed/movie/{id}"},
            {"name": "Server 2", "url": f"https://vidsrc.me/embed/movie/{id}"}
        ]
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
