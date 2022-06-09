"""Models for capstone project app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Replace this with your code!
class User(db.Model):
    """A user"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User ID={self.user_id}, email={self.email}>"

    @classmethod
    def create(cls, name, email, password):
        """Create and return a new user."""

        return cls(name=name, email=email, password=password)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()


class Watchlist(db.Model):
    """A watchlist"""
    __tablename__ = "watchlists"

    watchlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User', backref='watchlists')
    media = db.relationship('Media', secondary='media_watchlists', backref='watchlists')

    def __repr__(self):
        return f"<Watchlist ID={self.watchlist_id}, name={self.name}, user id={self.user_id}>"

    @classmethod
    def create(cls, name, description, user):
        """Create and return a new watchlist."""

        return cls(name=name, description=description, user=user)

    @classmethod
    def get_by_id(cls, watchlist_id):
        return cls.query.get(watchlist_id)

    @classmethod
    def get_by_info(cls, user, name):
        return cls.query.filter(Watchlist.user == user, Watchlist.name == name).first()

    # @classmethod
    # def get_by_email(cls, email):
    #     return cls.query.filter(User.email == email).first()
    @classmethod
    def contains_media(cls, watchlist_id, media):
        return cls.query.filter(Watchlist.watchlist_id == watchlist_id, Watchlist.media == media).first()

    @classmethod
    def all_watchlists(cls):
        return cls.query.all()

class MediaWatchlist(db.Model):
    """An association table for Media and Watchlist"""
    __tablename__ = "media_watchlists"

    mediawatchlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey('watchlists.watchlist_id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.media_id'))

    @classmethod
    def create(cls, watchlist_id, media_id):
        return cls(watchlist_id=watchlist_id, media_id=media_id)

    @classmethod
    def get_by_media_id(cls, media_id):
        return cls.query.get(media_id)

    @classmethod
    def get_by_watchlist_id(cls, watchlist_id):
        return cls.query.get(watchlist_id)

class Media(db.Model):
    """A media"""
    __tablename__ = "media"

    media_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    # duration = db.Column(db.Integer)
    # api_id = db.Column(db.Integer)
    # genre = db.Column(db.String)
    # streaming_id = db.Column(db.Integer)

    genres = db.relationship('Genre', secondary='media_genres', backref='media')
    streamings = db.relationship('Streaming', secondary='media_streamings', backref='media')
    

    def __repr__(self):
        return f"<Media ID={self.media_id}, name={self.name}>"

    @classmethod
    def create(cls, name, type):
        """Create and return a new user."""

        return cls(name=name, type=type)

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter(Media.name == name).first()

    @classmethod
    def all_media(cls):
        return cls.query.all()

    @classmethod
    def set_watch_status(cls):
        Media.media_watchlists 

    @classmethod
    def filter_media(cls, type, genre, streaming):
        if type == "both":
            if genre == "all" and streaming == "all":
                return cls.query.all()
            elif genre == "all":
                return cls.query.filter(Media.streamings.any(name=streaming)).all()
            elif streaming == "all":
                return cls.query.filter(Media.genres.any(name=genre)).all()
            else:
                return cls.query.filter(Media.streamings.any(name=streaming), Media.genres.any(name=genre)).all()
        else:
            if genre == "all" and streaming == "all":
                return cls.query.filter(Media.type == type).all()
            elif genre == "all":
                return cls.query.filter(Media.type==type, Media.streamings.any(name=streaming)).all()
            elif streaming == "all":
                return cls.query.filter(Media.type==type, Media.genres.any(name=genre)).all()
            else:
                return cls.query.filter(Media.type==type, Media.streamings.any(name=streaming), Media.genres.any(name=genre)).all()


class Genre(db.Model):
    """A genre"""
    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f"<Genre ID={self.genre_id}, name={self.name}>"

    @classmethod
    def create(cls, name):
        """Create and return a new genre type."""

        return cls(name=name)


class Streaming(db.Model):
    """A streaming platform"""
    __tablename__ = "streamings"

    streaming_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f"<Streaming ID={self.streaming_id}, name={self.name}>"

    @classmethod
    def create(cls, name):
        """Create and return a new genre type."""

        return cls(name=name)

class WatchStatus(db.Model):
    """An table for Watch Statuses"""
    __tablename__ = "watchstatuses"

    watchstatus_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.media_id'))
    status = db.Column(db.String) 

    def __repr__(self):
        return f"<WatchStatus ID={self.watchstatus_id}, status={self.status}>"

    @classmethod
    def create(cls, user_id, media_id, status):
        """Create and return a new genre type."""

        return cls(user_id=user_id, media_id=media_id, status=status)

    @classmethod
    def all_statuses(cls):
        return cls.query.all()

    @classmethod
    def get_status(cls, user_id, media_id):
        return cls.query.filter(WatchStatus.user_id==user_id, WatchStatus.media_id==media_id).first()

class MediaGenre(db.Model):
    """An association table for Media and Genres"""
    __tablename__ = "media_genres"

    mediagenre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.media_id'))

class MediaStreaming(db.Model):
    """An association table for Media and Streaming Platforms"""
    __tablename__ = "media_streamings"

    mediastreaming_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    streaming_id = db.Column(db.Integer, db.ForeignKey('streamings.streaming_id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.media_id'))


class Comments(db.Model):
    """An table for Comments"""
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.media_id'))
    title = db.Column(db.String)
    comment = db.Column(db.String)    

    @classmethod
    def create(cls, user_id, media_id, title, comment):
        """Create and return a new genre type."""

        return cls(user_id=user_id, media_id=media_id, title=title, comment=comment)

    @classmethod
    def get_by_media(cls, media_id):
        return cls.query.filter(Comments.media_id==media_id).all()

    @classmethod
    def get_by_comment_id(cls, comment_id):
        return cls.query.filter(Comments.comment_id==comment_id).first()


class Replies(db.Model):
    """An table for Replies"""
    __tablename__ = "replies"

    reply_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))
    reply = db.Column(db.String)

    @classmethod
    def create(cls, user_id, comment_id, reply):
        """Create and return a new genre type."""

        return cls(user_id=user_id, comment_id=comment_id, reply=reply)    

    @classmethod
    def get_by_comment(cls, comment_id):
        return cls.query.filter(Replies.comment_id==comment_id).all()


def connect_to_db(flask_app, db_uri="postgresql:///media", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
 
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)