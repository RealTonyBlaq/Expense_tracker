#!/usr/bin/python3
""" Expense Tracker Flask App """

from api.v1 import ETapp
from dotenv import load_dotenv, find_dotenv
from flask import (abort, Flask, jsonify, request,
                   render_template, send_from_directory, redirect)
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_current_user
from utilities import db
from models.user import User
from os import getenv, makedirs, path, scandir, remove
import signal
import sys


app_env = find_dotenv()
load_dotenv(app_env)

app = Flask(__name__,
            template_folder='../../web_flask/templates',
            static_folder='../../web_flask/static')


app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(getenv('JWT_TOKEN_EXPIRES'))
app.config['JWT_ACCESS_CSRF_COOKIE_NAME'] = getenv('JWT_CSRF_COOKIE_NAME')
app.config['JWT_ACCESS_COOKIE_NAME'] = getenv('JWT_ACCESS_COOKIE_NAME')
app.config['SECURITY_PASSWORD_SALT'] = getenv('SECURITY_PASSWORD_SALT')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['JWT_COOKIE_HTTPONLY'] = False
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_SAMESITE'] = None
app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
file_folder = getenv('UPLOADS_FOLDER', 'uploads')
UPLOAD_FOLDER = path.join(path.dirname(path.abspath(__file__)), file_folder)
app.config['UPLOADS_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 7 * 1024 * 1024
app.config['TABSCANNER_API_KEY'] = getenv('TABSCANNER_API_KEY')

makedirs(app.config['UPLOADS_FOLDER'], exist_ok=True)
makedirs(f'{app.config["UPLOADS_FOLDER"]}/profile_pictures', exist_ok=True)
makedirs(f'{app.config["UPLOADS_FOLDER"]}/receipts', exist_ok=True)

app.register_blueprint(ETapp)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}},
     supports_credentials=True)
jwt = JWTManager(app)
ALLOWED_PICTURE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_RECEIPT_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}


def sig_handler(sig, frame):
    """ Handles SIGINT """
    for user in db.all(User).values():
        user.is_logged_in = False
        db.add(user)

    db.save()
    db.close()
    sys.exit(0)


def allowed_picture(filename: str) -> bool:
    """ Validates an uploaded picture """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_PICTURE_EXTENSIONS


def allowed_receipt(filename: str) -> bool:
    """ Validates an upoladed receipt """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_RECEIPT_EXTENSIONS


@jwt.user_lookup_loader
def user_obj_loader(jwt_header, jwt_data: dict):
    """ Loads the user object using the email parsed in the JWT"""
    email = jwt_data['sub']
    return db.query(User).filter_by(email=email).first()


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
    return jsonify(error='Not Found'), 404


@app.errorhandler(401)
def unauthorized(error):
    """ Returns a JSON if a request was unauthorized """
    return jsonify(message='user not logged in'), 401


@app.route('/api/stats', strict_slashes=False)
def stats():
    """ Returns a count of User, Category and Expense objects """
    return jsonify(users=len(db.all(User)),
                   online_users=len(db.query(User).filter_by(
                       is_logged_in=True).all())), 200


@app.route('/support', strict_slashes=False)
def support():
    """ Redirects to their mail where they can send complaints """
    return redirect(f'mailto:{app.config["MAIL_DEFAULT_SENDER"]}')


@app.route('/api/v1/avatar', methods=['GET', 'POST', 'DELETE'],
           strict_slashes=False)
@jwt_required()
def post_profile_picture():
    """
    Handles Picture upload

    /GET - Returns the User's picture
    /POST - Uploads a User's picture to the server
    /DELETE - Deletes any saved picture of the User
    """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.method == 'GET':
        file_prefix = f'User{current_user.id}'
        files = [f.name for f in scandir(f'{app.config["UPLOADS_FOLDER"]}/profile_pictures')
                 if f.is_file() and f.name.startswith(file_prefix)]

        if len(files) == 0:
            abort(404)
        return send_from_directory(f'{app.config["UPLOADS_FOLDER"]}/profile_pictures', files[0])

    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify(message='No image found in the request'), 400

        file = request.files['image']
        if not file or file.filename == '':
            return jsonify(message='No file selected'), 400

        if allowed_picture(file.filename):
            # check for previous uploaded picture and delete it
            file_prefix = f'User{current_user.id}'
            for f in scandir(f'{app.config["UPLOADS_FOLDER"]}/profile_pictures'):
                if f.is_file() and f.name.startswith(file_prefix):
                    remove(path.join(f'{app.config["UPLOADS_FOLDER"]}/profile_pictures', f.name))

            # Save the picture to the server
            file_ext = file.filename.rsplit('.', 1)[1]
            filename = f'User{current_user.id}.{file_ext}'
            filepath = path.join(f'{app.config["UPLOADS_FOLDER"]}/profile_pictures', filename)
            file.save(filepath)
            return jsonify(message='image upload successful!'), 201

        return jsonify(message='File type not allowed'), 400

    if request.method == 'DELETE':
        file_prefix = f'User{current_user.id}'
        for f in scandir(f'{app.config["UPLOADS_FOLDER"]}/profile_pictures'):
            if f.is_file() and f.name.startswith(file_prefix):
                remove(path.join(f'{app.config["UPLOADS_FOLDER"]}/profile_pictures', f.name))

        return jsonify(message='success'), 200


@app.route('/scan-receipt', methods=['POST'],
             strict_slashes=False)
@jwt_required()
def scan_receipt():
    """
    POST /scan-receipt
        scans receipts and creates an Expense object
        with the scanned values
    """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if 'image' not in request.files:
        return jsonify(message='No image found in the request'), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify(message='No file selected'), 400

    filepath = path.join(f'{app.config["UPLOADS_FOLDER"]}/receipts', file.filename)
    file.save(filepath)

    UPLOAD_URL = "https://api.tabscanner.com/api/process"
    RESULT_URL_TEMPLATE = "https://api.tabscanner.com/api/result/{}"

    receipt = {"file": open()}

@app.route('/', strict_slashes=False)
def index():
    """ Returns the home page """
    return render_template('home.html')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sig_handler)
    app.run(host='0.0.0.0', port=5000, debug=True)
