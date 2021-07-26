import requests
from bs4 import BeautifulSoup
import sys
import sqlite3
import pickle as pkl
import argparse
import pandas as pd

def get_ETF_asx_list():
    # Get list of all ETFs listed on ASX
    URL = 'https://www2.asx.com.au/markets/trade-our-cash-market/asx-investment-products-directory/etps'
    HTML = requests.get(URL)
    if(not HTML.status_code==200):
        sys.exit(URL + " is not available\n", "RESPONSE " + HTML.status_code)
    soup = BeautifulSoup(HTML.text,'html.parser')
    region = []
    for head in soup.find_all('div', 'cmp-text'):
        for h4 in head.find_all('h4'):
            if(len(h4.text.strip()) > 1):
                region.append(h4.text.replace(" ",""))
    alldata = []
    links = []
    for idx, table in enumerate(soup.find_all('table')):           
        rows = table.findAll('tr')
        data = [[cell.text for cell in row("td")] for row in rows]
        links.extend( [f"{rows[i].td.a}" for i in range(1,len(rows))])
        headers=data.pop(0)
        for entry in data:
            entry.insert(0,region[idx])
        #print(data)
        alldata.extend(data)
    headers = [h.strip() for h in headers]
    headers.insert(0,'Market')
    return  alldata, headers, links

def get_ETF_performance():
    # Get performance of all ETFs listed on ASX
    URL = 'https://www.morningstar.com.au/ETFs/PerformanceTable#'
    HTML = requests.get(URL)
    if(not HTML.status_code==200):
        sys.exit(URL + " is not available\n", "RESPONSE " + HTML.status_code)
    soup = BeautifulSoup(HTML.text,'html.parser')
    alldata = []
    for idx, table in enumerate(soup.find_all('table')):           
        rows = table.findAll('tr')
        data = [[cell.text for cell in row("td")] for row in rows]
        #print(data)
        alldata.extend(data)
    last_upd = soup.find('div', 'LightgreySmall')
    return alldata, last_upd.string




