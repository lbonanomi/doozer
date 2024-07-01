import os
from time import strftime, localtime
import json
from flask import Flask
#import requests
#from bs4 import BeautifulSoup
import pg8000.dbapi


pages = ["https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information", "https://learn.microsoft.com/en-us/windows/release-health/release-information"]


connection = pg8000.dbapi.Connection(
    host = os.environ['POSTGRES_HOST'],
    user = os.environ['POSTGRES_USER'],
    password = os.environ['POSTGRES_PASSWORD'],
    database = os.environ['POSTGRES_DATABASE'],
    port = 5432
)


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'


@app.route('/latest/<version>', methods=['GET'])
def latest(connection, version):
    connection = pg8000.dbapi.Connection(
        host = os.environ['POSTGRES_HOST'],
        user = os.environ['POSTGRES_USER'],
        password = os.environ['POSTGRES_PASSWORD'],
        database = os.environ['POSTGRES_DATABASE'],
        port = 5432
    )

    sql = connection.cursor()
    sql.execute("SELECT DISTINCT(patch) FROM windows WHERE release = '{release}' ORDER BY patch DESC".format(release = version))

    throwaway = sql.fetchone()[0]   # Requirement is latest-minus-one
    latest_patch = sql.fetchone()[0]
    prior_patch = sql.fetchone()[0]
    
    
    connection.close()

    result = { "release":version, "latest_patch":latest_patch, "previous_patch":prior_patch, "previous_base":"10.0." + version + "." + prior_patch, "latest_base":"10.0." + version + "." + latest_patch  }

    return json.dumps(result) + "\n"
