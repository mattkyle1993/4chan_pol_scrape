from base64 import encode
from concurrent.futures import thread
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
from selenium.webdriver.common.keys import Keys
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
import sys
import re
import random
import collections
from mysql_database_functions import * 

WEBDRIVER_PATH = "C:\\Users\mattk\Desktop\streaming_data_experiment\chromedriver_win32\chromedriver.exe"
PARSE_HTML_FILE_PATH = 'C:/Users/mattk/Desktop/streaming_data_experiment/html_file/'
DEFAULT_TXT_FILES_PATH = "C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/txt_files/"
WORD_COUNT_JSON_CURRENTS_PATH ="C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/word_count_jsons/"
CONTENT_LIST_TXT_FILES_PATH = "C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/content_list_txt_files/"
QUERY_WORD_COUNTS_PATH = "C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/query_word_counts/"


def give_date_and_time(hours=False):
    now = datetime.now()
    if hours == True:
        formatted_date = now.strftime("%m_%d_%Y_%H_%M")
    else:
        formatted_date = now.strftime("%m_%d_%Y")
    return formatted_date

def count_analyze_words(thread_reply_list):
        
        """
        get a count of each unique string and write it to a json file
        """
        
        formatted_date = give_date_and_time(hours=True)

        from collections import defaultdict
        word_counts = defaultdict(int)
        
        nested_content_list = thread_reply_list['replies']
        
        flat_list = []
        for nest in nested_content_list:
            if type(nest) == str:
                nest = nest.split()
                for nestt in nest:
                    flat_list.append(nestt)
            if type(nest) == list:
                for n in nest:
                    nn = n.split()
                    for nnn in nn:
                        flat_list.append(nnn)
        for content in flat_list:
            words = content.split()
            for word in words:
                word_counts[word]+=1
        file_name = f"{WORD_COUNT_JSON_CURRENTS_PATH}word_counts_{formatted_date}.json"
        file_name_forscript = f"{WORD_COUNT_JSON_CURRENTS_PATH}word_counts_current_{formatted_date}.json"
        sorted_dict = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

        
        with open(file_name, "w") as json_file:
            json.dump(sorted_dict, json_file,indent=4) 

        with open(file_name_forscript, "w") as json_file:
            json.dump(sorted_dict, json_file,indent=4) 
        
        with open(f'{CONTENT_LIST_TXT_FILES_PATH}content_list_{formatted_date}.txt', 'w',encoding='utf-8') as f:
            for line in flat_list:
                f.write(line)
                f.write('\n')
        f.close()
        print("content list created")
        return formatted_date

f = open("thread_replies_dict_test.json")
data = json.load(f)
f.close()

count_analyze_words(data)
