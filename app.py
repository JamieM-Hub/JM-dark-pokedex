import os

from bson.objectid import ObjectId
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_pymongo import PyMongo, pymongo
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

if os.path.exists("env.py"):
    import env

types = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", 
        "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon"]

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

def process_search(data, query, returned, url):
    if returned:
        return render_template(url, data=returned)
    else:
        flash("nothing found")
        return redirect(url_for('get_pokemon'))
        

@app.route("/")
@app.route("/index")
def index():
    flash("Helloooooooooo!!")
    return render_template("index.html")


@app.route("/get_pokemon")
def get_pokemon():
    discovered = list(mongo.db.pokemon.find({ "dex_id" : {'$gt': 1000} }).sort("dex_id", pymongo.DESCENDING))
    original = list(mongo.db.pokemon.find({ "dex_id" : {'$lt': 1000} }).sort("dex_id", pymongo.ASCENDING))
    pokedex = discovered + original
    return render_template("pokemon.html", pokedex=pokedex)


@app.route("/get_pokemon/<id>")
def get_selected_pokemon(id):
    pokedex = mongo.db.pokemon.find()
    return redirect(url_for('get_pokemon', _anchor=id))


@app.route("/search_pokemon", methods=["GET", "POST"])
def search_pokemon():
    if request.method == "POST":
        pokedex = mongo.db.pokemon.find()
        query = request.form.get("query")
        returned = list(mongo.db.pokemon.find({"$text": {"$search": query}}).sort("name", pymongo.ASCENDING))
        process_search(pokedex, query, returned, "pokemon.html")
        data=returned
    else:
        data=pokedex

    return render_template("pokemon.html", pokedex=data)


@app.route("/search_trainers", methods=["GET", "POST"])
def search_trainers():
    if request.method == "POST":
        league = mongo.db.trainers.find()
        query = request.form.get("query")
        returned = list(mongo.db.trainers.find({"$text": {"$search": query}}).sort("name", pymongo.ASCENDING))
        process_search(league, query, returned, "trainers.html")
        data=returned
    else:
        data=league

    return render_template("trainers.html", trainers=data)


@app.route("/edit_pokemon/<dex_id>", methods=["GET", "POST"])
def edit_pokemon(dex_id):
    pokedex = mongo.db.pokemon.find()
    selected_pokemon = mongo.db.pokemon.find_one({"_id": ObjectId(dex_id)})

    if request.method == "POST":
        submit = {
            "name": request.form.get("name"),
            "dex_id": selected_pokemon['dex_id'],
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
            "created_by": selected_pokemon['created_by'],
            "rating": selected_pokemon['rating'],
            "in_squad": selected_pokemon['in_squad'],
            "rated_by": selected_pokemon['rated_by']
        }
        mongo.db.pokemon.update({"_id": ObjectId(dex_id)}, submit)
        flash(submit["name"].capitalize() + " updated!")
        return redirect(url_for("get_pokemon", id=submit['dex_id']))

    return render_template("edit_pokemon.html", pokedex=pokedex, pokemon=selected_pokemon, types=types)


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


@app.route("/profile/<username>")
def profile(username):
    trainer = mongo.db.trainers.find_one({"username": username})
    print(trainer['username'])
    # created_pokemon = list(mongo.db.trainers.find({"$text": {"$search": username}}).sort("name", pymongo.ASCENDING))
    created = mongo.db.pokemon.find({"created_by": username})
    return render_template("profile.html", trainer=trainer, pokedex=created)


@app.route("/edit_profile/<username>/<index>", methods=["GET", "POST"])
def edit_profile(username, index):
    # grab Trainer profile for session user and full sorted Pokedex
    trainer = mongo.db.trainers.find_one({"username": username})
    pokedex = list(mongo.db.pokemon.find().sort("name", pymongo.ASCENDING))
    if request.method == "POST":
        # serialize form input into new_profile
        private = False if request.form.get("private") else True
        submit = {
            "name": request.form.get("name"),
            "hometown": request.form.get("hometown"),
            "trainer_id": trainer['trainer_id'],
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
            "username": trainer['username'],
            "password": request.form.get("password"),
            "private": private,
            "rating": trainer['rating'],
            "rated_by": trainer['rated_by']
        }       
        print(f"\n{submit['username']}: {submit['password']}\n")
        print(f"{trainer['username']}: {trainer['password']}\n")
        # ensure hashed password matches user input
        if not check_password_hash(trainer['password'], submit['password']):
            # invalid password
            flash("Incorrect Password :(")
            return render_template("edit_profile.html", trainer=submit, pokedex=pokedex, types=types)
        else:
            # valid password
            submit['password'] = trainer['password']
            flash("Trainer ID updated!")
            mongo.db.trainers.update({"_id": ObjectId(index)}, submit)
            return redirect(url_for('profile', username=session['user']))
            
    trainer = mongo.db.trainers.find_one({"username": username})
    pokedex = list(mongo.db.pokemon.find().sort("name", pymongo.ASCENDING))        
    return render_template("edit_profile.html", trainer=trainer, pokedex=pokedex, types=types)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        username_taken = mongo.db.trainers.find_one(
            {"username": request.form.get("username")})

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
            "username": request.form.get("username").lower(),
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
        last_created_pokemon = list(mongo.db.pokemon.find().sort("dex_id", pymongo.DESCENDING).limit(1))
        dex_id = last_created_pokemon[0]['dex_id'] + 1
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

    return render_template("contribute.html", types=types)


@app.route("/trainers")
def trainers():
    trainers = mongo.db.trainers.find()
    return render_template("trainers.html", trainers=trainers)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # get date and time (https://www.programiz.com/python-programming/datetime/current-datetime)
        now = datetime.now().strftime("%H:%M | %d/%m/%Y")
        feedback = {
            "name": request.form.get("name"),
            "feedback": request.form.get("feedback"),
            "submitted_at": now
        }
        mongo.db.feedback.insert_one(feedback)
        flash("Thanks for the feedback!")
        return redirect(url_for('contact'))

    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
