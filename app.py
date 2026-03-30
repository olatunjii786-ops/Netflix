from fastapi import FastAPI
import tmdbv3api
import os

app = FastAPI()
tmdb = tmdbv3api.TMDb()
tmdb.api_key = '80434abc0b053ca70dfdf53b81f46059' # Ensure no spaces around the key
tmdb.language = 'en-US'

movie_api = tmdbv3api.Movie()
tv_api = tmdbv3api.TV()
discover = tmdbv3api.Discover() # Added for better K-Drama fetching

@app.get("/api/home")
def get_home():
    genres = []
    # Use Discovery for Korean Dramas to ensure we get results
    sections = [
        ("TRENDING", movie_api.popular()),
        ("KOREAN DRAMAS", discover.discover_tv_shows({'with_original_language': 'ko', 'sort_by': 'popularity.desc'})),
        ("ACTION", movie_api.genre(28)),
        ("HORROR", movie_api.genre(27))
    ]

    for name, data in sections:
        movies = []
        for m in data[:15]: # Get top 15
            path = getattr(m, 'poster_path', None)
            if path:
                movies.append({
                    "id": m.id,
                    "title": getattr(m, 'title', getattr(m, 'name', 'Unknown')),
                    "poster": f"https://image.tmdb.org/t/p/w500{path}",
                    "type": "tv" if "original_name" in dir(m) or "name" in dir(m) else "movie"
                })
        if movies:
            genres.append({"name": name, "movies": movies})
            
    return {"genres": genres}
