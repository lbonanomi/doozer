import os
from time import strftime, localtime
import json
from flask import Flask
import psycopg2-binary


pages = ["https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information", "https://learn.microsoft.com/en-us/windows/release-health/release-information"]


connection = psycopg2.connect(
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
def latest(version):
    sql = connection.cursor()
    sql.execute("SELECT DISTINCT(patch) FROM windows WHERE release = '{release}' ORDER BY patch DESC".format(release = version))

    latest_patch = sql.fetchone()[0]   # Bold of you to beta the latest patch
    stable_patch = sql.fetchone()[0]   # What most sensible folks deploy
    prior_patch = sql.fetchone()[0]    # Acceptable for-now
    authority = sql.fetchone()[0]      # Who says
    
    sql.close()
    connection.close()

    result = { "release":version, "latest_patch":latest_patch, "stable_patch":stable_patch, "previous_patch":prior_patch, "authority": authority  }

    return json.dumps(result) + "\n"
