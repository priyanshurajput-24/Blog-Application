from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from application.database import db
from datetime import datetime





# Create a follow/unfollow model 
class Follow_unfollow(db.Model):
    table_id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)
    followed_by_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)




# Create a blog user model 
class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String, unique=True,nullable = False )
    city = db.Column(db.String, nullable = False)
    join_date = db.Column(db.DateTime, default = datetime.utcnow)
    hashed_password = db.Column(db.String(128))
    profile_pic = db.Column(db.String(), nullable = True)
    posts = db.relationship('Posts', backref = "poster")
    comments = db.relationship('Comment', backref = "user", passive_deletes = True)
    likes = db.relationship('Like', backref = "user", passive_deletes = True)
    followed = db.relationship('Follow_unfollow',
                               foreign_keys=[Follow_unfollow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic')
    followers = db.relationship('Follow_unfollow',
                            foreign_keys=[Follow_unfollow.followed_by_id],
                            backref=db.backref('followed', lazy='joined'),
                            lazy='dynamic')
    about_user = db.Column(db.String, nullable = True)
    



    def get_id(self):        # It's for handling exception when user 'login'  -- comment it and see error    ====https://stackoverflow.com/questions/37472870/login-user-fails-to-get-user-id
           return (self.user_id)

    @property
    def password(self):
        raise AttributeError('You can not read Password !')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)


    # Create a string 
    def __repr__(self):
        return '<Name %r>' % self.name






# Create a blog post model 
class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable = False)
    key_note = db.Column(db.String)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)
    comments = db.relationship('Comment', backref = "post", passive_deletes = True)
    likes = db.relationship('Like', backref = "post", passive_deletes = True)




# Create a comment model 
class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable = False)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete = "CASCADE"), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id", ondelete = "CASCADE"), nullable = False)






# Create a like model 
class Like(db.Model):
    like_id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete = "CASCADE"), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id", ondelete = "CASCADE"), nullable = False)


