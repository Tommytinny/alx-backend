from flask import Flask, render_template, g, request
from flask_babel import Babel, _
from pytz import timezone
import pytz.exceptions
from datetime import datetime
import locale

app = Flask(__name__)


class Config:
    """Configuartion of available languages
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)

babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

@babel.localeselector
def get_locale():
    """To determine the best match with our supported languages
    """
    if 'locale' in request.args:
        localee = request.args.get('locale')
        if localee == 'en' or localee == 'fr':
            return localee
        
    if g.user:
        return g.user["locale"]
    
    if request.accept_languages:
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    else:
        return app.config['BABEL_DEFAULT_LOCALE']
    

@babel.timezoneselector
def get_timezone():
    """get timezone function
    """
    if 'timezone' in request.args:
        timezn = request.args.get('timezone')
        try:
            return timezone(timezn).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user:
        try:
            timezn = g.user.get('timezone')
            return timezone(timezn).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    
    default_timezn = app.config['BABEL_DEFAULT_TIMEZONE']
    return default_timezn
        

def get_user():
    """get user function
    """
    if 'login_as' in request.args:
        for key, value in users.items():
            if key == int(request.args.get('login_as')):
                return value
        return None
    return None

@app.before_request        
def before_request():
    """Before request fucntion
    """
    g.user = get_user()
    
    time_now = pytz.utc.localize(datetime.utcnow())
    time = time_now.astimezone(timezone(get_timezone()))
    #locale.setlocale(locale.LC_TIME, (get_locale(), 'UTF-8'))
    time_format = "%b %d, %Y %I:%M:%S %p"
    g.time = time.strftime(time_format)

@app.route("/", strict_slashes=False)
def hello_world():
    """Dipslay hello world
    """
    current_time = g.time
    return render_template("index.html", current_time=current_time)


    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)