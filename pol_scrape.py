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
                   "blood","kosher","vermin","military","pajeet",
                   "shitskin"] # e.g., n-word, k-word, etc.

        
    
        
if __name__ == "__main__":
    main = MainScrapeFunc()
    main.minimize_or_hide(minimize=True)
    main.main_function(
                        word_query_list=word_query_list,
                        complete_run=True,
                        save_thread_list=True,
                        sql_insert=False, 
                        # random_grab=3
                       )

# if there are strange discrepancies in the data from scrape to scrape (within hours), it 
# could be that previous threads in other scrapes have disappeared (404'd), and so 
# those word counts went down with them

# /html/body/form[2]/div[1]/div[1]/div[7]/div[2]/div[3]/a/img
# /html/body/form[2]/div[1]/div[1]/div[2]/div[2]/div[3]/a/img

# Las vegas December 6th (?), 2023 mass shooting 4chan/pol/ responses:
#         # "https://boards.4chan.org/pol/thread/451088072",
#         # "https://boards.4chan.org/pol/thread/451086113",
#         # "https://boards.4chan.org/pol/thread/451090789",
#         # "https://boards.4chan.org/pol/thread/451088971",
#         # "https://boards.4chan.org/pol/thread/451092402"