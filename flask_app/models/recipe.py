from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:

    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.under30 = data["under30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.user_id = data["user_id"]

    @staticmethod
    def valida_receta(recipe):
        valid = True
        if(len(recipe["name"]) < 3):
            flash("Nombre debe ser de almenos 3 caracteres", "receta")
            valid = False
        if(len(recipe["description"]) < 3):
            flash("Description debe ser de almenos 3 caracteres", "receta")
            valid = False
        if(len(recipe["instructions"]) < 3):
            flash("Instruction debe ser de almenos 3 caracteres", "receta")
            valid = False
        if(recipe["date_made"] == ""):
            flash("Seleccione una fecha", "receta")
            valid = False

        if("under30" not in recipe):
            flash("Seleccione una opción de duración", "receta")
        return valid

    @classmethod
    def save(cls, form: dict):
        query = "INSERT INTO recetas.recipes (name, description, instructions, date_made, under30, user_id ) "\
                "VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under30)s,%(user_id)s)"
        result = connectToMySQL("recetas").query_db(query, form)
        return result

    @classmethod
    def update(cls, form: dict):
        query = "UPDATE recetas.recipes "\
            "SET name= %(name)s, description = %(description)s, instructions= %(instructions)s, date_made= %(date_made)s, under30=%(under30)s "\
            "WHERE id= %(id)s"
        result = connectToMySQL("recetas").query_db(query, form)
        return result

    @classmethod
    def delete(cls, form: dict):
        query = "DELETE FROM recetas.recipes WHERE recipes.id= %(id)s"
        result = connectToMySQL("recetas").query_db(query, form)
        return result

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM recetas.recipes"
        results = connectToMySQL("recetas").query_db(query)
        recipes = []
        for x in results:
            recipes.append(cls(x))
        return recipes

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recetas.recipes WHERE id = %(id)s;"
        result = connectToMySQL("recetas").query_db(query, data)
        rcp = result[0]
        recipe = cls(rcp)
        return recipe
