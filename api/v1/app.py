#!/usr/bin/python3
""" Expense Tracker Flask App """

from api.v1 import ETapp
from dotenv import load_dotenv, find_dotenv
from flask import Flask, g, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.expense import Expense
from utilities import db
from models.user import User
from os import getenv
import signal
import sys


app_env = find_dotenv()
load_dotenv(app_env)


app = Flask(__name__,
            template_folder='../../web_flask/templates',
            static_folder='../../web_flask/static')


app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(getenv('JWT_ACCESS_TOKEN_EXPIRES'))
app.config['JWT_ACCESS_CSRF_COOKIE_NAME'] = getenv('JWT_ACCESS_CSRF_COOKIE_NAME')
app.config['JWT_ACCESS_COOKIE_NAME'] = getenv('JWT_ACCESS_COOKIE_NAME')
app.config['SECURITY_PASSWORD_SALT'] = getenv('SECURITY_PASSWORD_SALT')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['JWT_COOKIE_HTTPONLY'] = True
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
app.config['JWT_COOKIE_CSRF_PROTECT'] = True


app.register_blueprint(ETapp)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}}, supports_credentials=True)
jwt = JWTManager(app)


def sig_handler(sig, frame):
    """ Handles SIGINT """
    for user in db.all(User).values():
        user.is_logged_in = False
        db.add(user)

    db.save()
    db.close()
    sys.exit(0)


@jwt.user_lookup_loader
def user_obj_loader(jwt_header, jwt_data: dict):
    """ Loads the user object using the email parsed in the JWT"""
    email = jwt_data['sub']
    return db.query(User).filter_by(email = email).first()


@jwt.user_identity_loader
def load_user(user):
    """ Loads the user and returns the id """
    return user.email


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """ Handles expired tokens """
    return jsonify(
        message='The token has expired',
        error='token_expired'
    ), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """ Handle invalid tokens """
    return jsonify(
        message='Invalid token',
        error='invalid_token'
    ), 422


@jwt.unauthorized_loader
def missing_token_callback(error):
    """ Handle missing tokens """
    return jsonify(
        message='Token is missing',
        error='authorization_required'
    ), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """ Handles revoked tokens """
    return jsonify(
        message='Token has been revoked',
        error='token_revoked'
    ), 401


@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    db.close()


@app.errorhandler(404)
def not_found(error):
    """ Returns a JSON if a request route was not found """
    return jsonify(error='Not Found')


@app.errorhandler(401)
def unauthorized(error):
    """ Returns a JSON if a request was unauthorized """
    return jsonify(message='user not logged in')


@app.route('/api/stats', strict_slashes=False)
def stats():
    """ Returns a count of User, Category and Expense objects """
    return jsonify(users=len(db.all(User)),
                   online_users=len(db.query(User).filter_by(is_logged_in = True).all())), 200


@app.route('/', strict_slashes=False)
def index():
    """ Returns the home page """
    return render_template('home.html')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sig_handler)
    app.run(host='0.0.0.0', port=5000, debug=True)
