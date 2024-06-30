import os
from time import strftime, localtime
import json
from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'
