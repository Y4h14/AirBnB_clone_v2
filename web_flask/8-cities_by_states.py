#!/usr/bin/python3
""" defines a flask app that run on localhost"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def appcontext_treatdown(exc=None):
    """
    this functions runs after each request regardless of weather
    an exception was raised or not.
    used for clean up
    """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def state_list():
    """return all states data"""
    states = storage.all("State")
    return render_template('8-cities_by_states.html',
                           states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
