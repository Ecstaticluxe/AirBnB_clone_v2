#!/usr/bin/python3
"""
A python web app that prints all states in DB
"""
from flask import Flask, render_template
from markupsafe import escape
import models
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def route_states():
    """
    Handles request for /state_list
    """
    all_states = models.storage.all(State).values()
    return render_template('9-states.html', states=all_states, cities=None)


@app.route('/states/<id>', strict_slashes=False)
def route_state_id(id):
    states = models.storage.all(State).values()
    for state in states:
        if id == state.id:
            return render_template('9-states.html', states=state,
                                   cities=state.cities)
    return render_template('9-states.html', states=None, cities=None)


@app.teardown_appcontext
def manage_context(exc):
    """
    Reloads new data from DB
    """
    models.storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
