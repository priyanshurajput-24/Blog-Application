from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_ckeditor import CKEditor
import uuid as uuid
from application.config import LocalDevelopmentConfig
from application.database import db
import os

app = None
api = None
ckeditor = None
def create_app():
    app = Flask(__name__, template_folder="templates")
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    ckeditor = CKEditor(app)
    migrate = Migrate(app, db)
    app.config['SECRET_KEY'] = "12341234"
    UPLOAD_FOLDER = 'static/images/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    api = Api(app)
    app.app_context().push()
    return app, api, ckeditor

app, api, ckeditor = create_app()


from application.controllers import *

# Add all restful controllers
from application.api import UserAPI, PostAPI
api.add_resource(UserAPI, "/api/user", "/api/user/<int:user_id>")
api.add_resource(PostAPI, "/api/post", "/api/post/<int:post_id>")

 


if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080, debug=True)
