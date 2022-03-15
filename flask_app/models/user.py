from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:

    def __init__(self, data: dict):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data: dict):
        query = "INSERT INTO recetas.users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        nuevoId = connectToMySQL("recetas").query_db(query, data)
        return nuevoId

    @staticmethod
    def validaUsuario(user):
        valid = True
        if(len(user["first_name"]) < 2):
            flash("Nombre debe se de almenos 2 caracteres", "register")
            valid = False
        if(len(user["last_name"]) < 2):
            flash("Apellido debe se de almenos 2 caracteres", "register")
            valid = False

        if(not EMAIL_REGEX.match(user["email"])):
            flash("Email inválido", "register")
            valid = False
        if(len(user["password"]) < 8):
            flash("La contraseña debe se de almenos 8 caracteres", "register")
            valid = False

        if(user["password"] != user["confirm"]):
            flash("La contraseña no coincide", "register")
            valid = False

        query = "SELECT * FROM recetas.users WHERE email = %(email)s"
        result = connectToMySQL("recetas").query_db(query, user)

        if(len(result) > 0):
            flash("El e-mail ya está en uso", "register")
            valid = False
        return valid

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recetas.users WHERE id = %(id)s;"
        result = connectToMySQL("recetas").query_db(query, data)
        usr = result[0]
        user = cls(usr)
        return user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM recetas.users WHERE email = %(email)s;"
        result = connectToMySQL("recetas").query_db(query, data)
        if(len(result) < 1):
            return False
        else:
            usr = result[0]
            user = cls(usr)
            return user

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM recetas.users"
        results = connectToMySQL("recetas").query_db(query)
        usuarios = []
        for x in results:
            usuarios.append(cls(x))
        return usuarios
