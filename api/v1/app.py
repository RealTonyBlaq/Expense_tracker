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


app_env = find_dotenv()
load_dotenv(app_env)


app = Flask(__name__,
            template_folder='../../web_flask/templates',
            static_folder='../../web_flask/static')


app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = getenv('JWT_TOKEN_LOCATION')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(getenv('JWT_ACCESS_TOKEN_EXPIRES'))
app.config['JWT_ACCESS_CSRF_COOKIE_NAME'] = getenv('JWT_ACCESS_CSRF_COOKIE_NAME')
app.config['JWT_ACCESS_COOKIE_NAME'] = getenv('JWT_ACCESS_COOKIE_NAME')
app.config['SECURITY_PASSWORD_SALT'] = getenv('SECURITY_PASSWORD_SALT')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['JWT_COOKIE_HTTPONLY'] = True
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')


app.register_blueprint(ETapp)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}}, supports_credentials=True)
jwt = JWTManager(app)


@jwt.user_lookup_loader
def user_obj_loader(jwt_header, jwt_data: dict):
    """ Loads the user object using the email parsed in the JWT"""
    email = jwt_data['sub']
    return db.query(User).filter_by(email = email).first()


# Handle expired tokens
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'msg': 'The token has expired',
        'error': 'token_expired'
    }), 401

# Handle invalid tokens
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'msg': 'Invalid token',
        'error': 'invalid_token'
    }), 422

# Handle missing tokens
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'msg': 'Token is missing',
        'error': 'authorization_required'
    }), 401

# Handle revoked tokens (if using token blacklisting)
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'msg': 'Token has been revoked',
        'error': 'token_revoked'
    }), 401


@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    db.close()


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
