#!/usr/bin/python3
"""
a script that starts a Flask web application
"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def route_root():
    """
    Handles request to /
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def route_hbnb():
    """
    Handles request to /hbnb
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def route_c(text):
    """
    Handles request to /c/{text}
    """
    text = text.replace('_', ' ')
    return f"C {escape(text)}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
