from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """Configuartion of available languages
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTF"

app.config.from_object(Config)

babel = Babel(app)

@babel.localeselector
def get_locale():
    """To determine the best match with our supported languages
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route("/", strict_slashes=False)
def hello_world():
    """Dipslay hello world
    """
    return render_template("3-index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)