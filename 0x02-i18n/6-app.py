#!/usr/bin/env python3
""" Flask app
"""

from typing import Union
from flask import Flask, render_template, g, request
from flask_babel import Babel


class Config:
    """Configuartion of available languages
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTF"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale()-> str:
    """To determine the best match with our supported languages
    """
    if 'locale' in request.args:
        locale = request.args.get('locale')
        if locale == 'en' or locale == 'fr':
            return locale

    if g.user:
        return g.user["locale"]

    if request.accept_languages:
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    else:
        return app.config['BABEL_DEFAULT_LOCALE']


def get_user()-> Union[str, None]:
    """get user function
    """
    if 'login_as' in request.args:
        for key, value in users.items():
            if key == int(request.args.get('login_as')):
                return value
        return None
    return None


@app.before_request
def before_request()-> None:
    """Before request fucntion
    """
    g.user = get_user()


@app.route('/', strict_slashes=False)
def hello_world()-> str:
    """Dipslay hello world
    """
    if g.user:
        username = g.user["name"]
        return render_template("6-index.html", username=username)
    return render_template("6-index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
