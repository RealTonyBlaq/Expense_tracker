#!/usr/bin/env python3
""" Expense Tracker Flask app """

from auth.session import Auth
from flask import (abort, Flask, jsonify, make_response,
                   redirect, request,
                   render_template, url_for)
from flask_cors import CORS
from api import ETapp
import os
from models import storage


app = Flask(__name__)
app.register_blueprint(ETapp)
app.static_folder = 'static'
CORS(app, resources={r"/api/*": {"origins": "*"}})
auth = Auth()


@app.before_request
def before_all_requests() -> None:
    #Executed before all other requests
    if auth:
        if auth.require_auth(request.path, ['/api/*',
                                            '/static/*',
                                            '/reset/',
                                            '/signin/',
                                            '/signup/',
                                            '/',
                                            '/home/']):
            if not auth.session_cookie(request):
                abort(401)
            if not auth.current_user(request):
                abort(403)
            request.current_user = auth.current_user(request)

    
@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    storage.close()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Returns a JSON if a request route wasn't found """
    return jsonify({'error': 'Not Found'})


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Returns a JSON if the request wasn't authorized """
    return jsonify({'error': 'unauthorized'})


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Returns a JSON if the request is forbidden """
    return jsonify({'error': 'forbidden'})


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    return render_template('home.html')


@app.route('/reset')
def reset_password():
    """ Returns the reset password page """
    return render_template('reset.html')


@app.route('/dashboard', strict_slashes=False)
def dashboard():
    """ Handles dashboard view and salary submission """
    user = auth.current_user(request)
    if user:
        return render_template('dashboard.html')
    return redirect(url_for('home'))


@app.route('/signup', methods=['POST', 'GET'], strict_slashes=False)
def signup():
    """ Handles the case when the user clicks on submit """
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        auth.create_user(data)
        return render_template('signin.html',
                               success="Account created successfully")

    return render_template('create.html')


@app.route('/signin', methods=['POST', 'GET'], strict_slashes=False)
def signin():
    """ Confirms a User's details and logs them in to their dashboard """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if auth.validate(email, password):
            cookie = auth.create_session(email)
            response = make_response(redirect(url_for('dashboard')), 200)
            response.set_cookie('session_id', cookie)
            return response
        abort(401)

    return render_template('signin_page.html')


if __name__ == "__main__":
    app.run(debug=True)
