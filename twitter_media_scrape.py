from ast import parse
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
from mysql_database_functions import * # import mySQL functions

url = "https://twitter.com/EndWokeness/status/1730405097866137838"

driver = get_selenium_driver()
driver.get(url)
time.sleep(5)
html_content = driver.page_source
driver.quit()
parsed_content = parse_html(html_content=html_content,filename="twitter_experiment",thread_search=False)
write_line_by_line_txt(content_list=parsed_content,filename="twitter_experiment")