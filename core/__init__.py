from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    from .views import repo

    app.register_blueprint(repo.bp)

    return app
