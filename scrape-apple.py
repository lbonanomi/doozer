from bs4 import BeautifulSoup
import requests
import psycopg2
import os
import re

connection = psycopg2.connect(
  host = os.environ['POSTGRES_HOST'],
  user = os.environ['POSTGRES_USER'],
  password = os.environ['POSTGRES_PASSWORD'],
  database = os.environ['POSTGRES_DATABASE'],
  port = 5432,
  sslmode='require'
)

sql = connection.cursor()


releases = ['Sequoia', 'Sonoma', 'Ventura', 'Tahoe']

for page in ['https://support.apple.com/en-us/100100']:
    data = requests.get(page, timeout=10).text

    soup = BeautifulSoup(data, 'html.parser')

    for release in releases:
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):

                if "macOS" in row.text:
                    columns = row.find_all('td')

                    if release in columns[0].text:
                        for links in columns[0].findAll('a'):
                            stem = "https://support.apple.com" + links.get('href')

                        try:
                            stem
                        except NameError:
                            stem = ""
                      
                        patchArr = columns[0].text.split()
                        patch = re.sub('[A-Za-z]', '', patchArr[2])

                        sql.execute("INSERT INTO macos VALUES ('{}', '{}', '{}', '{}', '{}')".format(columns[2].text, patch, release, page, stem))

connection.commit()
sql.close()
connection.close()
