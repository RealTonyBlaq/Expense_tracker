#!/usr/bin/python3
from flask import Flask, render_template
app = Flask(__name__)

app.static_folder = 'static'


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template("create.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")



if __name__ == "__main__":
    app.run(debug=True)