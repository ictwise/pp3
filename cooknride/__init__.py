import os
import re
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
app.secret_key = os.environ.get("SECRET_KEY")
# config for image uploads
images = UploadSet('images', IMAGES)
app.config["UPLOADED_IMAGES_DEST"] = "static/images"
app.config["UPLOAD_DIRECTORY"] = "cooknride/static/images/"
configure_uploads(app, images)

cloudinary.config( 
                    cloud_name="djnbzkd3z",
                    api_key="932831466982918", 
                    api_secret="fUTJZMmuWUglHVe_QigZTqgE5kc" 
)

if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")  # local
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri  # heroku


db = SQLAlchemy(app)
mongo = PyMongo(app)

from cooknride import routes   # nqa
