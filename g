def harvest(connection, pages):
    """Drop existing definitions and reload from pages"""

    #sql = harvester_connection.cursor()

    return "GOT A DB HANDLE"

    for page in pages:
        data = requests.get(page, timeout=10).text

        return "GOT HTML"

        soup = BeautifulSoup(data, 'html.parser')

        return "SOUP'S ON!"
        
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

                sql.execute("INSERT INTO windows VALUES ('{}', '{}', '{}', '{}')".format(svc_option, avail_date, release, patch))

    
    result = { "status":"ok", "msg":"Reloaded" }
    return json.dumps(result) + "\n"
