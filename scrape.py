from bs4 import BeautifulSoup
import requests
import psycopg2
import os
import re

print(
  len(os.environ['POSTGRES_USER']), 
  len(os.environ['POSTGRES_PASSWORD'])
     )
