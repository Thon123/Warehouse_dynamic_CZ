#!/usr/bin/python3
#TODO: ideálně řešit přes classu a inicializovat podle potřeby..
#místo import *

"""________________________________[ MODULY PRO CELEK ]"________________________________"""
import gspread #ok
# pip3 install oauth2client
from oauth2client.service_account import ServiceAccountCredentials 
import requests  # pip3 install requests
from bs4 import BeautifulSoup # pip3 install beautifulsoup4
from boltons.setutils import IndexedSet #pip3 install boltons
import tabula #tabula netřeba na server
from tabula import read_pdf #též netřeba na ubuntu
import csv #též netřeba na ubuntu
import os #též netřeba
from lxml import etree #sudo apt-get install python3-lxml
from lxml.builder import E #není instalačka
from timeit import default_timer as timer #netřeba už je
from retrying import retry #pip3 install retry
from datetime import datetime #pip3 install Datetime
from apscheduler.schedulers.blocking import BlockingScheduler #pip3 install APScheduler
import time
import json
from requests.auth import HTTPBasicAuth
import pprint
import sys


#adresa = ".\credentials.json"
#adresa = "C:\\Users\\thon\\OneDrive\\Plocha\\Upgrade\\Python\\Django\\Django SKLAD\\SKLAD_CELEK\\
# credentials.json"
"""________________________________[ PROPOJENÍ S GOOGLE SHEETS ]"________________________________"""
#Základní propojení Google Sheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials) #json soubor pro autorizaci

#URLČKA PRO FEEDY
nabitabaterka_url = "nabitabaterka.xml"
yescom_url = "yescom.xmll"
ep_url = "ep.xml"

"""_____________________________________[ PROPOJENÍ S API ]"_____________________________________"""

url_nb = "url_api_neuvdeno"
heslo_nb ="xxxxxxxxxxxxxxxx"
jmeno_nb ="nabitabaterka"

url_yescom = "url_api_neuvdeno"
heslo_yescom = "xxxxxxxxxxxxxx"
jmeno_yescom = "yescom"

url_ep = "url_api_neuvdeno"
heslo_ep = "xxxxxxxxxxxxxxx"
jmeno_ep = "easy-print"




