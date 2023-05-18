from flask_restful import Resource ,fields, marshal_with, reqparse
from application.database import db
from application.models import Users, Posts ,Like
from application.validation import NotFoundError, BusinessValidationError
from werkzeug.security import generate_password_hash,check_password_hash



output_fields = {
    "user_id" : fields.Integer,
    "name" : fields.String,
    "username" : fields.String,
    "email" : fields.String,
    "city" : fields.String,
    "join_date" : fields.DateTime
}

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('name')
create_user_parser.add_argument('username')
create_user_parser.add_argument('email')
create_user_parser.add_argument('city')
create_user_parser.add_argument('hashed_password')


update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('name')
update_user_parser.add_argument('email')
update_user_parser.add_argument('city')
update_user_parser.add_argument('about_user')







class UserAPI(Resource):
    @marshal_with(output_fields)
    def get(self, user_id):
        user = db.session.query(Users).filter(Users.user_id == user_id).first()
        if user:
            return user
        else:
            raise NotFoundError(status_code = 404)




    @marshal_with(output_fields)
    def put(self, user_id):
        user = db.session.query(Users).filter(Users.user_id == user_id).first()
        if user is None:
            raise NotFoundError(status_code = 404)
        args = update_user_parser.parse_args()
        name = args.get("name", None)
        city = args.get("city", None)
        about_user = args.get("about_user", None)
        email = args.get("email", None)

        if email is None:
            raise BusinessValidationError(status_code=400, error_code="Email101", error_message="email is required")

        if "@" in email:
            pass
        else:
            raise BusinessValidationError(status_code=400, error_code="Email102", error_message="Invalid email")

        user = db.session.query(Users).filter(Users.email == email).first()
        if user:
            raise BusinessValidationError(status_code=400, error_code="Email103", error_message="Duplicate email")


        # Cheak, if user exists
        user = db.session.query(Users).filter(Users.user_id == user_id).first()
        if user is None:
            raise NotFoundError(status_code = 404)

        user.name = name
        user.city = city
        user.about_user = about_user
        user.email = email

        db.session.add(user)
        db.session.commit()

        return user





    def delete(self, user_id):
        user = db.session.query(Users).filter(Users.user_id == user_id).first()
        if user is None:
            raise NotFoundError(status_code = 404)

        posts = Posts.query.filter_by(author_id = user_id).first()
        if posts:
            raise BusinessValidationError(status_code=400, error_code="Delete101", error_message="Can't delete the user, there is a post written by this user") 
        
        db.session.delete(user)
        db.session.commit()

        return "", 200





    def post(self):
        args =create_user_parser.parse_args()
        name = args.get("name", None)
        username = args.get("username", None)
        email = args.get("email", None)
        city = args.get("city",None)
        hashed_password = args.get("hashed_password", None)

        if username is None:
            raise BusinessValidationError(status_code=400, error_code="User101", error_message="username is required")

        if email is None:
            raise BusinessValidationError(status_code=400, error_code="Email101", error_message="email is required")

        if "@" in email:
            pass
        else:
            raise BusinessValidationError(status_code=400, error_code="Email102", error_message="Invalid email")

        user = db.session.query(Users).filter((Users.username == username) | (Users.email == email)).first()

        if user:
            raise BusinessValidationError(status_code=400, error_code="User103", error_message=" Duplicate user")

        
        hashed_password = generate_password_hash(hashed_password, "sha256")

        new_user = Users(name = name , username = username, email = email, city = city, hashed_password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '', 201








output_fields_for_post = {
    "title" : fields.String,
    "key_note" : fields.String,
    "content" : fields.String
}



update_post_parser = reqparse.RequestParser()
update_post_parser.add_argument('title')
update_post_parser.add_argument('key_note')
update_post_parser.add_argument('content')



create_post_parser = reqparse.RequestParser()
create_post_parser.add_argument('title')
create_post_parser.add_argument('key_note')
create_post_parser.add_argument('content')
create_post_parser.add_argument('author_id')



class PostAPI(Resource):
    def get(self, post_id):
        post = db.session.query(Posts).filter(Posts.post_id == post_id).first()
        likes = db.session.query(Like).filter(Like.post_id == post_id)
        user_id = post.author_id
        like_count = likes.count()
        poster_name = Users.query.get_or_404(user_id)

        if post:
            return {"title": post.title, "key_note": post.key_note, "content": post.content, "likes": like_count, "poster_name" : poster_name.name }
        else:
            raise NotFoundError(status_code = 404)




    @marshal_with(output_fields_for_post)
    def put(self, post_id):
        post = db.session.query(Posts).filter(Posts.post_id == post_id).first()
        if post is None:
            raise NotFoundError(status_code = 404)
        args = update_post_parser.parse_args()
        title = args.get("title", None)
        key_note = args.get("key_note", None)
        content = args.get("content", None)


        post.title = title
        post.key_note = key_note
        post.content = content
        db.session.add(post)
        db.session.commit()

        return post





    def delete(self, post_id):
        post = db.session.query(Posts).filter(Posts.post_id == post_id).first()
        if post is None:
            raise NotFoundError(status_code = 404)

        db.session.delete(post)
        db.session.commit()

        return "", 200

    def post(self):
        args =create_post_parser.parse_args()
        title = args.get("title", None)
        key_note = args.get("key_note", None)
        content = args.get("content", None)
        author_id = args.get("author_id", None)


        if title is None:
            raise BusinessValidationError(status_code=400, error_code="Title101", error_message="title is required")

        if content is None:
            raise BusinessValidationError(status_code=400, error_code="Content101", error_message="Content is required")

        if author_id is None:
            raise BusinessValidationError(status_code=400, error_code="AuthorId101", error_message="author_id is required")


        new_post = Posts(title = title , key_note = key_note, content = content,author_id = author_id)
        db.session.add(new_post)
        db.session.commit()
        return '', 201
