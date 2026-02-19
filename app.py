from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/movies')
def scrape_movies():
    movie_list = []
    try:
        # Example URL - using a public trending list
        target_url = "https://vidsrc.to/trending" 
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This logic grabs the poster and title from the HTML
        for card in soup.select('.movie-item')[:30]:
            movie_list.append({
                "name": card.select_one('.title').text.strip(),
                "poster": card.select_one('img')['src'],
                "url": "https://vidsrc.to" + card.select_one('a')['href']
            })
    except Exception as e:
        # Static backup if the site is down
        movie_list = [{"name": "Avatar", "poster": "https://image.tmdb.org/t/p/w500/kuf6evRbcS3SKEA3oVvznZ10yak.jpg", "url": ""}]
        
    return jsonify(movie_list)

@app.route('/register')
def register():
    # Simple ID provider
    return "01"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
