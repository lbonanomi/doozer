import json
import os
from time import strftime, localtime
from flask import Flask, jsonify
import psycopg2


pages = ["https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information", "https://learn.microsoft.com/en-us/windows/release-health/release-information"]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    usage = """
    <p>This is an appliance that digests the tables of Windows patch version information on """ + " and ".join(pages) + """ and converts them into a RESTful query endpoint</p>
    <p>Why not try it?</p> 
    <ul>
    <li><a href="/latest/19044">/latest/19044</a> for the latest-minus-one patch version for Windows 10 Release 21H2</li>
    <li><a href="/latest/19045">/latest/19045</a> for the latest-minus-one patch version for Windows 10 Release 22H2</li>
    <li><a href="/latest/22631">/latest/22621</a> for the latest-minus-one patch version for Windows 11 Release 22H2</li>
    <li><a href="/latest/22631">/latest/22631</a> for the latest-minus-one patch version for Windows 11 Release 23H2</li>
    </ul>
    <br><br>"""

    return usage

@app.route('/latest/<version>', methods=['GET'])
def latest(version):
    connection = psycopg2.connect(
        host = os.environ['POSTGRES_HOST'],
        user = os.environ['POSTGRES_USER'],
        password = os.environ['POSTGRES_PASSWORD'],
        database = os.environ['POSTGRES_DATABASE'],
        port = 5432
    )
    
    sql = connection.cursor()
    sql.execute("SELECT DISTINCT(patch), authority, kb FROM windows WHERE release = '{release}' ORDER BY patch DESC".format(release = version))

    latest_patch = sql.fetchone()
    latest_patch_number = latest_patch[0]   # Bold of you to beta the latest patch
    latest_patch_authority = latest_patch[1]
    latest_patch_kb = latest_patch[2].replace("KB", "https://support.microsoft.com/help/")
    
    stable_patch = sql.fetchone()
    stable_patch_number = stable_patch[0]   # What most sensible folks deploy
    stable_patch_authority = stable_patch[1]
    stable_patch_kb = stable_patch[2].replace("KB", "https://support.microsoft.com/help/")
    
    prior_patch = sql.fetchone()
    prior_patch_number = prior_patch[0]    # Acceptable for-now
    prior_patch_authority = prior_patch[1]
    prior_patch_kb = prior_patch[2].replace("KB", "https://support.microsoft.com/help/")
    

    sql.close()
    connection.close()

    #result = { "release":version, "latest_patch":latest_patch_number, "stable_patch":stable_patch_number, "previous_patch":prior_patch_number, "authority": latest_patch_authority  }
    
    result = { 
        "release":version, 
        "latest": { "patch_number": latest_patch_number, "authority": latest_patch_authority, "kb": latest_patch_kb }, 
        "stable": { "patch_number": stable_patch_number, "authority": stable_patch_authority, "kb": stable_patch_kb }, 
        "previous": { "patch_number": prior_patch_number, "authority": prior_patch_authority, "kb": prior_patch_kb } 
    }

    return jsonify(result) 
