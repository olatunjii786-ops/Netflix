from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Allow requests from your Android app

# Predefined genres
genres = ["action", "thriller", "comedy", "horror", "romance", "sci-fi", "drama", "animation"]

# Predefined movie names (example)
movie_names = [
    "Avatar", "John Wick", "Inception", "The Matrix", "Avengers", "Joker",
    "Interstellar", "Frozen", "Titanic", "The Dark Knight", "Toy Story", "Parasite",
    "Guardians of the Galaxy", "Deadpool", "Shrek", "Iron Man", "Spider-Man", "Doctor Strange"
]

# Generate thousands of movies dynamically
movies = []

for i in range(1000):
    name = random.choice(movie_names) + f" {i+1}"
    genre = random.choice(genres)
    poster = f"https://picsum.photos/200/300?random={i+1}"  # random placeholder poster
    url = f"https://vidsrc.me/embed/movie/{i+1}"  # placeholder watch URL
    movies.append({
        "name": name,
        "poster": poster,
        "url": url,
        "genre": genre
    })

@app.route('/movies')
def get_movies():
    return jsonify(movies)

@app.route('/')
def home():
    return "Netflix Clone Backend ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
