from bs4 import BeautifulSoup
import requests
import psycopg2
import os
import re


pages = ["https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information" , "https://learn.microsoft.com/en-us/windows/release-health/release-information"]


connection = psycopg2.connect(
  host = os.environ['POSTGRES_HOST'],
  user = os.environ['POSTGRES_USER'],
  password = os.environ['POSTGRES_PASSWORD'],
  database = os.environ['POSTGRES_DATABASE'],
  port = 5432,
  sslmode='require'
)

sql = connection.cursor()

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

      try:
        kb = columns[3].text
      except IndexError:
        continue


      if re.search("[0-9]{4}\-[0-9]{2}\-[0-9]{2}", avail_date):
        sql.execute("INSERT INTO windows VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(svc_option, avail_date, release, patch, page, kb))


connection.commit()
sql.close()
connection.close()
