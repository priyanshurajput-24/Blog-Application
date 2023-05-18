from application.webforms import PostForms, LoginForm, UserForm, SearchForm ,CommentForm
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask import render_template, request, redirect, url_for, flash
from application.models import Users,Posts, Follow_unfollow, Like,Comment
from werkzeug.security import generate_password_hash, check_password_hash
from application.database import db
from app import app
from werkzeug.utils import secure_filename
import uuid as uuid
import os


# Route for home page
# @app.route("/login",methods= ["GET"])
# def main():
    # return render_template("base.html")

####--------------------------------------------####
#### --------- User Related Routing ----------- ####
####--------------------------------------------####



# Flask Login Work
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))




# Create a Login route
@app.route("/", methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            #Cheak the HASH
            if check_password_hash(user.hashed_password, form.password.data):
                login_user(user)
                return redirect(url_for('posts'))
    return render_template("login.html", form = form)



# Create a log out route
@app.route("/logout", methods = ["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



# Create a Dashboard route
@app.route("/dashboard", methods = ["GET","POST"])
@login_required
def dashboard():
    user_id,poster = current_user.user_id,current_user.user_id
    form = UserForm()
    name_to_update = Users.query.get_or_404(user_id)
    user_posts = Posts.query.filter_by(author_id= poster).all()
    total_follower = Follow_unfollow.query.filter_by(follower_id = user_id).all()
    total_following = Follow_unfollow.query.filter_by(followed_by_id = user_id).all()
    return render_template('dashboard.html', form = form, name_to_update = name_to_update, user_id = user_id, user_posts = user_posts, total_follower = total_follower , total_following = total_following)




# Create add user route
@app.route("/user/add", methods = ["GET","POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user is None:
            # Hashed the password
            hashed_password = generate_password_hash(form.hashed_password.data, "sha256")
            user  = Users(name = form.name.data, username = form.username.data, email = form.email.data, city = form.city.data,  hashed_password = hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user)  #--  **This line is used for IMMEDIATELY login of user after just registering***
            return redirect(url_for('posts'))

        
        flash("Please use a different username !")


        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.city.data = ''
        form.hashed_password.data = ''
    return render_template("add_user.html", form = form, name = name)




# Create update user route
@app.route("/update/<int:user_id>",methods = ["GET","POST"])
@login_required
def update(user_id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(user_id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.city = request.form['city']
        name_to_update.username = request.form['username']
        name_to_update.about_user = request.form['about_user']


        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']    
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            saver = request.files['profile_pic']
            name_to_update.profile_pic = pic_name

            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

                return redirect(url_for('dashboard'))
            except:
                return render_template('update.html', form = form, name_to_update = name_to_update, user_id = user_id)

        else:
            db.session.commit()
            return redirect(url_for('dashboard'))

    else:
        return render_template('update.html', form = form, name_to_update = name_to_update, user_id = user_id )




# Create delete user route
@app.route("/delete/<int:user_id>")
@login_required
def delete(user_id):
    user_posts = Posts.query.filter_by(author_id = user_id).all()
    if user_posts:
        flash("Please remove all your Posts")
        return redirect(url_for('dashboard'))
    else:
        if user_id == current_user.user_id:
            name = None
            form = UserForm()
            user_to_delete = Users.query.get_or_404(user_id) 
            try:
                db.session.delete(user_to_delete)
                db.session.commit()
                our_users = Users.query.order_by(Users.join_date)
                return redirect(url_for('add_user'))

            except:
                our_users = Users.query.order_by(Users.join_date)
                return render_template("add_user.html", form = form, name = name, our_users = our_users)
        else:
            flash("Sorry You can't delete this user ..")
            return redirect(url_for('dashboard'))



#This Pass Stuff to Nav-Bar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form = form)



#Create a Search route in username
@app.route("/search_in_username", methods = ["GET","POST"])
def search_in_username():
    form = SearchForm()
    users = Users.query
    if form.validate_on_submit():
        searched = form.searched.data
        users = users.filter(Users.name.like("%"+  searched + "%"))
        users = users.order_by(Users.name).all()
        return render_template("search_in_username.html", form = form, searched =searched , users = users)



#Create a User Profile route
@app.route('/user_view/<int:user_id>',methods = ["GET","POST"])
def user_view(user_id):
    user = Users.query.get_or_404(user_id)
    user_posts = Posts.query.filter_by(author_id= user_id).all()
    total_follower = Follow_unfollow.query.filter_by(follower_id = user_id).all()
    total_following = Follow_unfollow.query.filter_by(followed_by_id = user_id).all()
    return render_template("user_view.html",user = user, total_follower = total_follower,user_posts = user_posts, total_following = total_following)









####--------------------------------------------####
#### --------- Post Related Routing ----------- ####
####--------------------------------------------####        



#Add a Post Page
@app.route("/add-post", methods = ['GET','POST'])
@login_required
def add_post():
    form = PostForms()

    if form.validate_on_submit():
        poster = current_user.user_id
        post = Posts(title = form.title.data, content = form.content.data, author_id = poster, key_note = form.key_note.data)
        form.title.data = ''
        form.content.data = ''
        form.key_note.data = ''     
        db.session.add(post)
        db.session.commit()
        posts = Posts.query.filter_by(author_id = current_user.user_id).all()
        return render_template("posts.html", posts = posts)

    return render_template("add_post.html", form = form)




# View All Post route Without Comment
@app.route("/posts", methods= ["get","post"])
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts = posts)



# View Particular Post route With Comment
@app.route("/post/<int:post_id>", methods = ["GET","POST"])
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id =  post_id)
    return render_template("post.html", post = post, comments = comments)




# Add a Edit Post route
@app.route("/posts/edit/<int:post_id>", methods = ["GET","POST"])
def edit_post(post_id):
    post = Posts.query.get_or_404(post_id)
    form = PostForms()
    if form.validate_on_submit():
        post.title = form.title.data
        post.key_note = form.key_note.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post', post_id = post.post_id))
    if current_user.user_id == post.author_id:
        form.title.data = post.title
        form.key_note.data = post.key_note
        form.content.data = post.content 
        return render_template("edit_post.html", form = form)
    else:
        print("you are not authorised to delete this post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts = posts)




# Add a Delete Post route
@app.route("/posts/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    post_to_delete = Posts.query.get_or_404(post_id)
    post_id = current_user.user_id 
    if post_id == post_to_delete.poster.user_id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts = posts)

        except:
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts = posts)
    else:
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts = posts)




####-----------------------------------------------####
#### --------- Comment Related Routing ----------- ####
####-----------------------------------------------####        


# Add a comment route
@app.route("/comment/<post_id>", methods = ["POST","GET"])
@login_required
def post_comment(post_id):
    post = Posts.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id =  post_id)
    form = CommentForm()
    if form.validate_on_submit():
        user = current_user.name
        comment = Comment(text = form.text.data, author = user, post_id = post_id)
        form.text.data = ''
        db.session.add(comment)
        db.session.commit()
        post = Posts.query.get_or_404(post_id)
        return redirect(url_for('post', post_id = post_id))
    
    return render_template("comment.html", form = form,post_id = post_id,post = post, comments = comments)





####---------------------------------------------------####
#### --------- Like a Post Related Routing ----------- ####
####---------------------------------------------------####        




# Add a liking post route
@app.route("/like_post/<post_id>", methods = ["POST","GET"])
@login_required
def like_post(post_id):
    post = Posts.query.filter_by(post_id = post_id)
    like = Like.query.filter_by(author = current_user.name, post_id = post_id).first()

    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author = current_user.name, post_id = post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('post', post_id = post_id))






####-------------------------------------------------------####
#### --------- Follow/Unfollow Related Routing ----------- ####
####-------------------------------------------------------####        




# Add a Follow/Unfollow user route
@app.route("/follow_user/<user_id>", methods = ["POST","GET"])
@login_required
def follow_user(user_id):
    follower = Follow_unfollow.query.filter_by(followed_by_id = current_user.user_id, follower_id = user_id).first()

    if follower:
        db.session.delete(follower)
        db.session.commit()
    else:
        follower = Follow_unfollow(follower_id = user_id, followed_by_id = current_user.user_id)
        db.session.add(follower)
        db.session.commit()
    return redirect(url_for('user_view', user_id = user_id))

