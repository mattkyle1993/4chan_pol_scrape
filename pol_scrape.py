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
from word_queries_input import *
import re

<<<<<<< Updated upstream
# list of specific words to search for and find matches using fuzzy wuzzy

word_query_list = ["nigger","kike","jew","white","jesus",
                   "hitler","christian","muslim","troon",
                   "tranny","genocide","kill","goy",
                   "globalist","fren","comfy","globohomo",
                   "pogrom","society","collapse",
                   "blood","kosher","vermin","military","pajeet",
                   "shitskin"] # e.g., n-word, k-word, etc.

        
    
        
=======
>>>>>>> Stashed changes
if __name__ == "__main__":
    main = MainScrapeFunc()
    main.minimize_or_hide(minimize=True)
    main.main_function(
                        word_query_list=[],
                        complete_run=True,
                        save_thread_list=True,
                        sql_insert=False, 
                        grab=15
                       )
