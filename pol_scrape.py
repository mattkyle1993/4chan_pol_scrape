import requests
import json
import html_to_json
from bs4 import BeautifulSoup
import psutil    
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import time
from fuzzywuzzy import fuzz, process
import math
from pol_scrape_funcs import * # import functions

# check if VPN is running to safely protect IP address while scraping
# if not running start it up and wait for the program to successfully start before scraping
urls_list = [
    "https://boards.4chan.org/pol/thread/449494489",
    "https://boards.4chan.org/pol/thread/449526226",
    "https://boards.4chan.org/pol/thread/449514242",
    "https://boards.4chan.org/pol/thread/449524492",
    "https://boards.4chan.org/pol/thread/449490998",
    "https://boards.4chan.org/pol/thread/449527376",
    "https://boards.4chan.org/pol/thread/449520687",
    "https://boards.4chan.org/pol/thread/449524526",
    "https://boards.4chan.org/pol/thread/449528422",
    "https://boards.4chan.org/pol/thread/449529428",
    "https://boards.4chan.org/pol/thread/449522438",
    "https://boards.4chan.org/pol/thread/449519290",
    "https://boards.4chan.org/pol/thread/449526686",
    "https://boards.4chan.org/pol/thread/449527537",
    "https://boards.4chan.org/pol/thread/449502986",
    "https://boards.4chan.org/pol/thread/449526713",
    "https://boards.4chan.org/pol/thread/449492267",
    "https://boards.4chan.org/pol/thread/449518710",
    "https://boards.4chan.org/pol/thread/449521804",
    "https://boards.4chan.org/pol/thread/449529770",
    "https://boards.4chan.org/pol/thread/449525250"
]
# list of specific words to search for and find matches using fuzzy wuzzy
word_query_list = ["jew","hitler"] # e.g., n-word, k-word, etc.


if __name__ == "__main__":
    run_vpn()
    content_list = run_url_scrape(urls_list)
    count_analyze_words(content_list)
    json_data = grab_latest_json()
    query_list_match_dict = find_similar_matches(query_list=[],dictionary=json_data,threshold=80) # LIST OF SLURS TO QUERY
    
    

