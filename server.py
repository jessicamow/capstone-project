"""Server for movie ratings app."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, request, session, jsonify
import os
import requests
from model import connect_to_db, db, User, Watchlist, Media, MediaWatchlist, Genre, MediaGenre, Streaming, MediaStreaming, WatchStatus, Comments, Replies
from pprint import pprint
from api_search import STREAMING_SERVICES, GENRES, filter_genre, get_genre_data
import random
import ast

app = Flask(__name__)
app.secret_key = "dev2"
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
    watch_statuses = []
    if user:
        for watchlist in user.watchlists:
            for media in watchlist.media:
                watch_status = WatchStatus.get_status(user.user_id, media.media_id)
                watch_statuses.append(watch_status)
                print(watch_status)
    return render_template('homepage.html', user=user, watch_statuses=watch_statuses)

@app.route("/users")
def all_users():
    """View all users."""

    users = User.all_users()

    return render_template("all_users.html", users=users)

@app.route("/media")
def all_media():
    """View all media."""

    all_users = User.all_users()
    all_media = Media.all_media()

    return render_template("all_media.html", streamings=STREAMING_SERVICES, genres=GENRES)

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

    return render_template("homepage.html", user=None)

@app.route("/log-out", methods=["POST"])
def log_out():

    if session.get("user_email"):
        session.pop("user_email")

    return render_template("homepage.html", user=None)


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = User.get_by_id(user_id)

    return render_template("all_watchlists.html", user=user)

@app.route('/trying-users')
def trying():
    data = {}

    all_users = User.all_users()
    index = 0
    for user in all_users:
        data[index] = user.name
        print(user.name)
        index += 1

    print(data)
    return jsonify(data)


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
    print(watchlist)
    db.session.add(watchlist)
    db.session.commit()
    print(watchlist)
    flash(f"You created a new watchlist named {watchlist.name}")

    return redirect('/')

@app.route("/media-search")
def media_search():
    return render_template("media_search.html", streamings=STREAMING_SERVICES, genres=GENRES)


@app.route("/select-movie")
def select_movie():
    title = request.args.get("title")
    trailer_dict = get_trailer('movie', title)
    print(title)
    if trailer_dict['Success'] == True:
        return jsonify({'success': True,
                    'media_data': trailer_dict['media_data']})
        # return render_template("trailer.html", media_info=[trailer_dict['URL'], trailer_dict['name'], trailer_dict['id'], 'tv'])
    else:
        return jsonify({'success': False, 'message': trailer_dict['Message']})
        

@app.route("/select-tv")
def select_tv():
    title = request.args.get("title")
    trailer_dict = get_trailer('tv', title)
    if trailer_dict['Success'] == True:
        return jsonify({'success': True,
                    'media_data': trailer_dict['media_data']})
        # return render_template("trailer.html", media_info=[trailer_dict['URL'], trailer_dict['name'], trailer_dict['id'], 'tv'])
    else:
        return jsonify({'success': False, 'message': trailer_dict['Message']})
        # flash(trailer_dict['Message'])
        # return redirect('/media-search')
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
        return jsonify({'success': False, 'message': 'Sorry, please re-enter search criteria'})
        # flash("Sorry, please re-enter search criteria")
        # return redirect('/media-search')

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
        search_results.append([media[media_name], media['overview'], media_type])
        # print(media)
    return jsonify({'success': True,
                    'search_results': search_results})
    # return render_template("search_results.html", search_results=search_results, form_name=f"/select-{media_type}")

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

    if media_type == 'tv':
        media_name = media_data['name']
        media_duration = media_data['episode_run_time']
    elif media_type == 'movie':
        media_name = media_data['title']
        media_duration = media_data['runtime']
    media_genres = media_data['genres']
    media_genres_data = []
    for genre in media_genres:
        print(genre)
        media_genres_data.extend(get_genre_data(genre['name']))

    print("@@@@@@@@@@@@@@", media_genres_data)
    media_api_id = media_data['id']
    media_overview = media_data['overview']
    media_streaming = []
    watch_status = "TBD"
    
    provider_url = f"https://api.themoviedb.org/3/{media_type}/{media_api_id}/watch/providers"
    provider_payload = {
        'api_key': API_KEY, 
        'language': 'en-US'
    }

    provider_res = requests.get(provider_url, params=provider_payload)
    # print(provider_res.status_code)
    provider_data = provider_res.json()
    # pprint(provider_data)
    if provider_data['results']['US'].get("flatrate"):
        providers = provider_data['results']['US']['flatrate']
        for i in range(len(providers)):
            media_streaming.append(providers[i]['provider_name'])
    else:
        media_streaming.append("No subscription services found that offer this media; need to purchase")
    media_data = [trailer_url, media_name, media_type, media_api_id, watch_status, media_genres_data, media_streaming, media_overview]
    trailer_dict = {'Success': True, 'media_data': media_data}
    return trailer_dict
    # Success = True, URL = trailer_url, message = none

@app.route('/similar-media/<media_type>/<media_id>')
def similar_media(media_type, media_id):
    url = f"https://api.themoviedb.org/3/{media_type}/{media_id}/recommendations"
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
        return jsonify({'success': True,
                    'media_data': trailer_dict['media_data']})
    else:
        return jsonify({'success': False, 'message': trailer_dict['Message']})

@app.route('/add-to-watchlist')
def add_to_watchlist():
    watchlist_name = request.args.get("watchlist-name")
    print("##################", watchlist_name)
    media_data = request.args.get("media-data")
    print(media_data)
    print(type(media_data))
    media_data = media_data.split(",")
    print(media_data)
    print(type(media_data))

    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)
    print("****************", user.user_id)

    watchlist = Watchlist.get_by_info(user, watchlist_name)
    if not watchlist:
        # flash("That watchlist does not exist")
        # return render_template("trailer.html", media_info=media_info)
        return jsonify({'message': "Sorry, that watchlist has not yet been created!"})

    print("??????????????", watchlist.name)
    print(media_data)
    media_URL = media_data[0]
    media_name = media_data[1]
    media_type = media_data[2]
    media_ID = media_data[3]
    watch_status = media_data[4]
    media_genres = media_data[5]
    media_streaming = media_data[6]
    print(media_name)
    print(media_type)
    print(media_ID)
    print(watch_status)
    print(media_genres)
    print(media_streaming)
    print("!!!!!!! executed through here0")
    media = Media.get_by_name(media_name)
    print(media)
    print("!!!!!!! executed through here1")
    if not media:
        media = Media.create(media_name, media_type)
        print(media)
        db.session.add(media)
        db.session.commit()
        print(media)
        print("!!!!!!! executed through here2")
        # media.genres.append(media_genres)
        # media.streamings.append(media_streaming)
        genre = Genre.create("Comedy")
        print(genre)
        print(media.genres)
        print(media.streamings)
        media.genres.append(genre)
        print("!!!!!!! executed through here3")
        print(media.genres)
        print("*******", user.user_id, media.media_id)
        print("********", watch_status)
    watchlists_containing_media = Watchlist.query.filter(Watchlist.media.any(name=media_name)).all()

    if watchlist in watchlists_containing_media:
        # flash(f"{media_name} has already been added to watchlist {watchlist.name}")
        # return render_template("trailer.html", media_info=media_info)
        return jsonify({'message': f"{media_name} has already been added to your watchlist!"})
    
    watch_status = WatchStatus.create(user.user_id, media.media_id, "TBD")
    db.session.add(watch_status)
    db.session.commit()
    print(user.user_id, media.media_id)
    print(watch_status)
    watchlist.media.append(media)
    db.session.commit()
    # flash(f"Added {media_name} to watchlist {watchlist.name}")
    # return render_template('all_watchlists.html', user=user)
    print("!!!!!!! executed through here4")
    return jsonify({'message': f"Successfully added {media_name} to your watchlist!"})

@app.route('/watchlists/<watchlist_id>')
def view_watchlist(watchlist_id):
    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)
    watchlist = Watchlist.get_by_id(watchlist_id)
    print("############", watchlist)
    print(watchlist.media)
    return render_template('watchlist_details.html', watchlist=watchlist)
    
@app.route('/filter-media')
def filter_media():
    filter_type = request.args.get("filter_type")
    filter_genre = request.args.get("filter_genre")
    filter_streaming = request.args.get("filter_streaming")

    print("****", filter_type, "*****", filter_genre, "*****", filter_streaming)

    if filter_genre == "":
        filter_genre = "all"
    if filter_streaming == "":
        filter_streaming = "all"

    filter_media_results = Media.filter_media(filter_type, filter_genre, filter_streaming)
    all_statuses = WatchStatus.all_statuses()
    for status in all_statuses:
        print(status.user_id, status.media_id)

    print(filter_media_results)
    print(all_statuses)

    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)

    friends_media = {}
    media_names = []
    media_types = []
    media_watch_statuses = []
    media_descriptions = []
    media_trailers = []
    media_users = []
    media_genres = []
    media_streamings = []
    for media in filter_media_results:
        friends_media[media.name] = {}
        friends_media[media.name]["type"] = media.type
        friends_media[media.name]["user_info"] = []
        for watchlist in media.watchlists:
            # friends_media[media.name]["user_info"].append({"user_name":watchlist.user.name, "watch_status":watch_status.status})
            print(watchlist)
            media_names.append(media.name)
            media_types.append(media.type)
            media_users.append(watchlist.user.name)
            print(watchlist.user.user_id, media.media_id)
            watch_status = WatchStatus.get_status(watchlist.user.user_id, media.media_id)
            print("hhhhhhhhhh", watchlist.user.user_id, media.media_id)
            print(watchlist.user.name, media.name)
            print(watch_status)
            media_watch_statuses.append(watch_status.status)
            friends_media[media.name]["user_info"].append({"user_name":watchlist.user.name, "watch_status":watch_status.status})
    pprint(friends_media)

    for key, value in list(friends_media.items()):
        print(value)
        print(len(value['user_info']))
        print(value['user_info'][0]['user_name'])
        if len(value['user_info']) == 1 and value['user_info'][0]['user_name'] == user.name:
            friends_media.pop(key)
    pprint(friends_media)

    return jsonify({'success': True,
                    'media_names': media_names,
                    'media_types': media_types,
                    'media_watch_statuses': media_watch_statuses,
                    'media_users': media_users,
                    'friends_media': friends_media,
                    'logged_user': user.name})


@app.route('/view-discussion-threads')
def view_discussion_threads():
    media_name = request.args.get("media-name")
    print(media_name)
    selected_media = Media.get_by_name(media_name)
    comments = Comments.get_by_media(selected_media.media_id)

    users = []
    for comment in comments:
        user_id = comment.user_id
        user = User.get_by_id(user_id)
        users.append(user)

    if session.get("media_discussion"):
        session.pop("media_discussion")
    session["media_discussion"] = media_name

    print("viewing discussion threads")
    print("******* comments", comments)
    return render_template("discussion.html", media_name=media_name, comments=comments, users=users)


@app.route('/add-discussion-threads')
def add_discussion_threads():

    new_comment = request.args.get("post")
    title = request.args.get("title")
    print(new_comment)

    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)

    
    # selected_media = Media.get_by_name(media_name)
    # comments = Comments.get_by_media(selected_media.media_id)

    print("viewing discussion threads")

    media_name = session["media_discussion"]
    media = Media.get_by_name(media_name)
    add_comment = Comments.create(user.user_id, media.media_id, title, new_comment)
    db.session.add(add_comment)
    db.session.commit()

    comments = Comments.get_by_media(media.media_id)

    users = []
    for comment in comments:
        user_id = comment.user_id
        user = User.get_by_id(user_id)
        users.append(user)

    # print("******* comments", comments)
    # return render_template("discussion.html", media_name=media_name, comments=comments)
    return jsonify({'success': True,
                    'user': user.name,
                    'title': add_comment.title,
                    'comment_id': add_comment.comment_id})
    # return render_template("discussion.html", media_name=media_name, comments=comments, users=users)

@app.route('/view-individual-thread')
def view_individual_thread():
    comment_id = request.args.get("comment_id")

    if session.get("comment_thread"):
        session.pop("comment_thread")
    session["comment_thread"] = comment_id

    selected_thread = Comments.get_by_comment_id(comment_id)
    user_created_thread = User.get_by_id(selected_thread.user_id)
    title = selected_thread.title
    comment = selected_thread.comment
    replies = []
    user_replies = []
    replies_in_db = Replies.get_by_comment(comment_id)
    for reply in replies_in_db:
        replies.append(reply.reply)
        user_reply = User.get_by_id(reply.user_id)
        user_replies.append(user_reply.name)

    return jsonify({'success': True,
                    'title': title,
                    'comment': comment,
                    'user_comment': user_created_thread.name,
                    'replies': replies,
                    'user_replies': user_replies})

@app.route('/add-reply')
def add_reply():
    reply = request.args.get("reply")

    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)

    comment_id = session["comment_thread"] 

    new_reply = Replies.create(user.user_id, comment_id, reply)
    db.session.add(new_reply)
    db.session.commit()

    return jsonify({'success': True,
                    'reply': reply,
                    'user_reply': user.name})   

@app.route('/update-status')
def update_status():
    status = request.args.get("updated-status")

    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)

    media_name = session["media_discussion"]
    media = Media.get_by_name(media_name)

    prev_status = WatchStatus.get_status(user.user_id, media.media_id)

    if not prev_status:
        return jsonify({'success': False,
                    'message': "Sorry, this show has not been added to your watchlist yet!"})   
    
    prev_status.status = status
    db.session.commit()

    return jsonify({'success': True,
                    'message': "Successfully updated your watch status!"})   


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    # connect_to_db(app)
    app.run(debug=True)
