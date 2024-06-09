#!/usr/bin/python3
""" Expense Tracker Flask app """

from flask import Flask, jsonify, redirect, request, render_template, url_for
from flask_cors import CORS
from api import ETapp
from models import storage
from models.category import Category
from models.expense import Expense
from models.user import User, confirm_account, check_string


app = Flask(__name__)
app.register_blueprint(ETapp)
app.static_folder = 'static'
CORS(app)


@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Returns a JSON if a request route wasn't found """
    return jsonify({'error': 'Not Found'})


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    return render_template('home.html')


@app.route('/reset')
def reset_password():
    """ Returns the reset password page """
    return render_template('home.html')


@app.route('/dashboard', methods=['GET', 'POST'], strict_slashes=False)
def dashboard():
    """ Handles dashboard view and salary submission """
    # if not g.user:
    #    return redirect(url_for('signin'))

    user_id = request.args.get('u')
    return render_template('dashboard.html')

    # return render_template('dashboard.html', salary=g.user.salary)


@app.route('/signup', methods=['POST', 'GET'], strict_slashes=False)
def signup():
    """ Handles the case when the user clicks on submit """
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')

        # Add validation for input data here

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        new = User(**data)
        new.save()
        return render_template('signin.html',
                               success="Account created successfully")

    return render_template('create.html')


@app.route('/signin', methods=['POST', 'GET'], strict_slashes=False)
def signin():
    """ Confirms a User's details and logs them in to their dashboard """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = confirm_account(email, password)
        if user:
            # g.user = user.details()
            return redirect(url_for('dashboard', u=user.id))
        return render_template('signin.html',
                               error='Incorrect email/password. \
                                   Please try again!')

    return render_template('signin.html')


if __name__ == "__main__":
    app.run(debug=True)
