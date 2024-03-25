#!/usr/bin/python3
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def appcontext_teardown(exc=None):
    """resetting storage"""
    storage.close


@app.route('/hbnb_filters')
def filters():
    """
    renders the filter page of the clone
    """
    states = storage.all('State').values()
    amenity = storage.all('Amenity').values()
    return render_template("10-hbnb_filters.html",
                           states=states, amenity=amenity)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
