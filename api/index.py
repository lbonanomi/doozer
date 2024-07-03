import os
from time import strftime, localtime
import json
from flask import Flask
import psycopg2


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
    sql.execute("SELECT DISTINCT(patch), authority, kb FROM windows WHERE release = '{release}' ORDER BY patch DESC".format(release = version))

    latest_patch = sql.fetchone()
    latest_patch_number = latest_patch[0]   # Bold of you to beta the latest patch
    latest_patch_authority = latest_patch[1]
    latest_patch_kb = latest_patch[2].replace("KB", "https://support.microsoft.com/help/")
    
    stable_patch = sql.fetchone()
    stable_patch_number = stable_patch[0]   # What most sensible folks deploy
    stable_patch_authority = stable_patch[1]
    stable_patch_kb = stable_patch[2] #.replace("KB", "https://support.microsoft.com/help/")
    
    prior_patch = sql.fetchone()
    prior_patch_number = prior_patch[0]    # Acceptable for-now
    prior_patch_authority = prior_patch[1]
    prior_patch_kb = prior_patch[2] #.replace("KB", "https://support.microsoft.com/help/")
    

    sql.close()
    connection.close()

    #result = { "release":version, "latest_patch":latest_patch_number, "stable_patch":stable_patch_number, "previous_patch":prior_patch_number, "authority": latest_patch_authority  }
    result = { 
        "release":version, 
        "latest": { "patch_number": latest_patch_number, "authority": latest_patch_authority, "kb": latest_patch_kb }, 
        "stable": { "patch_number": stable_patch_number, "authority": stable_patch_authority, "kb": stable_patch_kb }, 
        "previous": { "patch_number": prior_patch_number, "authority": prior_patch_authority, "kb": prior_patch_kb } 
    }

    return json.dumps(result) + "\n"
