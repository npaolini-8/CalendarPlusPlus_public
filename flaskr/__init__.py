from flask import Flask
import os


def create_app():
    """
    Application factory for Flask, see
    https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/
    """
    flask = Flask(__name__)
    flask.config['SECRET_KEY'] = "1a19f9414df3b48c05b67702b5cf7fffdff6964e"
    flask.config['TMP'] = os.path.join(os.getcwd(), "flaskr", "static", "tmp")

    # initialize core blueprints/routes second
    from . import views
    views.init_app(flask)

    return flask
