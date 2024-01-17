import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

def extract_html(url):
    with requests.get(url) as fp:
        html = fp.text
    return html


data = []
for i in range(4):
    html = extract_html(f"http://faculty.webster.edu/corbetre/dogtown/history/1900-lastname{i+1}.html")
    soup = bs(html, 'html.parser')
    tables = soup.find_all('table', {"border":""})
    table = [t for t in tables if t.get("border") == ""][0]
    df = pd.read_html(str(table), header=0)[0]
    data.append(df)

data = pd.concat(data)
# Some are annotated with ()
lnames = data['Last Name'].str.split("(").str[0].str.strip().unique()
np.savetxt('lnames.txt', lnames, fmt="%s")

