from flask import Flask


def create_app():
    """
    Application factory for Flask, see
    https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/
    """
    flask = Flask(__name__)

    # initialize core blueprints/routes second
    import views
    views.init_app(flask)

    return flask


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
