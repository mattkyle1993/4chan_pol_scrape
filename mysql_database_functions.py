import mysql.connector
import mysql.connector
import requests
import json
import html_to_json
from bs4 import BeautifulSoup
import psutil    
import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import time
from fuzzywuzzy import fuzz, process
import math
from html.parser import HTMLParser
from html.entities import name2codepoint
import codecs
import urllib.request, urllib.error, urllib.parse
import pathlib
import mysql.connector
from pol_scrape_funcs import *

def grab_latest_json():
    """
    grab latest json file to build dictionary for matching function
    """
    directory = "C:/Users/mattk/Desktop/streaming_data_experiment/word_count_current/word_counts_current.json"
    f = open(directory)
    data = json.load(f)
    f.close()
    return data

def login_create_mysql_cursor(): 
    try:
        cnx = mysql.connector.connect(user='root', password='fakeTrick56%',
                                    host='127.0.0.1',
                                    database='4chan_pol_scrape')
    except:
        pass

    cursor = cnx.cursor()
    return [cursor, cnx]

def close_commit_mysql_connect(cnx,cursor):
    cnx.commit()
    cnx.close() 
    cursor.close()

def insert_into_table(json_query_data, sql_table="pol_word_counts"):
    # insert_query = "INSERT INTO your_table_name (date, nigger, kike, jew, jesus, hitler) VALUES (%s, %s, %s, %s, %s, %s)"

    cursor, cnx = login_create_mysql_cursor()
    
    data_table = {
        "pol_word_counts": ['nigger', 'kike', 'jew', 'jesus', 'hitler']
    }
    
    words = data_table[sql_table]
    dataframe = {}
    for word in words:
        if word != 'date':
            for key, item in json_query_data.items():    
                if key == word:
                    dataframe[key] = item

    insert_query = f"INSERT INTO {sql_table} (nigger, kike, jew, jesus, hitler) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(insert_query,(dataframe['nigger'],dataframe['kike'],dataframe['jew'],dataframe['jesus'],dataframe['hitler']))
    close_commit_mysql_connect(cnx,cursor)



