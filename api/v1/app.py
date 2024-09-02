#!/usr/bin/python3
""" Expense Tracker Flask App """

from api.v1 import ETapp
from dotenv import load_dotenv, find_dotenv
from flask import Flask, g, jsonify, render_template
from flask_cors import CORS
from flask_login import LoginManager, user_loaded_from_request
from flask.sessions import SecureCookieSessionInterface
from models.expense import Expense
from utilities import db
from models.user import User
from os import getenv


app_env = find_dotenv()
load_dotenv(app_env)

app = Flask(__name__,
            template_folder='../../web_flask/templates',
            static_folder='../../web_flask/static')

app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = getenv('SECURITY_PASSWORD_SALT')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')

login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(ETapp)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}}, supports_credentials=True)


@user_loaded_from_request.connect
def user_loaded_from_request(app, user=None):
    """
    sets the login_via_request variable to true
    """
    g.login_via_request = True


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_request'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)


app.session_interface = CustomSessionInterface()


@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    db.close()


@login_manager.user_loader
def load_user(user_id):
    """ Loads the user object """
    try:
        user = db.find(User, user_id)
        return user
    except (ValueError, TypeError):
        return None


@login_manager.unauthorized_handler
def null_user():
    """Returns null"""
    return jsonify({'message': 'user not authenticated'}), 401


@app.errorhandler(404)
def not_found(error):
    """ Returns a JSON if a request route was not found """
    return jsonify({'error': 'Not Found'})


@app.route('/api/stats', strict_slashes=False)
def stats():
    """ Returns a count of User, Category and Expense objects """
    obj_stats = {'users': len(db.all(User))}
    return jsonify(obj_stats), 200


@app.route('/', strict_slashes=False)
def index():
    """ Returns the home page """
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
