from flask import Flask, render_template, redirect, session, flash, request
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route("/new/recipe")
def new_recipe():
    if("user_id" not in session):
        return redirect("/")

    data = {"id": session["user_id"]}

    user = User.get_by_id(data)

    return render_template("new_recipe.html", user=user)


@app.route("/create/recipe", methods=["POST"])
def create_recipe():
    print(request.form)
    if("user_id" not in session):
        return redirect("/")

    if(not Recipe.valida_receta(request.form)):
        return redirect("/new/recipe/")

    Recipe.save(request.form)
    return redirect("/dashboard")


@app.route("/edit/recipe/<int:id>")
def edit_recipe(id):

    if("user_id" not in session):
        return redirect("/")

    data = {"id": session["user_id"]}
    user = User.get_by_id(data)

    data_recipe = {"id": id}
    recipe = Recipe.get_by_id(data_recipe)
    print(type(recipe.date_made))
    date = str(recipe.date_made).split(" ")[0]
    print(date)

    if(session["user_id"] != recipe.user_id):
        return redirect("/")

    return render_template("edit_recipe.html", user=user, recipe=recipe, date=date)


@app.route("/update/recipe", methods=["POST"])
def update_recipe():
    print(request.form)
    if("user_id" not in session):
        return redirect("/")

    if(not Recipe.valida_receta(request.form)):
        return redirect("/edit/recipe/"+request.form["id"])

    Recipe.update(request.form)
    return redirect("/dashboard")


@app.route("/show/recipe/<int:id>")
def show_recipe(id):
    if("user_id" not in session):
        return redirect("/")

    data = {"id": session["user_id"]}
    user = User.get_by_id(data)

    data_recipe = {"id": id}
    recipe = Recipe.get_by_id(data_recipe)
    print(recipe)
    print(type(recipe))

    return render_template("show_recipe.html", user=user,recipe=recipe)


@app.route("/delete/recipe/<int:id>")
def delete_recipe(id):
    if("user_id" not in session):
        return redirect("/")

    data = {"id": session["user_id"]}
    user = User.get_by_id(data)

    data_recipe = {"id": id}
    Recipe.delete(data_recipe)

    return redirect("/dashboard")