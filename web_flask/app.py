#!/usr/bin/python3

from flask import Flask, render_template


app = Flask(__name__, static_folder='static')


@app.route('/', strict_slashes=False)
def home() -> str:
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)
