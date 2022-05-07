"""Server for movie ratings app."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, request, session
import os
import requests
# from model import connect_to_db, db


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['TMDB_KEY']


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route("/search")
def all_users():
    title = request.args.get("title")
    url = "https://api.themoviedb.org/3/search/movie"
    payload = {
        'api_key': API_KEY, 
        'query': title,
        'language': 'en-US'
    } 
    res = requests.get(url, params=payload)
    data = res.json()
    if data['results'] == []:
        flash('The movie does not exist in this database')
        return redirect('/')
        
    data_results = data['results']
    if len(data_results) > 1:
        data_results = data_results[0]
    movie_id = data_results['id']
    movie_url = f"http://api.themoviedb.org/3/movie/{movie_id}/videos"
    movie_payload = {
        'api_key': API_KEY, 
        # 'append_to_response': 'videos'
        'language': 'en-US'
    } 
    movie_res = requests.get(movie_url, params=movie_payload)
    movie_data = movie_res.json()
    trailer_key = movie_data['results'][0]['key']
    trailer_url = f"https://www.youtube.com/embed/{trailer_key}"

    return render_template("search.html", data=trailer_url)


# @app.route("/users", methods=["POST"])
# def register_user():
#     email = request.form.get("email")
#     password = request.form.get("password")

#     if crud.get_user_by_email(email) == None:
#         newUser = crud.create_user(email, password)
#         print('this is the if blockn\n')

#         flash('Account was succesfully created')
#     else:
#         # crud.get_user_by_email(email)
#         print('this if the else block\n')
#         flash('Email already exists.')

#     return redirect('/')


# @app.route('/users/<user_id>')
# def user_details(user_id):
#     user_details = crud.get_user_by_id(user_id)
#     return render_template("user_details.html", users=user_details)
# # <a href="/movies">


# @app.route('/login', methods=['POST'])
# def to_login():
#     flash('Logged In')
#     return redirect('/')


# @app.route('/movies')
# def all_movies():
#     '''View all movies'''
#     movies = crud.get_movies()
#     return render_template("all_movies.html", movies=movies)


# @app.route('/movies/<movie_id>')
# def movie_details(movie_id):
#     movie_details = crud.get_movie_by_id(movie_id)
#     return render_template("movie_details.html", movie=movie_details)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    # connect_to_db(app)
    app.run(debug=True)
