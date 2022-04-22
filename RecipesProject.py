import csv
import os
from flask import Flask, render_template, request, redirect, url_for

#cd Flask
#venv\Scripts\activate
#$env:FLASK_APP = "RecipesProject"
# $env:FLASK_ENV = "development"
#flask run

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/photos")
def photos():

    recipe_images = []
    with open("recipes.csv", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            recipe_images.append(row) # recipe_images = []

    return render_template("photos.html", recipe_images=recipe_images)


app.config["UPLOAD_PATH"] = "static/images"
@app.route('/upload', methods=["GET", "POST"])
def file_upload():
    if request.method == "GET":
        return render_template("image_upload.html")
    recipe_name = request.form.get("recipe_name")
    ingredients = request.form.get("ingredients")
    prep_time = request.form.get("prep_time")


    print(recipe_name)
    uploaded_file = request.files["recipe_image"]
    if uploaded_file.filename != "":
        uploaded_file.save(os.path.join(app.config["UPLOAD_PATH"], uploaded_file.filename))
        recipe_list = []
        with open("recipes.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                recipe_list.append(row)
        recipe_list.append([uploaded_file.filename, recipe_name, ingredients, prep_time])
        with open("recipes.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(recipe_list)
    return redirect(url_for("photos"))

@app.route("/remove-recipe")
def remove_recipe_page():
    recipe_list = []
    with open("recipes.csv", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            recipe_list.append(row)

    return render_template("remove.html", recipe_list=recipe_list)


@app.route("/delete/<recipe>")
def delete(recipe):
    recipe_list = []
    with open("recipes.csv", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            recipe_list.append(row)
    for food in recipe_list:
        if food[1] == recipe:
            recipe_list.remove(food)
            with open("recipes.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(recipe_list)
    return redirect(url_for("main_page"))

