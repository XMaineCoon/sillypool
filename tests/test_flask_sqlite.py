import sqlite3
from flask import g, app
from flask import Flask

DATABASES = '/data/database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASES)
    return db

app = Flask()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    cur = get_db().cursor()


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0]))