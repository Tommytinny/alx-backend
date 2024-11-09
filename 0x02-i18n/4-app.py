#!/usr/bin/env python3
"""Flask app
"""

from flask import Flask, render_template, request
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


@babel.localeselector
def get_locale()-> str:
    """To determine the best match with our supported languages
    """
    if 'locale' in request.args:
        if request.args.get('local') == 'en':
            return 'en'
        if request.args.get('locale') == 'fr':
            return 'fr'
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/", strict_slashes=False)
def hello_world()-> str:
    """Dipslay hello world
    """
    return render_template("4-index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
