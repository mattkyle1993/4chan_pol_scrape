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
import re

# list of specific words to search for and find matches using fuzzy wuzzy

word_query_list = ["nigger","kike","jew","white","jesus",
                   "hitler","christian","muslim","troon",
                   "tranny","genocide","kill","goy",
                   "globalist","fren","comfy","globohomo",
                   "pogrom","society","collapse",
                   "blood","kosher","vermin"] # e.g., n-word, k-word, etc.
now = datetime.now()
readable_formatted_date = now.strftime("%m-%d-%Y")

# indian_slurs = ["pajeet","poo"]

def main_function(complete_run=False,sql_insert=False,save_thread_list=False,choose_thread=""):
    if complete_run == True:
        run_vpn_and_chromedriver()
        scrape = scrape_pol_class()
        if choose_thread != "":
            if type(choose_thread) == str:
                if len(choose_thread) == 9:
                    choose_thread = f"https://boards.4chan.org/pol/thread/{choose_thread}"
                    thread_list = [choose_thread]
                else:
                    thread_list = [choose_thread]
            if type(choose_thread) == list:
                thread_list = choose_thread
        if choose_thread == "":
            print("grabbing all threads")
            thread_list = scrape.grab_thread_urls_from_catalog()
            thread_list = thread_list[2:4]
        if save_thread_list == True:
            write_line_by_line_txt(thread_list,filename="temp_thread_list")
        thread_dict, shortened_threads = scrape.grab_info_from_threads(thread_list)
        write_json(thread_dict,file_name="thread_dict")
        thread_reply_dict_list = scrape.grab_all_replies(thread_dict,shortened_threads)
        print("Number of threads scraped:",len(thread_list))
        content_list = run_url_scrape(thread_list)
        count_analyze_words(content_list)
    json_data = grab_latest_json()
    print(f"Word counts on 4chan/pol/ for threads existing on: {readable_formatted_date}")
    # query_list_match_dict = find_similar_matches(query_list=word_query_list,words_dictionary=json_data,threshold=80) # LIST OF SLURS TO QUERY
    find_similar_matches(query_list=word_query_list,words_dictionary=json_data,threshold=80) # LIST OF SLURS TO QUERY
    if sql_insert == True:
        print("test")
        # insert_into_table(sql_table="pol_word_counts")
        # insert_into_table(sql_table="thread_stats_info",thread_list=thread_list)
    
if __name__ == "__main__":
    main_function(complete_run=True,sql_insert=True,save_thread_list=True,choose_thread=[
        "https://boards.4chan.org/pol/thread/451088072",
        "https://boards.4chan.org/pol/thread/451086113",
        "https://boards.4chan.org/pol/thread/451090789",
        "https://boards.4chan.org/pol/thread/451088971",
        "https://boards.4chan.org/pol/thread/451092402"
        ])

# if there are strange discrepancies in the data from scrape to scrape (within hours), it 
# could be that previous threads in other scrapes have disappeared (404'd), and so 
# those word counts went down with them

# /html/body/form[2]/div[1]/div[1]/div[7]/div[2]/div[3]/a/img
# /html/body/form[2]/div[1]/div[1]/div[2]/div[2]/div[3]/a/img