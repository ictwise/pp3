from flask import flash, render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_uploads import UploadSet, configure_uploads, IMAGES, DATA, ALL
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from cooknride import app, db, mongo
from cooknride.models import Cuisine, Users
import os
import cloudinary
import cloudinary.uploader

images = UploadSet('images', IMAGES)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if "user" not in session:
        flash("You need to be logged in to add a recipe")
        return redirect(url_for("get_recipes"))

    if request.method == "POST":
        if request.files:

            file = request.files['file']

        if file:
            filename = file.save(os.path.join(
                                            app.config["UPLOADED_IMAGES_DEST"], 
                                            secure_filename(file.filename)
            ))

    recipe = {
        "cuisine_id": request.form.get("cuisine_id"),
        "title": request.form.get("title"),
        "ingredients": request.form.get("ingredients"),
        "date_posted": request.form.get("date_posted"),
        "image": ("cooknride/static/images/" + secure_filename(file.filename)),
        "user_id": session["user"]
    }
    mongo.db.recipes.insert_one(recipe)

    flash("Recipe Successfully Added")
    cuisines = list(Cuisine.query.order_by(Cuisine.cuisine_name).all())

    return render_template("add_recipe.html", cuisines=cuisines)


@app.route('/upload_image', methods=["GET", "POST"])
def upload_image():
   
    if request.method == "POST":
        if request.files:

            file = request.files['file']

            if file:
                file.save(os.path.join(
                                        app.config["UPLOADED_IMAGES_DEST"], 
                                        secure_filename(file.filename)
                                        ))

    return render_template("add_recipe.html")


@app.route("/get_cuisines")
def get_cuisines():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage cuisines!")
        return redirect(url_for("get_cuisines"))

    cuisines = list(Cuisine.query.order_by(Cuisine.cuisine_name).all())
    return render_template("cuisines.html", cuisines=cuisines)


@app.route("/add_cuisine", methods=["GET", "POST"])
def add_cuisine():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage cuisines!")
        return redirect(url_for("get_cuisines"))

    if request.method == "POST":
        cuisine = Cuisine(cuisine_name=request.form.get("cuisine_name"))
        db.session.add(cuisine)
        db.session.commit()
        return redirect(url_for("get_cuisines"))
    return render_template("add_cuisine.html")


@app.route("/edit_cuisine/<int:cuisine_id>", methods=["GET", "POST"])
def edit_cuisine(cuisine_id):
    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage cuisines!")
        return redirect(url_for("get_cuisines"))
    
    cuisine = Cuisine.query.get_or_404(cuisine_id)
    if request.method == "POST":
        cuisine.cuisine_name = request.form.get("cuisine_name")
        db.session.commit()
        return redirect(url_for("get_cuisines"))
    return render_template("edit_cuisine.html", cuisine=cuisine)


@app.route("/delete_cuisine/<int:cuisine_id>")
def delete_cuisine(cuisine_id):
    if session["user"] != "admin":
        flash("You must be admin to manage cuisines!")
        return redirect(url_for("cuisines"))

    cuisine = Cuisine.query.get_or_404(cuisine_id)
    db.session.delete(cuisine)
    db.session.commit()
    mongo.db.cuisines.delete_many({"cuisine_id": str(cuisine_id)})
    return redirect(url_for("get_cuisines"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = Users.query.filter(Users.user_name == 
                                           request.form.get("username").lower()
                                           ).all()
  
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
    
        user = Users(
            user_name=request.form.get("username").lower(),
            email=request.form.get("email").lower(),
            password=generate_password_hash(request.form.get("password"))
        )
    
        db.session.add(user)
        db.session.commit()

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = Users.query.filter(Users.user_name == 
                                           request.form.get("username").lower()
                                           ).all()

        if existing_user:
            print(request.form.get("username"))
            # ensure hashed password matches user input
            if check_password_hash(
                        existing_user[0].password, request.form.get("password")
                        ):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
      
    if "user" in session:
        return render_template("profile.html", username=session["user"])

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))



