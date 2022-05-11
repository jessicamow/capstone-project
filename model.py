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

    def __repr__(self):
        return f"<Watchlist ID={self.watchlist_id}, name={self.name}>"

    @classmethod
    def create(cls, name, description):
        """Create and return a new user."""

        return cls(name=name, description=description)

    @classmethod
    def get_by_id(cls, watchlist_id):
        return cls.query.get(watchlist_id)

    # @classmethod
    # def get_by_email(cls, email):
    #     return cls.query.filter(User.email == email).first()

    @classmethod
    def all_watchlists(cls):
        return cls.query.all()


class Media(db.Model):
    """A media"""
    __tablename__ = "media"

    media_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    duration = db.Column(db.Integer)
    api_id = db.Column(db.String)
    watch_status = db.Column(db.String)
    genre = db.Column(db.String)
    streaming_id = db.Column(db.Integer)

    # user = db.relationship('User', backref='watchlists')

    def __repr__(self):
        return f"<Media ID={self.media_id}, name={self.name}>"

    @classmethod
    def create(cls, name, type, duration, api_id, watch_status, genre, streaming_id):
        """Create and return a new user."""

        return cls(name=name, type=type, duration=duration, api_id=api_id, watch_status=watch_status, genre=genre, streaming_id=streaming_id)

    @classmethod
    def get_by_id(cls, media_id):
        return cls.query.get(media_id)

    # @classmethod
    # def get_by_email(cls, email):
    #     return cls.query.filter(User.email == email).first()

    @classmethod
    def all_media(cls):
        return cls.query.all()

def connect_to_db(flask_app, db_uri="postgresql:///test", echo=True):
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