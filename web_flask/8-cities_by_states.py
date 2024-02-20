#!/usr/bin/python3
"""
A python web app that prints all states in DB
"""
from flask import Flask, render_template
from markupsafe import escape
import models
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def route_cities_state():
    """
    Handles request for /state_list
    """
    all_states = models.storage.all(State).values()
    return render_template('8-cities_by_states.html', states=all_states)


@app.teardown_appcontext
def manage_context(exc):
    """
    Reloads new data from DB
    """
    models.storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
