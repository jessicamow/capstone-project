"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import model
import server

os.system("dropdb media")
os.system("createdb media")

model.connect_to_db(server.app)
model.db.create_all()

# Load movie data from JSON file
# with open("data/media.json") as f:
#     media_data = json.loads(f.read())

# # Create 3 users; each user will make 1 watchlist
# for n in range(3):
#     email = f"user{n}@test.com"  # Voila! A unique email!
#     password = "test"
#     name = f"User{n}"

#     user = model.User.create(name, email, password)

#     w_name = f"watchlist{n}"
#     w_desc = f"details for watchlist{n}"
#     w_user = user

#     watchlist = model.Watchlist.create(w_name, w_desc, w_user)

#     random_media = media_data[n]
#     name, type, watch_status, genres, streamings = (
#         random_media["name"],
#         random_media["type"],
#         random_media["watch_status"],
#         random_media["genres"],
#         random_media["streamings"]
#     )
#     media = model.Media.get_by_name(name)

#     if not media:
#         media = model.Media.create(name, type)

#         for genre in genres:
#             add_genre = model.Genre.create(genre)
#             media.genres.append(add_genre)

#         for streaming in streamings:
#             add_streaming = model.Streaming.create(streaming)
#             media.streamings.append(add_streaming)       

    
#     watchlist.media.append(media)
    
#     model.db.session.add(user)
#     model.db.session.add(watchlist)
#     model.db.session.commit()

#     print(user.user_id, media.media_id)
#     watch_status = model.WatchStatus.create(user.user_id, media.media_id, watch_status)
#     model.db.session.add(watch_status)
#     model.db.session.commit()
