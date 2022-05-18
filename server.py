"""Server for movie ratings app."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, request, session
import os
import requests
from model import connect_to_db, db, User, Watchlist, Media, MediaWatchlist
from pprint import pprint
from api_search import STREAMING_SERVICES, GENRES, filter_genre
import random
import ast

app = Flask(__name__)
app.secret_key = "dev1"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['TMDB_KEY']

# os.system("dropdb media")
# os.system("createdb media")
connect_to_db(app)
# db.create_all()

@app.route('/')
def index():
    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)
    return render_template('homepage.html', user=user)

@app.route("/users")
def all_users():
    """View all users."""

    users = User.all_users()

    return render_template("all_users.html", users=users)

@app.route("/media")
def all_media():
    """View all media."""

    all_media = Media.all_media()

    return render_template("all_media.html", all_media=all_media)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = User.create(name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = User.get_by_id(user_id)

    return render_template("all_watchlists.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/')
    else:
        # Log in user by storing the user's email in session
        flash(f"Welcome back, {user.name}!")
        session["user_email"] = user.email
        return redirect('/')

@app.route("/create-watchlist", methods=["POST"])
def create_watchlist():
    name = request.form.get("watchlist_name")
    description = request.form.get("watchlist_desc")

    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)
    if not user:
        flash("You have not created an account yet")
        return redirect('/media-search')
    watchlist = Watchlist.create(name, description, user)
    db.session.add(watchlist)
    db.session.commit()
    print(watchlist)
    flash(f"You created a new watchlist named {watchlist.name}")

    return redirect('/media-search')

@app.route("/media-search")
def media_search():
    return render_template("media_search.html", streamings=STREAMING_SERVICES, genres=GENRES)


@app.route("/select-movie")
def select_movie():
    title = request.args.get("title")
    trailer_dict = get_trailer('movie', title)
    print(title)
    if trailer_dict['Success'] == True:
        print([trailer_dict['URL'], trailer_dict['name'], trailer_dict['id'], 'movie'])
        return render_template("trailer.html", media_info=[trailer_dict['URL'], trailer_dict['name'], trailer_dict['id'], 'movie'])
    else:
        flash(trailer_dict['Message'])
        return redirect('/media-search')
        

@app.route("/select-tv")
def select_tv():
    title = request.args.get("title")
    trailer_dict = get_trailer('tv', title)
    if trailer_dict['Success'] == True:
        return render_template("trailer.html", media_info=[trailer_dict['URL'], trailer_dict['name'], trailer_dict['id'], 'tv'])
    else:
        flash(trailer_dict['Message'])
        return redirect('/media-search')
    # Check if key success is true or false
    # If false, flash message with key message and return redirect
    # Redo to return render_template or redirect based on what comes back from get_trailer


@app.route("/search-results")
def search_results():
    media_type = request.args.get("media_type")
    genre_input = request.args.get("genre")
    streaming_service_input = request.args.get("streaming")
    print(genre_input, streaming_service_input, media_type)
    if genre_input == "":
        genre_id = ""
    else:
        genre_id = filter_genre(media_type, genre_input)
    if streaming_service_input == "":
        streaming_id = ""
    else:
        streaming_id = STREAMING_SERVICES.get(streaming_service_input, None)
    if genre_id == None or streaming_id == None:
        flash("Sorry, please re-enter search criteria")
        return redirect('/media-search')

    url = f"https://api.themoviedb.org/3/discover/{media_type}"
    payload = {
        'api_key': API_KEY, 
        'language': 'en-US',
        'with_genres': genre_id,
        'with_watch_providers': streaming_id,
        'watch_region': 'US',
        'with_watch_monetization_types': 'flatrate',
        'page': 1
    }
    res = requests.get(url, params=payload)
    data = res.json()
    search_results = []
    if media_type == 'tv':
        media_name = 'name'
    elif media_type == 'movie':
        media_name = 'title'

    for media in data['results']:
        search_results.append([media[media_name], media['overview']])
        # print(media)
    return render_template("search_results.html", search_results=search_results, form_name=f"/select-{media_type}")

def get_trailer(media_type, title):
    url = f"https://api.themoviedb.org/3/search/{media_type}"
    payload = {
        'api_key': API_KEY, 
        'query': title,
        'language': 'en-US'
    } 
    res = requests.get(url, params=payload)
    data = res.json()
    # pprint(data)
    data_results = data['results'][0]

    # pprint(data_results, indent=1)

    if data_results == []:
        trailer_dict = {'Success': False, 'URL': None, 'Message': 'Sorry, the title you entered does not exist in this database'}
        return trailer_dict
        # Redo to return mini dictionary with the key Success key URL and key message for this helper function if title does not exist
        # Success = False, URL = none, message = flash message above

    media_id = data_results['id']
    media_url = f"http://api.themoviedb.org/3/{media_type}/{media_id}"
    media_payload = {
        'api_key': API_KEY, 
        'language': 'en-US',
        'append_to_response': 'videos'
    } 
    media_res = requests.get(media_url, params=media_payload)
    media_data = media_res.json()

    # pprint(media_data, indent=1)

    if media_data['videos']['results'] == []:
        trailer_dict = {'Success': False, 'URL': None, 'Message': 'Sorry, there is no trailer available in this database for that media title'}
        # Redo here too
        # Success = False, URL = none, message = flash message above

    trailer_key = media_data['videos']['results'][0]['key']
    trailer_url = f"https://www.youtube.com/embed/{trailer_key}"

    media_id = media_data['id']
    if media_type == 'tv':
        media_name = media_data['name']
        media_duration = media_data['episode_run_time']
    elif media_type == 'movie':
        media_name = media_data['title']
        media_duration = media_data['runtime']
    # media_type already defined
    # media_api_id = 
    media_streaming = []
    
    provider_url = f"https://api.themoviedb.org/3/{media_type}/{media_id}/watch/providers"
    provider_payload = {
        'api_key': API_KEY, 
        'language': 'en-US'
    }

    provider_res = requests.get(provider_url, params=provider_payload)
    # print(provider_res.status_code)
    provider_data = provider_res.json()
    # pprint(provider_data)
    # provider_name = provider_data['results']['US']['flatrate']
    # print(len(provider_name))
    # for i in range(len(provider_name)):
        # print(provider_name[i]['provider_name'])
        # media_streaming.append(provider_name[i]['provider_name'])
    print(media_name)
    trailer_dict = {'Success': True, 'URL': trailer_url, 'Message': None, 'id': media_id, 'name': media_name}
    return trailer_dict
    # Success = True, URL = trailer_url, message = none

@app.route('/similar-media/<media_type>/<media_id>')
def similar_media(media_type, media_id):
    url = f"https://api.themoviedb.org/3/{media_type}/{media_id}/similar"
    payload = {
        'api_key': API_KEY, 
        'language': 'en-US'
    } 
    res = requests.get(url, params=payload)
    data = res.json()
    # pprint(data)
    if media_type == 'tv':
        title = 'name'
    elif media_type == 'movie':
        title = 'title'
    index = random.randrange(len(data['results']))
    print(index)
    media_name = data['results'][index][title]
    trailer_dict = get_trailer(media_type, media_name)
    if trailer_dict['Success'] == True:
        return render_template("trailer.html", media_info=[trailer_dict['URL'], trailer_dict['name'], trailer_dict['id'], media_type])
    else:
        flash(trailer_dict['Message'])
        return redirect('/media-search')

@app.route('/add-to-watchlist')
def add_to_watchlist():
    watchlist_name = request.args.get("watchlist-name")
    print("##################", watchlist_name)
    media_info = request.args.get("media-info")
    print(media_info)
    print(type(media_info))
    media_info = ast.literal_eval(media_info)
    print(media_info)
    print(type(media_info))

    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)

    watchlist = Watchlist.get_by_info(user, watchlist_name)
    if not watchlist:
        flash("That watchlist does not exist")
        return render_template("trailer.html", media_info=media_info)

    print("??????????????", watchlist.name)
    print(media_info)
    media_name = media_info[1]
    media_type = media_info[3]
    media = Media.query.filter(Media.name == media_name).first()
    if not media:
        media = Media.create(media_name, media_type, 'Yet to begin')
    watchlists_containing_media = Watchlist.query.filter(Watchlist.media.any(name=media_name)).all()
    if watchlist in watchlists_containing_media:
        flash(f"{media_name} has already been added to watchlist {watchlist.name}")
        return render_template("trailer.html", media_info=media_info)

    watchlist.media.append(media)
    db.session.commit()
    flash(f"Added {media_name} to watchlist {watchlist.name}")
    return render_template('all_watchlists.html', user=user)

@app.route('/watchlists/<watchlist_id>')
def view_watchlist(watchlist_id):
    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)
    watchlist = Watchlist.get_by_id(watchlist_id)
    return render_template('watchlist_details.html', watchlist=watchlist)
    

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    # connect_to_db(app)
    app.run(debug=True)
