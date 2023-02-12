from flask import flash, render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_uploads import UploadSet, configure_uploads, IMAGES, DATA, ALL
from werkzeug.datastructures import FileStorage
from cooknride import app, db, mongo
from cooknride.models import Cuisine, Users
import os
from datetime import datetime


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    if "user" in session:
        current_user = session["user"]
        recipes = list(mongo.db.recipes.find())
        return render_template(
            "recipes.html", recipes=recipes, current_user=current_user)

    else:
        recipes = list(mongo.db.recipes.find())
        return render_template("recipes.html", recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes)


@app.route("/recipe/<_id>", methods=["GET", "POST"])
def recipe(_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(_id)})
    return render_template("recipe.html",
                           recipe=recipe)


@app.route("/get_cuisines")
def get_cuisines():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage cuisines!")
        return redirect(url_for("get_cuisines"))

    cuisines = list(Cuisine.query.order_by(Cuisine.cuisine_name).all())
    return render_template("cuisines.html", cuisines=cuisines)

@app.route("/cuisine_deleted")
def cuisine_deleted():
    return render_template("cuisine_deleted.html")

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
    cuisine = Cuisine.query.get_or_404(cuisine_id)
    db.session.delete(cuisine)
    db.session.commit()
    mongo.db.recipes.delete_many({"cuisine_id": str(cuisine_id)})
    flash("Cuisine Successfully Deleted")
    return redirect(url_for("cuisine_deleted"))


@app.route("/manage_cuisines")
def manage_cuisines():
    cuisines = get_cuisines()
    return render_template("cuisines.html", cuisines=cuisines)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if "user" not in session:
        flash("You need to be logged in to add a recipe")
        return redirect(url_for("get_recipes"))

    if request.method == "POST":
        recipe = {
                  "cuisine_id": request.form.get("cuisine_id"),
                  "title": request.form.get("title"),
                  "ingredients": request.form.get("ingredients"),
                  "date_posted": request.form.get("date_posted"),
                  "image": request.form.get("image"),
                  "user_id": session["user"],
                  "method": request.form.get("method")
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added")
        return redirect(url_for("get_recipes"))

    cuisines = list(Cuisine.query.order_by(Cuisine.cuisine_name).all())
    return render_template(
        "add_recipe.html", date_posted=datetime.now().strftime('%Y-%m-%d'),
        cuisines=cuisines)


@app.route("/edit_recipe/<_id>", methods=["GET", "POST"])
def edit_recipe(_id):

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(_id)})

    if "user" not in session or (
            session["user"] != recipe["user_id"] and
            session["user"] != "admin"):
        flash("You can only edit your own recipes or admins, log in!")
        return redirect(url_for("get_recipes"))

    if request.method == "POST":
        submit = {
                  "cuisine_id": request.form.get("cuisine_id"),
                  "title": request.form.get("title"),
                  "ingredients": request.form.get("ingredients"),
                  "date_posted": request.form.get("date_posted"),
                  "image": request.form.get("image"),
                  "method": request.form.get("method"),
                  "user_id": session["user"]
        }
        mongo.db.recipes.update_one({'_id': ObjectId(_id)}, {'$set': submit})
        flash("Recipe Successfully Updated")
        return redirect(url_for("get_recipes"))
    cuisines = list(Cuisine.query.order_by(Cuisine.cuisine_name).all())
    return render_template("edit_recipe.html",
                           recipe=recipe, cuisines=cuisines)


@app.route("/delete_recipe/<_id>")
def delete_recipe(_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(_id)})

    if "user" not in session or (
            session["user"] != recipe["user_id"]
            and session["user"] != "admin"):
        flash(
         "You can only delete your own recipes or if you are an admin, log in!"
        )
        return redirect(url_for("get_recipes"))

    mongo.db.recipes.delete_many({"_id": ObjectId(_id)})
    flash("Recipe deleted!")
    return redirect(url_for("get_recipes"))


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
