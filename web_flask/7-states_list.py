#!/usr/bin/python3
""" defines a flask app that run on localhost"""
from models import storage
from flask import Flask, render_template
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def appcontext_treatdown(exc=None):
    """
    this functions runs after each request regardless of weather
    an exception was raised or not.
    used for clean up
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def state_list():
    """return all states data"""
    print(storage.all("State"))
    return render_template('7-states_list.html',
                           result=storage.all("State"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
