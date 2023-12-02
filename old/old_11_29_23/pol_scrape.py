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

# list of specific words to search for and find matches using fuzzy wuzzy
word_query_list = ["jew","hitler",] # e.g., n-word, k-word, etc.

if __name__ == "__main__":
    thread_list = grab_thread_urls_from_catalog()
    run_vpn_and_chromedriver()
    content_list = run_url_scrape(thread_list)
    count_analyze_words(content_list)
    json_data = grab_latest_json()
    query_list_match_dict = find_similar_matches(query_list=word_query_list,dictionary=json_data,threshold=80) # LIST OF SLURS TO QUERY
    
    

