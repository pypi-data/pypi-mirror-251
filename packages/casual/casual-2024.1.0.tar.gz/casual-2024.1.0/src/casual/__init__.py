from flask import Flask, render_template


def create_app():
    """Application Factory

    Returns:
        app: The Application
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Entry point into the app"""

        return render_template("index.html.j2")

    return app
