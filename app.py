import os

from bson.objectid import ObjectId
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash, generate_password_hash

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_pokemon", methods=["GET", "POST"])
def get_pokemon():
    pokedex = mongo.db.pokemon.find()
    # if request.method == "POST":
    #     mongo.db.pokemon
    return render_template("pokemon.html", pokedex=pokedex)


@app.route("/edit_pokemon/<dex_id>", methods=["GET", "POST"])
def edit_pokemon(dex_id):
    if request.method == "POST":
        submit = {
            "name": request.form.get("name"),
            "dex_id": request.form.get("dex_id"),
            "type": [
                request.form.get("type_1"),
                request.form.get("type_2")
            ],
            "species": request.form.get("species"),
            "height": [
                request.form.get("height_feet"),
                request.form.get("height_inches")
            ],
            "weight": request.form.get("weight"),
            "desc": request.form.get("desc"),
            "img_src": request.form.get("img_src"),
            "created_by": request.form.get("created_by"),
        }
        mongo.db.pokemon.update({"_id": ObjectId(dex_id)}, submit)
        flash("Pokemon updated!")
        return redirect(url_for("get_pokemon"))

    pokedex = mongo.db.pokemon.find()
    selected_pokemon = mongo.db.pokemon.find_one({"_id": ObjectId(dex_id)})
    return render_template("edit_pokemon.html", pokedex=pokedex, pokemon=selected_pokemon)


@app.route("/delete_pokemon/<dex_id>")
def delete_pokemon(dex_id):
    mongo.db.pokemon.remove({"_id": ObjectId(dex_id)})
    flash("Pokemon deleted :(")
    return redirect(url_for("get_pokemon"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.trainers.find_one(
            {"username": request.form.get("username")})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                print(session["user"])
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password :(")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password :(")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("Logged out. Bye!")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab Trainer profile for session user
    trainer = mongo.db.trainers.find_one({"username": session["user"]})
    return render_template("profile.html", trainer=trainer)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        username_taken = mongo.db.trainers.find_one(
            {"username": request.form.get("username").lower()})

        if username_taken:
            flash("Username unavailable!")
            return redirect(url_for("register"))

        trainers_length = mongo.db.trainers.count()
        trainer_id = trainers_length + 1
        private = False if request.form.get("private") else True
        new_trainer = {
            "name": request.form.get("name"),
            "trainer_id": trainer_id,
            "hometown": request.form.get("hometown"),
            "fav_type": request.form.get("fav_type"),
            "fav_pokemon": request.form.get("fav_pokemon"),
            "bio": request.form.get("bio"),
            "img_src": request.form.get("img_src"),
            "squad": [
                request.form.get("squad_1 "),
                request.form.get("squad_2 "),
                request.form.get("squad_3 "),
                request.form.get("squad_4 "),
                request.form.get("squad_5 "),
                request.form.get("squad_6 "),
            ],
            "username": request.form.get("username"),
            "password": generate_password_hash(request.form.get("password")),
            "private": private,
            "rating": 0,
            "rated_by": []
        }
        mongo.db.trainers.insert_one(new_trainer)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Trainer registered!")
        return redirect(url_for("profile", username=session["user"]))

    pokedex = list(mongo.db.pokemon.find())
    return render_template("register.html", pokedex=pokedex)


@app.route("/contribute", methods=["GET", "POST"])
def contribute():
    if request.method == "POST":
        pokedex_length = mongo.db.pokemon.count()
        dex_id = pokedex_length + 1
        new_pokemon = {
            "name": request.form.get("name"),
            "dex_id": dex_id,
            "type": [
                request.form.get("type_1"),
                request.form.get("type_2")
            ],
            "species": request.form.get("species"),
            "height": [
                request.form.get("height_feet"),
                request.form.get("height_inches")
            ],
            "weight": request.form.get("weight"),
            "desc": request.form.get("desc"),
            "img_src": request.form.get("img_src"),
            "created_by": request.form.get("created_by"),
            "rating": 0,
            "in_squad": [],
            "rated_by": []

        }
        mongo.db.pokemon.insert_one(new_pokemon)
        flash("Pokemon discovered!")
        return redirect(url_for('get_pokemon'))

    return render_template("contribute.html")


@app.route("/trainers")
def trainers():
    trainers = mongo.db.trainers.find()
    return render_template("trainers.html", trainers=trainers)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
