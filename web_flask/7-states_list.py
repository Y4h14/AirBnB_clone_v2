#!/usr/bin/python3
from models import storage
from flask import Flask, render_template
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    return render_template('7-states_list.html',
                           result=storage.all(State))




if __name__ == '__main__':
    app.run(host='0.0.0.0')