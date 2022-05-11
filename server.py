"""Server for movie ratings app."""

from cgi import test
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, request, session
import os
import requests
from model import connect_to_db, db
from pprint import pprint


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['TMDB_KEY']

STREAMING_SERVICES = {'Netflix': 8, 'Amazon Prime Video': 9, 'Disney Plus': 337, 'Apple iTunes': 2, 'Google Play Movies': 3, 'Sun Nxt': 309, 'fuboTV': 257, 'Classix': 445, 'Hulu': 15, 'Rooster Teeth': 485, 'Paramount Plus': 531, 'Netflix Kids': 175, 'HBO Max': 384, 'Crunchyroll': 283, 'Peacock': 386, 'Cultpix': 692, 'Acorn TV': 87, 'Peacock Premium': 387, 'Apple TV Plus': 350, 'Amazon Video': 10, 'FilmBox+': 701, 'VIX ': 457, 'YouTube': 192, 'Curiosity Stream': 190, 'Kocowa': 464, 'Funimation Now': 269, 'Starz Play Amazon Channel': 194, 'WOW Presents Plus': 546, 'Paramount+ Amazon Channel': 582, 'Magellan TV': 551, 'EPIX Amazon Channel': 583, 'BroadwayHD': 554, 'Discovery+ Amazon Channel': 584, 'Showtime Amazon Channel': 203, 'Dekkoo': 444, 'AMC+ Amazon Channel': 528, 'HBO Now': 27, 'Hoichoi': 315, 'The Roku Channel': 207, 'BritBox': 151, 'Rakuten Viki': 344, 'Showtime Roku Premium Channel': 632, 'Pluto TV': 300, 'iQIYI': 581, 'Paramount+ Roku Premium Channel': 633, 'Starz Roku Premium Channel': 634, 'AMC+ Roku Premium Channel': 635, 'Epix Roku Premium Channel': 636, 'HBO Max Free': 616, 'YouTube Premium': 188, 'Hoopla': 212, 'The CW': 83, 'CW Seed': 206, 'Vudu': 7, 'VUDU Free': 332, 'Starz': 43, 'Showtime': 37, 'PBS': 209, 'Pantaflix': 177, 'CBS': 78, 'FXNow': 123, 'Tubi TV': 73, 'Kanopy': 191, 'Comedy Central': 243, 'Microsoft Store': 68, 'Redbox': 279, 'Max Go': 139, 'ABC': 148, 'DIRECTV': 358, 'Crackle': 12, 'AMC': 80, 'NBC': 79, 'Epix': 34, 'Freeform': 211, 'History': 155, 'Syfy': 215, 'A&E': 156, 'Lifetime': 157, 'Shudder': 99, 'Sundance Now': 143, 'Popcornflix': 241, 'Pantaya': 247, 'Boomerang': 248, 'Urban Movie Channel': 251, 'Dove Channel': 254, 'Yupp TV': 255, 'Eros Now': 218, 'Magnolia Selects': 259, 'WWE Network': 260, 'MyOutdoorTV': 264, 'Nickhits Amazon Channel': 261, 'Noggin Amazon Channel': 262, 'Hopster TV': 267, 'Laugh Out Loud': 275, 'Smithsonian Channel': 276, 'Pure Flix': 278, 'Hallmark Movies': 281, 'PBS Kids Amazon Channel': 293, 'Boomerang Amazon Channel': 288, 'Cinemax Amazon Channel': 289, 'Pantaya Amazon Channel': 292, 'Hallmark Movies Now Amazon Channel': 290, 'PBS Masterpiece Amazon Channel': 294, 'Viewster Amazon Channel': 295, 'MZ Choice Amazon Channel': 291, 'Sling TV': 299, 'HiDive': 430, 'Topic': 454, 'MTV': 453, 'Retrocrush': 446, 'Shout! Factory TV': 439, 'Chai Flicks': 438, 'Mhz Choice': 427, 'Vice TV ': 458, 'Shudder Amazon Channel': 204, 'AcornTV Amazon Channel': 196, 'BritBox Amazon Channel': 197, 'Fandor Amazon Channel': 199, 'Screambox Amazon Channel': 202, 'Sundance Now Amazon Channel': 205, 'Cartoon Network': 317, 'Adult Swim': 318, 'USA Network': 322, 'Fox': 328, 'FlixFling': 331, 'Bet+ Amazon Channel': 343, 'Darkmatter TV': 355, 'Bravo TV': 365, 'TNT': 363, 'Food Network': 366, 'BBC America': 397, 'IndieFlix': 368, 'AHCTV': 398, 'TLC': 412, 'HGTV': 406, 'DIY Network': 405, 'Investigation Discovery': 408, 'Science Channel': 411, 'Destination America': 402, 'Animal Planet': 399, 'Discovery Life': 404, 'Discovery': 403, 'Motor Trend': 410, 'Cooking Channel': 400, 'Travel Channel': 413, 'Paramount Network': 418, 'Here TV': 417, 'TV Land': 419, 'Logo TV': 420, 'VH1': 422, 'DreamWorksTV Amazon Channel': 263, 'TBS': 506, 'AsianCrush': 514, 'FILMRISE': 471, 'Revry': 473, 'Spectrum On Demand': 486, 'OXYGEN': 487, 'VRV': 504, 'tru TV': 507, 'DisneyNOW': 508, 'WeTV': 509, 'Discovery Plus': 520, 'ARROW': 529, 'Plex': 538, 'The Oprah Winfrey Network': 555, 'British Pathé TV': 571, 'Freevee Amazon Channel': 613, 'Netflix Free': 459, 'CBS All Access Amazon Channel': 198, 'Mubi': 11, 'GuideDoc': 100, 'Public Domain Movies': 638, 'Argo': 534, 'Eventive': 677, 'Spamflix': 521, 'DOCSVILLE': 475, 'Filmzie': 559, 'True Story': 567, 'DocAlliance Films': 569, 'KoreaOnDemand': 575, 'YouTube Free': 235, 'Criterion Channel': 258, 'ShortsTV Amazon Channel': 688, 'Fandor': 25, 'Screambox': 185, 'realeyz': 14, 'History Vault': 268, 'Lifetime Movie Club': 284, 'Night Flight Plus': 455, 'OVID': 433, 'The Film Detective': 470, 'Mubi Amazon Channel': 201, 'AMC on Demand': 352, 'TCM': 361, 'Flix Premiere': 432, 'Hi-YAH': 503, 'Alamo on Demand': 547, 'MovieSaints': 562, 'Dogwoof On Demand': 536, 'Film Movement Plus': 579, 'Metrograph': 585, 'Curia': 617, 'Kino Now': 640, 'Cinessance': 694}
TV_GENRES = {'Action & Adventure': 10759, 'Animation': 16, 'Comedy': 35, 'Crime': 80, 'Documentary': 99, 'Drama': 18, 'Family': 10751, 'Kids': 10762, 'Mystery': 9648, 'News': 10763, 'Reality': 10764, 'Sci-Fi & Fantasy': 10765, 'Soap': 10766, 'Talk': 10767, 'War & Politics': 10768, 'Western': 37}
MOVIE_GENRES = {'Action': 28, 'Adventure': 12, 'Animation': 16, 'Comedy': 35, 'Crime': 80, 'Documentary': 99, 'Drama': 18, 'Family': 10751, 'Fantasy': 14, 'History': 36, 'Horror': 27, 'Music': 10402, 'Mystery': 9648, 'Romance': 10749, 'Science Fiction': 878, 'TV Movie': 10770, 'Thriller': 53, 'War': 10752, 'Western': 37}


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route("/select-movie")
def select_movie():
    title = request.args.get("title")
    trailer_url = get_trailer('movie', title)
    print(title)

    return render_template("trailer.html", data=trailer_url)


@app.route("/select-tv")
def select_tv():
    title = request.args.get("title")
    trailer_url = get_trailer('tv', title)

    return render_template("trailer.html", data=trailer_url)

@app.route("/search-movie")
def search_criteria():
    genre_input = request.args.get("genre")
    streaming_service_input = request.args.get("streaming")
    genre_id = MOVIE_GENRES[genre_input]
    streaming_id = STREAMING_SERVICES[streaming_service_input]

    url = "https://api.themoviedb.org/3/discover/movie"
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
    for movie in data['results']:
        # trailer_url = get_trailer('movie', movie['title'])
        search_results.append([movie['title'], movie['overview']])
    return render_template("search.html", search_results=search_results)

def get_trailer(media_type, title):
    url = f"https://api.themoviedb.org/3/search/{media_type}"
    payload = {
        'api_key': API_KEY, 
        'query': title,
        'language': 'en-US'
    } 
    res = requests.get(url, params=payload)
    data = res.json()
    data_results = data['results'][0]

    # pprint(data_results, indent=1)

    if data_results == []:
        flash('Sorry, the title you entered does not exist in this database')
        return redirect('/')

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
        flash('Sorry, there is no trailer available in this database for that media title')
        return redirect('/')

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
    media_watchstatus = 'tbd'
    media_streaming = []
    
    provider_url = f"https://api.themoviedb.org/3/{media_type}/{media_id}/watch/providers"
    provider_payload = {
        'api_key': API_KEY, 
        'language': 'en-US'
    }

    provider_res = requests.get(provider_url, params=provider_payload)
    provider_data = provider_res.json()
    provider_name = provider_data['results']['US']['flatrate']
    # pprint(provider_data['results']['US'])
    # print(len(provider_name))
    for i in range(len(provider_name)):
        # print(provider_name[i]['provider_name'])
        media_streaming.append(provider_name[i]['provider_name'])
    print(media_name)
    return trailer_url

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
