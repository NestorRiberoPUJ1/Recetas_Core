from datetime import date, datetime
import bcrypt
from flask import Flask, render_template, redirect, session, flash, request
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    if (not User.validaUsuario(request.form)):
        return redirect("/")
    pwd = bcrypt.generate_password_hash(request.form["password"])

    formulario = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pwd
    }
    id = User.save(formulario)

    session["user_id"] = id
    return redirect("/dashboard")


@app.route("/login", methods=["POST"])
def login():
    user = User.get_by_email(request.form)

    if(not user):
        flash("Email no encontrado", "login")
        return redirect("/")

    if(not bcrypt.check_password_hash(user.password, request.form["password"])):
        flash("Contraseña incorrecta", "login")
        return redirect("/")

    session["user_id"] = user.id

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if("user_id" not in session):
        return redirect("/")

    data = {"id": session["user_id"]}

    user = User.get_by_id(data)
    recipes = Recipe.getAll()
    hour="2022-08-03 8:00:00"

    return render_template("dashboard.html", user=user, recipes=recipes,hour=hour)
