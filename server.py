from re import T
from flask_app import app
from flask_app.controllers import recipes_controller, users_controller  # Controladores


if(__name__ == "__main__"):
    app.run(debug=True)
