from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Like(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    
  def __repr__(self) -> str:
    return 'Like>>> {self.id}'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    liked_posts = db.relationship('Post', backref="user")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return 'User>>> {self.username}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    #nested_post = db.Column(db.Integer, db.ForeignKey('post.id')) #Shared post
    #comments = db.relationship('Comment', backref="post") #Comments
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return 'Post>>> {self.id}'



