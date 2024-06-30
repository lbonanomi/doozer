import os
from time import strftime, localtime
import json
from flask import Flask
import requests
from bs4 import BeautifulSoup
import pg8000.dbapi


pages = ["https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information", "https://learn.microsoft.com/en-us/windows/release-health/release-information"]


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'


def harvest(pages):
    """Drop existing definitions and reload from pages"""
    #con = sqlite3.connect('windows.db')
    #cur = con.cursor()

    con = pg8000.dbapi.Connection(
        host = os.environ['POSTGRES_HOST'],
        user = os.environ['POSTGRES_USER'],
        password = os.environ['POSTGRES_PASSWORD'],
        database = os.environ['POSTGRES_DATABASE'],
        port = 5432
    )

    sql = connection.cursor()
    
    #sql.execute("SELECT DISTINCT(patch) FROM windows WHERE release = '{release}' ORDER BY patch DESC".format(release = version))

    
    # Copy the existing table to a backup
    #
    #cur.execute("CREATE TABLE new AS SELECT * FROM windows WHERE 0")
    #
    #cur.execute("DELETE FROM windows") # NOT YET!

    for page in pages:
        data = requests.get(page, timeout=10).text

        soup = BeautifulSoup(data, 'html.parser')

        for table in soup.find_all('table'):

            rows = table.find_all('tr')

            for row in rows:
                columns = row.find_all('td')

                try:
                    svc_option = columns[0].text
                except IndexError:
                    continue

                try:
                    avail_date = columns[1].text
                except IndexError:
                    continue

                try:
                    build = columns[2].text

                    if "." in build:
                        (release, patch) = build.split(".")
                    else:
                        release = build
                        patch = ""

                except IndexError:
                    continue

                #cur = con.cursor()
                sql.execute("INSERT INTO windows VALUES ('{}', '{}', '{}', '{}')".format(svc_option, avail_date, release, patch))
                #con.commit()
    
    result = { "status":"ok", "msg":"Reloaded" }
    return json.dumps(result) + "\n"


    
    # WOOP WOOP TEST ONLY!!
    #cur.execute("delete from new where release = '10240'")

    # Now that table "new" is built, compare it with table "windows"
    #
    #sql_diff = cur.execute("select COUNT(DISTINCT patch) from windows where patch not in (SELECT patch FROM new)")
    #diff = sql_diff.fetchone()[0]
    #
    #sql_tot = cur.execute("select COUNT(PATCH) from windows")
    #total = sql_tot.fetchone()[0]
    #
    #pct = (diff * 100) / total
    #
    #print(str(pct), "% difference between stored and harvested versions")
    #
    #if pct > 2:
    #    cur = con.cursor()
    #    cur.execute("DROP TABLE new")
    #
    #    result = { "status":"err", "err":"delta", "msg":"Too much difference between stored and colected patch versions. Aborting update." }
    #    return (json.dumps(result) + "\n", 500)
    #
    #else:
    #    cur = con.cursor()
    #    cur.execute("DROP TABLE WINDOWS")
    #    cur.execute("ALTER TABLE new RENAME TO windows")
    #
    #    result = { "status":"ok", "msg":"Reloaded" }
    #    return (json.dumps(result) + "\n", 200)


@app.route('/refresh', methods=['PUT'])
def refresh():
    x = harvest(pages)
    #return "Reloaded from source page(s)\n", 201
    return x


@app.route('/latest/<version>', methods=['GET'])
def latest(version):
    connection = pg8000.dbapi.Connection(
        host = os.environ['POSTGRES_HOST'],
        user = os.environ['POSTGRES_USER'],
        password = os.environ['POSTGRES_PASSWORD'],
        database = os.environ['POSTGRES_DATABASE'],
        port = 5432
    )

    sql = connection.cursor()
    sql.execute("SELECT DISTINCT(patch) FROM windows WHERE release = '{release}' ORDER BY patch DESC".format(release = version))

    throwaway = sql.fetchone()[0]   # Requirement is latest-mnus-one
    latest_patch = sql.fetchone()[0]
    prior_patch = sql.fetchone()[0]

    connection.close()

    result = { "release":version, "latest_patch":latest_patch, "previous_patch":prior_patch, "previous_base":"10.0." + version + "." + prior_patch, "latest_base":"10.0." + version + "." + latest_patch  }

    return json.dumps(result) + "\n"




@app.route('/about')
def about():
    return 'About'
