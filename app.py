import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


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
