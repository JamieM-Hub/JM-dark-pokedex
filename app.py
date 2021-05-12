# Import
import os

from bson.objectid import ObjectId
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_pymongo import PyMongo, pymongo
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

if os.path.exists("env.py"):
    import env

# Flask
app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
mongo = PyMongo(app)

# Global vars

# all possible types
types = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", 
        "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon"]

# link to default image for pokemon or trainer creation preview
default_img_p = "https://i.pinimg.com/originals/95/d5/cd/95d5cded00f3a3e8a98fb1eed568aa9f.png"
default_img_t = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Man_standing_silhouette.svg/253px-Man_standing_silhouette.svg.png"

# Global funcs

def process_search(page, data, query, returned, url):
    query = "\"" + query + "\""
    if returned:
        flash(f"{page} found for {query}")
        return render_template(url, data=returned)
    else:
        flash(f"No {page} found for {query}")
        return redirect(url_for('get_pokemon'))
        

# Routes
@app.route("/")
@app.route("/index")
def index():
    if not session:
        flash("Welcome to the Dark Pokedex!")
    return render_template("index.html")


@app.route("/get_pokemon")
def get_pokemon():
    # display pokemon in ascending order from negative (user created pokemon) to positive (original pokemon)
    discovered = list(mongo.db.pokemon.find({ "dex_id" : {'$gt': 1000} }).sort("dex_id", pymongo.DESCENDING))
    original = list(mongo.db.pokemon.find({ "dex_id" : {'$lt': 1000} }).sort("dex_id", pymongo.ASCENDING))
    pokedex = discovered + original

    # supply trainers to display trainer's name next to created pokemon
    trainers = list(mongo.db.trainers.find())

    return render_template("pokemon.html", pokedex=pokedex, trainers=trainers)


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
        process_search("Pokemon", pokedex, query, returned, "pokemon.html")
        data=returned
    else:
        data=pokedex

    return render_template("pokemon.html", pokedex=data)


@app.route("/rate_pokemon/<index>/<unrate>", methods=["GET", "POST"])
def rate_pokemon(index, unrate):
    # get rated pokemon
    pokedex = mongo.db.pokemon.find()
    rated_pokemon = mongo.db.pokemon.find_one({"_id": ObjectId(index)})

    # logic
    if unrate == "False":
        # add user to pokemon's rated_by array
        mongo.db.pokemon.update(
            {"_id": ObjectId(index)},
            {"$push": {"rated_by": session['user']}}
        )
        # increment trainer rating
        mongo.db.trainers.update(
            {"username": rated_pokemon['created_by']},
            {"$inc": {"rating": 1}}
        )
    else:
        # remove user from pokemon's rated_by array
        mongo.db.pokemon.update(
            {"_id": ObjectId(index)},
            {"$pull": {"rated_by": session['user']}}
        )
        # decrement trainer rating
        mongo.db.trainers.update(
            {"username": rated_pokemon['created_by']},
            {"$inc": {"rating": -1}}
        )

    # update pokemon rating number according to new length of rated_by
    rated_pokemon = mongo.db.pokemon.find_one({"_id": ObjectId(index)})
    rating = len(rated_pokemon['rated_by'])
    mongo.db.pokemon.update(
        {"_id": ObjectId(index)},
        {"$set": {"rating": rating}}
    )

    # get rated pokemon's id for anchor
    id = rated_pokemon['dex_id']

    return redirect(url_for('get_pokemon', id=id))


@app.route("/rate_trainer/<index>/<unrate>", methods=["GET", "POST"])
def rate_trainer(index, unrate):
    # get rated trainer
    trainers = mongo.db.trainers.find()
    rated_trainer = mongo.db.trainers.find_one({"_id": ObjectId(index)})
    rating = rated_trainer['rating']

    # logic
    if unrate == "False":
        # add user to trainer's rated_by array
        mongo.db.trainers.update(
            {"_id": ObjectId(index)},
            {"$push": {"rated_by": session['user']}}
        )
        rating += 1;
    else:
        # remove user from trainer's rated_by array
        mongo.db.trainers.update(
            {"_id": ObjectId(index)},
            {"$pull": {"rated_by": session['user']}}
        )
        rating -= 1;

    # update trainer rating number according to sum of trainer and their pokemons' rated_by
    mongo.db.trainers.update(
        {"_id": ObjectId(index)},
        {"$set": {"rating": rating}}
    )

    # get rated trainer's id for anchor
    id = rated_trainer['trainer_id']

    return redirect(url_for('trainers', id=id))


@app.route("/search_trainers", methods=["GET", "POST"])
def search_trainers():
    if request.method == "POST":
        trainers = mongo.db.trainers.find()
        query = request.form.get("query")
        returned = list(mongo.db.trainers.find({"$text": {"$search": query}}).sort("name", pymongo.ASCENDING))
        process_search("Trainers", trainers, query, returned, "trainers.html")
        data=returned
    else:
        data=league

    return render_template("trainers.html", trainers=data)


@app.route("/edit_pokemon/<index>", methods=["GET", "POST"])
def edit_pokemon(index):
    # get selected pokemon
    selected_pokemon = mongo.db.pokemon.find_one({"_id": ObjectId(index)})

    # get user info
    user = mongo.db.trainers.find_one(
        {"username": session['user']})
    trainer_name = user['name']

    # create updated record
    if request.method == "POST":
        updated_pokemon = {
            "name": request.form.get("name").lower(),
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

        # prevent duplicate pokemon names
        pokemon_exists = mongo.db.pokemon.find_one({"name": updated_pokemon['name']})
        if updated_pokemon['name'] != selected_pokemon['name'] and pokemon_exists:
            flash(updated_pokemon['name'].upper() + " already exists!")     
            return render_template("edit_pokemon.html", index=index, pokemon=updated_pokemon, trainer_name=trainer_name, types=types)

        # prevent duplicate types
        if updated_pokemon['type'][0] == updated_pokemon['type'][1]:
            flash("Pokemon cannot have two identical types.")
            return render_template("edit_pokemon.html", index=index, pokemon=updated_pokemon, trainer_name=trainer_name, types=types)    

        # update record
        else:
            mongo.db.pokemon.update({"_id": ObjectId(index)}, updated_pokemon)
            flash(updated_pokemon['name'].upper() + " updated!")
            return redirect(url_for("profile", username=session['user']))

    return render_template("edit_pokemon.html", index=index, pokemon=selected_pokemon, trainer_name=trainer_name, types=types)


@app.route("/preview_pokemon/<username>/<index>", methods=["GET", "POST"])
def preview_pokemon(username, index):
    # get selected pokemon
    selected_pokemon = mongo.db.pokemon.find_one({"_id": ObjectId(index)})

    # create preview record and render
    preview = {
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
    return render_template("edit_pokemon.html", pokemon=preview, index=index, types=types)


@app.route("/delete_pokemon/<index>", methods=["GET", "POST"])
def delete_pokemon(index):
    # grab user info from db
    user = mongo.db.trainers.find_one(
        {"username": session['user']})

    # user enters correct password
    if check_password_hash(
            user["password"], request.form.get("password")):
            
        # remove record
        deleted_pokemon = mongo.db.pokemon.find_one({"_id": ObjectId(index)})
        mongo.db.pokemon.remove({"_id": ObjectId(index)})

        # display deletion confirmation and return to user profile
        flash(deleted_pokemon['name'].upper() + " was deleted from the Dark Pokedex.")
        return redirect(url_for('profile', username=session['user']))

    # user enters incorrect password
    else:
        flash("Password incorrect.")
        return render_template("edit_pokemon.html", pokemon=deleted_pokemon, index=index, types=types)

    # catch error
    flash("Deletion failed.")
    return redirect(url_for('profile', username=session['user']))


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
                flash("Welcome back " + existing_user['name'] + ", we missed you!")
                return redirect(url_for("profile", username=session["user"]))

            else:
                # invalid password match
                flash("Login details do not match any existing Trainer.")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Login details do not match any existing Trainer.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("Come back soon! Enjoy the real world!")
    session.pop("user")

    return redirect(url_for("login"))


@app.route("/profile/<username>")
def profile(username):
    trainer = mongo.db.trainers.find_one({"username": username})
    created = mongo.db.pokemon.find({"created_by": username}).sort("dex_id", pymongo.DESCENDING)
    
    return render_template("profile.html", trainer=trainer, pokedex=created)


@app.route("/edit_profile/<username>/<index>", methods=["GET", "POST"])
def edit_profile(username, index):
    # grab Trainer profile for session user
    trainer = mongo.db.trainers.find_one({"username": username})

    # grab full sorted pokedex as list
    pokedex = list(mongo.db.pokemon.find().sort("name", pymongo.ASCENDING))

    if request.method == "POST":
        # serialize form input into new_profile
        private = False if request.form.get("private") else True
        updated_trainer = {
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
            "username": request.form.get('username').lower(),
            "password": trainer['password'],
            "private": private,
            "rating": trainer['rating'],
            "rated_by": trainer['rated_by']
        }

        # VALIDATION
        # prevent duplicate username
        username_taken = mongo.db.trainers.find_one(
            {"username": request.form.get("username")})
        if updated_trainer['username'] != trainer['username'] and username_taken:
            flash(f"Username \"{updated_trainer['username']}\" is taken! Please try a different username.")
            return render_template("edit_profile.html", index=index, trainer=updated_trainer, pokedex=pokedex, types=types)

        # if user attempts password change
        if request.form.get("change_password") or request.form.get("confirm_password"):
            # check change_password matches confirm_password
            if request.form.get("change_password") == request.form.get("confirm_password"):
                # update user password to new password
                updated_trainer['password'] = generate_password_hash(request.form.get("change_password"))
            else:
                # display error if new password fields do not match
                flash("New password fields did not match - please try again.")
                return render_template("edit_profile.html", index=index, trainer=updated_trainer, pokedex=pokedex, types=types)

        # VERIFICATION
        # ensure hashed password matches user input
        if not check_password_hash(trainer['password'], request.form.get("password")):
            # invalid password
            flash("Password incorrect!")
            return render_template("edit_profile.html", index=index, trainer=updated_trainer, pokedex=pokedex, types=types)
        else:
            # valid password - update Trainer record
            mongo.db.trainers.update({"_id": ObjectId(index)}, updated_trainer)
            flash(updated_trainer['name'] + "'s profile updated. Looking fresh!")

            # update session user
            session['user'] = updated_trainer['username']
            return redirect(url_for('profile', username=session['user'], index=index))

    else:    
        return render_template("edit_profile.html", trainer=trainer, index=index, pokedex=pokedex, types=types)


@app.route("/preview_profile/<username>/<index>", methods=["GET", "POST"])
def preview_profile(username, index):
    trainer = mongo.db.trainers.find_one({"username": username})
    pokedex = list(mongo.db.pokemon.find().sort("name", pymongo.ASCENDING)) 

    if request.method == "POST":
        # serialize form input into new_profile
        private = False if request.form.get("private") else True
        preview = {
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
        return render_template("edit_profile.html", trainer=preview, index=index, pokedex=pokedex, types=types)
    
    return 


@app.route("/register", methods=["GET", "POST"])
def register():
    # get pokedex as list
    pokedex = list(mongo.db.pokemon.find())

    if request.method == "POST":
        # calculate back-end record fields
        trainers_length = mongo.db.trainers.count()
        trainer_id = trainers_length + 1
        private = False if request.form.get("private") else True
        if (request.form.get("img_src") == ""):
            img_src = default_img_t
        else:
            img_src = request.form.get("img_src")

        # create new trainer record
        new_trainer = {
            "name": request.form.get("name"),
            "trainer_id": trainer_id,
            "hometown": request.form.get("hometown"),
            "fav_type": request.form.get("fav_type"),
            "fav_pokemon": request.form.get("fav_pokemon"),
            "bio": request.form.get("bio"),
            "img_src": img_src,
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

        # prevent duplicate trainer name
        # name_taken = mongo.db.trainers.find_one(
        #     {"name": request.form.get("name")})
        # if name_taken:
        #     flash("That Trainer Name is taken! Trainer Names are case sensitive so try a different case or a different name.")
        #     return render_template("register.html", trainer=new_trainer, pokedex=pokedex, types=types)

        # prevent duplicate username
        username_taken = mongo.db.trainers.find_one(
            {"username": request.form.get("username").lower()})
        if username_taken:
            flash("That username is taken! Usernames are not case sensitive so try a different username.")
            return render_template("register.html", trainer=new_trainer, pokedex=pokedex, types=types)
 
        # create new Trainer record
        mongo.db.trainers.insert_one(new_trainer)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Welcome to the Dark Pokedex, " + new_trainer['name'] + "!")
        return redirect(url_for("profile", username=session["user"]))

    else:
        return render_template("register.html", pokedex=pokedex, types=types)


@app.route("/contribute", methods=["GET", "POST"])
def contribute():
    # get user info from db
    user = mongo.db.trainers.find_one(
        {"username": session['user']})
    trainer_name = user['name']

    if request.method == "POST":
        last_created_pokemon = list(mongo.db.pokemon.find().sort("dex_id", pymongo.DESCENDING).limit(1))
        dex_id = last_created_pokemon[0]['dex_id'] + 1
        new_pokemon = {
            "name": request.form.get("name").lower(),
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
            "created_by": user['username'],
            "rating": 0,
            "in_squad": [],
            "rated_by": []
        }

        # prevent duplicate pokemon names
        pokemon_exists = mongo.db.pokemon.find_one({"name": new_pokemon['name']})
        if pokemon_exists:
            flash(new_pokemon['name'].upper() + " already exists!")
            return render_template("preview_contribute.html", pokemon=new_pokemon, trainer_name=trainer_name, types=types)

        # prevent duplicate types
        if new_pokemon['type'][0] == new_pokemon['type'][1]:
            flash("Pokemon cannot have two identical types.")
            return render_template("preview_contribute.html", pokemon=new_pokemon, trainer_name=trainer_name, types=types)

        # create new record
        mongo.db.pokemon.insert_one(new_pokemon)
        flash(user['name'] + " discovered " + new_pokemon['name'].upper() + "!")
        return redirect(url_for('profile', username=session['user']))

    else:
        # object used to populate blank pokemon preview
        null_pokemon = {
            "name": "NAME",
            "dex_id": 0,
            "type": [
                "TYPE 1",
                "TYPE 2",
            ],
            "species": "SPECIES",
            "height": [
                0,
                0,
            ],
            "weight": 0,
            "desc": "POKEDEX TEXT ENTRY",
            "img_src": "https://i.pinimg.com/originals/95/d5/cd/95d5cded00f3a3e8a98fb1eed568aa9f.png",
            "created_by": session['user'],
            "rating": 0,
            "in_squad": [],
            "rated_by": []
        }
        return render_template("contribute.html", pokemon=null_pokemon, trainer_name=trainer_name, types=types)


@app.route("/preview_contribute/", methods=["GET", "POST"])
def preview_contribute():
    # get user info from db
    user = mongo.db.trainers.find_one(
        {"username": session['user']})
    trainer_name = user['name']

    if request.method == "POST":
        last_created_pokemon = list(mongo.db.pokemon.find().sort("dex_id", pymongo.DESCENDING).limit(1))
        dex_id = last_created_pokemon[0]['dex_id'] + 1
        preview = {
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
            "created_by": session['user'],
            "rating": 0,
            "in_squad": [],
            "rated_by": []
        }
        # print(preview)
        return render_template("preview_contribute.html", pokemon=preview, trainer_name=trainer_name, types=types)
    else:
        return


@app.route("/trainers")
def trainers():
    # get pokedex
    pokedex = list(mongo.db.pokemon.find())
    # get trainers
    trainers = mongo.db.trainers.find()
    return render_template("trainers.html", trainers=trainers, pokedex=pokedex, default_img=default_img_p)


@app.route("/trainers/<id>")
def get_selected_trainer(id):
    # get pokedex
    pokedex = list(mongo.db.pokemon.find())
    # get trainers
    trainers = mongo.db.trainers.find()
    return render_template("trainers.html", trainers=trainers, pokedex=pokedex, default_img=default_img_p, anchor=id)


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


# Main
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
