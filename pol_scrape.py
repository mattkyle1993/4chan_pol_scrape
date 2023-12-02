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
from pol_scrape_funcs import * 
from mysql_database_functions import * 

# list of specific words to search for and find matches using fuzzy wuzzy
word_query_list = ["nigger","kike","jew","white","jesus","hitler","christian","muslim"] # e.g., n-word, k-word, etc.
now = datetime.now()
readable_formatted_date = now.strftime("%m-%d-%Y")

# indian_slurs = ["pajeet","poo"]

def main_function(complete_run=True,sql_insert=False):
    if complete_run == True:
        thread_list = grab_thread_urls_from_catalog()
        run_vpn_and_chromedriver()
        content_list = run_url_scrape(thread_list)
        count_analyze_words(content_list)
    json_data = grab_latest_json()
    if sql_insert == True:
        insert_into_table(json_query_data=json_data)
    print(f"Word counts on 4chan/pol/ for threads existing on: {readable_formatted_date}")
    # query_list_match_dict = find_similar_matches(query_list=word_query_list,words_dictionary=json_data,threshold=80) # LIST OF SLURS TO QUERY
    
if __name__ == "__main__":
    main_function(complete_run=False)



