import csv
from io import StringIO
from urllib.parse import urlunparse, urlparse

import requests


def read_google_sheet(url):
    # https://docs.google.com/spreadsheets/d/1kAhlM57dGLYBZCksvJiSxgswzInKM98WIkZhoB037SI/edit?usp=sharing
    # https://docs.google.com/spreadsheets/d/1kAhlM57dGLYBZCksvJiSxgswzInKM98WIkZhoB037SI/export?format=csv&usp=sharing
    u = urlparse(url)
    new = urlunparse(
        u._replace(path=u.path.replace("/edit", "/export"), query=f"format=csv&{u.query}")
    )
    r = requests.get(new)
    r.encoding = "utf-8"
    

    rows = []
    fp = StringIO(r.text, newline="")
    return [r for r in csv.reader(fp)]
