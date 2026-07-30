import csv
from io import StringIO
from urllib.parse import urlunparse, urlparse

import requests


def csv_read_text(text):
    rows = []
    fp = StringIO(text, newline="")
    return csv.reader(fp)


def csv_dict_read_text(text):
    rows = []
    fp = StringIO(text, newline="")
    return csv.DictReader(fp)


def read_google_sheet(url):
    # https://docs.google.com/spreadsheets/d/1kAhlM57dGLYBZCksvJiSxgswzInKM98WIkZhoB037SI/edit?usp=sharing
    # https://docs.google.com/spreadsheets/d/1kAhlM57dGLYBZCksvJiSxgswzInKM98WIkZhoB037SI/export?format=csv&usp=sharing
    u = urlparse(url)
    new = urlunparse(
        u._replace(path=u.path.replace("/edit", "/export"), query=f"format=csv&{u.query}")
    )
    r = requests.get(new)
    r.encoding = "utf-8"
    
    return list(csv_read_text(r.text))
