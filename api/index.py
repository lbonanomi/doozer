import os
from time import strftime, localtime
import json
from flask import Flask
import requests
from bs4 import BeautifulSoup
import pg8000

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'


@app.route('/latest/<version>', methods=['GET'])
def latest(version):
    con = sqlite3.connect('windows.db')
    cur = con.cursor()

    sql = cur.execute('SELECT DISTINCT(patch) FROM windows WHERE release = "{release}" ORDER BY CAST(patch AS INTEGER) DESC'.format(release = version))

    throwaway = sql.fetchone()[0]   # Requirement is latest-mnus-one
    latest_patch = sql.fetchone()[0]
    prior_patch = sql.fetchone()[0]

    result = { "release":version, "latest_patch":latest_patch, "previous_patch":prior_patch, "previous_base":"10.0." + version + "." + prior_patch, "latest_base":"10.0." + version + "." + latest_patch  }

    return json.dumps(result) + "\n"


@app.route('/about')
def about():
    return 'About'
