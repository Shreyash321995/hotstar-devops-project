from flask import Flask, render_template, request
import requests
import  os 

app = Flask(__name__)

API_KEY = os.getenv("TMDB_API_KEY")

@app.route('/')
def home():

    query = request.args.get("query")

    if query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
    else:
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

    response = requests.get(url)

    movies = []

    if response.status_code == 200:

        data = response.json()

        for movie in data["results"][:10]:

            movie_id = movie["id"]

            poster = ""

            if movie.get("poster_path"):
                poster = "https://image.tmdb.org/t/p/w500" + movie["poster_path"]

            trailer = "#"

            video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

            video_response = requests.get(video_url)

            if video_response.status_code == 200:

                videos = video_response.json()["results"]

                for video in videos:

                    if video["site"] == "YouTube":

                        trailer = f"https://www.youtube.com/watch?v={video['key']}"

                        break

            movies.append({
                "title": movie["title"],
                "poster": poster,
                "trailer": trailer
            })

    return render_template("index.html", movies=movies)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
