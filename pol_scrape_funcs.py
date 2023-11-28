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

class MyHTMLParser(HTMLParser):
    """
    Got the original code from here, before modifications: https://docs.python.org/3/library/html.parser.html
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.parsed_list = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            # print("Start tag:", tag)
            for attr in attrs:
                # print("     attr:", attr)
                
                self.parsed_list.append(attr)
    def handle_endtag(self, tag):
        # print("End tag  :", tag)
        pass

    def handle_data(self, data):
        # print("Data     :", data)
        pass

    def handle_comment(self, data):
        # print("Comment  :", data)
        pass

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        # print("Named ent:", c)
        pass
    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        # print("Num ent  :", c)
        pass
    def handle_decl(self, data):
        # print("Decl     :", data)
        pass

def run_vpn_and_chromedriver(chromedriver=False):
    
    program_directory = [
        "C:\\Program Files\Private Internet Access\pia-client.exe",
        "C:\\Users\mattk\Desktop\streaming_data_experiment\chromedriver_win32\chromedriver.exe"]
    program_name = ["VPN","CHROMEDRIVER"]
    if chromedriver == True:
        program_list = ["pia-client.exe","chromedriver.exe"]
    if chromedriver == False:
        program_list = ["pia-client.exe"]
    
    ct = -1
    for program in program_list:
        ct += 1
        wait_seconds = 10
        process_list = [p.name() for p in psutil.process_iter()]
        print("checking if VPN is running:")
        print("---------------------------"*5)
        if program not in process_list:
            print(f"...{program_name[ct]} not running...")
            print(f"...starting {program}...")
            os.startfile(program_directory[ct])
            print(f"...waiting for program {program_name[ct]} to start before scraping...")
            time.sleep(wait_seconds)
            process_list = [p.name() for p in psutil.process_iter()]
            if program in process_list:
                if "pia" in program:
                    print("...vpn has started. now activating private IP address...")
                    print(f"...waiting for {wait_seconds} seconds vpn to activate private IP addess...")
                    time.sleep(wait_seconds)
                    print("...wait complete!")
            if "pia" in program:
                print("error")
            else:
                pass
        else:
            print(f"...{program_name[ct]} running!")

def beaut_soup_grab(url,find_all='div',div_class=""):
    r = requests.get(url, headers={'accept': 'application/json'})
    if r.status_code == 200:
        # Process the response content here
        print(f"Success for {url}")
    else:
        # Log an error for non-success status codes
        print(f"Error: {url} returned status code {r.status_code}")
    output = r.text
    soup = BeautifulSoup(output, 'html.parser')
    if div_class == "":
        divs = soup.find_all(find_all) 
    else:
        divs = soup.find_all(find_all,class_=div_class) 
    return divs

def run_url_scrape(url_list):
    # code to automate grabbing URL's: TO BE CODED
    # sample URLs. These are likely deadlinks.
    
    # get latest date and sort div's by that
    now = datetime.now()
    search_date = now.strftime("%m/%d/%y")

    content_list = []
    for url in url_list:
        try:
            divs = beaut_soup_grab(url)
            # rid the list of divs without user postings by filtering for div's with anonymous 2 or more times
            for div in divs:
                content = div.text
                if content.count("Anonymous") >= 2:
                    if search_date in content:
                        if content in content_list:
                            pass
                        else:
                            content_list.append(content)
        except requests.exceptions.RequestException as e:
            # Handle exceptions raised by requests, e.g., connection error, timeout, etc.
            print(f"Request Exception for {url}: {e}")
        except Exception as e:
            # Handle other unexpected exceptions
            print(f"An unexpected error occurred for {url}: {e}")
            
    return content_list

def grab_thread_urls_from_catalog():
    """
    grabs thread URLs from catalog page of 4chan /pol/
    
    https://boards.4chan.org/pol/catalog
    """
    pol_cat_url = "https://boards.4chan.org/pol/catalog"
    
    webdriver_path = "C:\\Users\mattk\Desktop\streaming_data_experiment\chromedriver_win32\chromedriver.exe"
    
    service = Service(executable_path=webdriver_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(pol_cat_url)
    time.sleep(5)
    
    # Get the HTML content of the page
    html_content = driver.page_source

    # Specify the file name where you want to save the HTML content
    file_name = 'C:/Users/mattk/Desktop/streaming_data_experiment/html_file/4chan_catalog_pol.html'

    # Save the HTML content to a file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(html_content)

    # Close the WebDriver when you're done
    time.sleep(5)
    driver.quit()
    
    HTMLFile = open(file_name, "r",encoding="utf-8") 
    HTMLFile = HTMLFile.read() 
    parser = MyHTMLParser()
    parser.feed(HTMLFile)

    list = parser.parsed_list
    thread_list = []
    for item in list:
        if item[0] == 'href':
            if "/pol/thread/" in item[1]:
                if item[1] not in thread_list:
                    thread_url = "https:" + item[1]
                    thread_list.append(thread_url)

    return thread_list

def upload_data_mySQL(sorted_dict,content_list):
    
    """
    will create table for word counts by date
    
    create tables of particularly problmatic posts
    
    over time and with more data, trends can be seen for the use of different 
    words and terms that come and go with the broader newscycle 
    
    """
    
    pass

def count_analyze_words(content_list):
    
    """
    get a count of each unique string and write it to a json file
    
    also writes down each and every div to a txt file. each div should, in theory,
    be a unique post by a given user. so if there are 5000+ divs in the final list, then
    there are 5000 unique posts, in theory. It's highly likely there are mistakes getting through
    but this is the closest I can get, for now
    
    the portion about catching mass shooting key phrases is a work in progress    
    
    until mysql is set up, complete post content will be saved to a txt file and 
    word counts will be saved to a json file
    
    """
    
    now = datetime.now()
    formatted_date = now.strftime("%m_%d_%Y_%H_%M")
    
    from collections import defaultdict
    word_counts = defaultdict(int)
    
    # search for words that indicate violent intentions
    # "race war" is a prime example, though on its own it is meaningless
    # but "race war" in a mass shooter manifesto is not unheard of
    # other possible searches could be along the lines of:
    # "streaming live on facebook"
    # "wish me luck and follow in my footsteps"
    # "I am following in the footsteps of those before me"
    # "I'm going to go for a high score" ("Gamifying" mass shootings by seeing 
    #  ## # # how many kills they can get before they die by suicide or cop)
    # and other phrases like those that indicate someone is 
    # about to commit a mass shooting or mass violence in general
    
    race_war_ct = 0
    for content in content_list:
        if "race war" in content:
            race_war_ct += 1
        words = content.split()
        for word in words:
            word_counts[word]+=1
    file_name = f"C:/Users/mattk/Desktop/streaming_data_experiment/word_count_jsons/word_counts_{formatted_date}.json"
    file_name_forscript = f"C:/Users/mattk/Desktop/streaming_data_experiment/word_count_current/word_counts_current.json"
    sorted_dict = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

    # upload word counts and post content to Mysql database
    upload_data_mySQL(sorted_dict,content_list) 
    
    with open(file_name, "w") as json_file:
        json.dump(sorted_dict, json_file,indent=4) 
    try:
        os.remove("C:/Users/mattk/Desktop/streaming_data_experiment/word_count_current/word_counts_current.json")
    except:
        pass
    with open(file_name_forscript, "w") as json_file:
        json.dump(sorted_dict, json_file,indent=4) 
        
    with open(f'content_list_{formatted_date}.txt', 'w',encoding='utf-8') as f:
        for line in content_list:
            f.write(line)
            f.write('\n')
    f.close()
    print("content list created")

def more_non_letters_than_letters(input_string):
    
    """
    takes a given string and counts letters and non-letters and
    determines whether or not the string is more likely a word 
    or more likely a series of random characters
    """
    
    non_letter_count = 0
    letter_count = 0
    for char in input_string:
        if char.isalpha():
            letter_count += 1
        else:
            non_letter_count += 1
    return non_letter_count > letter_count

def merge_dicts(dicts_list):
    """
    merge together dictionaries
    """
    merged_dict = {}
    for d in dicts_list:
        merged_dict.update(d)
    return merged_dict

def find_similar_matches(query_list, dictionary, threshold=80):

    """
    find matches for the queryied words (i.e., slurs) and 
    remove and 'fluff' and mismatches
    """

    match_dict_list = []
    for query in query_list:
        # get upper bound number to add to query string size for getting matches
        querylen_step_1 = len(query) * .33
        querylen_step_2 = querylen_step_1 * 100
        querylen_step_3 = int(querylen_step_2)
        querylen_step_4 = querylen_step_3 % 100
        
        new_dict = {}
        for word, score in dictionary.items():
            match_string = word[0]
            match_string_first_letter = match_string[0].lower()
            query_string_first_letter = query[0].lower()
            if query_string_first_letter == match_string_first_letter:
                if querylen_step_4 >= 50:
                    uper_bnd = math.ceil(querylen_step_1)
                else:
                    uper_bnd = math.floor(querylen_step_1)
                uper_bnd = len(query) + uper_bnd
                if len(query) <= len(word):
                    if len(word) <= uper_bnd:
                        if more_non_letters_than_letters(word) == False:
                            new_dict[word] = score
        matches = process.extract(query, new_dict.keys(), limit=None)
        matches = [(word, score) for word, score in matches if score >= threshold]
        if matches:
            for word, similarity_score in matches:
                print(f"QUERY:{query}. {word}: {similarity_score}")
            match_dict_list.append(matches)
        else:
            print("no matches for query:",query)
    return merge_dicts(match_dict_list)

def grab_latest_json():
    """
    grab latest json file to build dictionary for matching function
    """
    directory = "C:/Users/mattk/Desktop/streaming_data_experiment/word_count_current/word_counts_current.json"
    f = open(directory)
    data = json.load(f)
    f.close()
    return data


            