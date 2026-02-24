from flask import Flask, jsonify

app = Flask(__name__)

# This is your database. Add as many movies as you want inside the 'movies' lists.
movie_data = [
    {
        "genre": "Trending",
        "movies": [
            {
                "title": "Example Trending",
                "poster": "https://image.tmdb.org/t/p/w500/or86B6Xjz39u0ZCNqSG0biF7XOP.jpg",
                "s1": "https://vidsrc.to/embed/movie/tt0111161",
                "s2": "https://vidsrc.me/embed/tt0111161",
                "s3": "https://v2.vidsrc.me/embed/tt0111161"
            }
        ]
    },
    {
        "genre": "Action",
        "movies": [
            {
                "title": "Action Movie",
                "poster": "https://image.tmdb.org/t/p/w500/6oom5QOTv0Y6InA39v9uJvAzvR5.jpg",
                "s1": "https://vidsrc.to/embed/movie/tt1234567",
                "s2": "https://vidsrc.me/embed/tt1234567",
                "s3": "https://v2.vidsrc.me/embed/tt1234567"
            }
        ]
    },
    {
        "genre": "Drama",
        "movies": []
    },
    {
        "genre": "TV Shows",
        "movies": []
    },
    {
        "genre": "Asian",
        "movies": []
    },
    {
        "genre": "Chinese",
        "movies": []
    }
]

@app.route('/movies', methods=['GET'])
def get_movies():
    # This sends the data to your Android app
    return jsonify(movie_data)

@app.route('/')
def home():
    return "Netflix Backend is Running! Go to /movies to see the data."

if __name__ == '__main__':
    # Railway will provide the PORT automatically
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
