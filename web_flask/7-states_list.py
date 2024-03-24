#!/usr/bin/python3
"""
A python web app that prints all states in DB
"""
from flask import Flask, render_template
from markupsafe import escape
import models

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def route_state_list():
    """
    Handles request for /state_list
    """
    all_states = models.storage.all(models.state.State).values()
    all_states = sorted(all_states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=all_states)


@app.teardown_appcontext
def manage_context(exc):
    """
    Reloads new data from DB
    """
    models.storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
