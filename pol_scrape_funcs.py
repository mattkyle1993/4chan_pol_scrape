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

WEBDRIVER_PATH = "C:\\Users\mattk\Desktop\streaming_data_experiment\chromedriver_win32\chromedriver.exe"
PARSE_HTML_FILE_PATH = 'C:/Users/mattk/Desktop/streaming_data_experiment/html_file/'
DEFAULT_TXT_FILES_PATH = "C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/txt_files/"
WORD_COUNT_JSON_CURRENTS_PATH ="C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/word_count_jsons/"
CONTENT_LIST_TXT_FILES_PATH = "C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/content_list_txt_files/"
QUERY_WORD_COUNTS_PATH = "C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/query_word_counts/"

PATHS_LIST = [
    WEBDRIVER_PATH,
PARSE_HTML_FILE_PATH,
DEFAULT_TXT_FILES_PATH,
WORD_COUNT_JSON_CURRENTS_PATH,
CONTENT_LIST_TXT_FILES_PATH,
QUERY_WORD_COUNTS_PATH 
]

def provide_save_path(folder_path):
    
    """
    
    WEBDRIVER_PATH = chromedriver.exe
    PARSE_HTML_FILE_PATH = html_file
    DEFAULT_TXT_FILES_PATH = txt_files
    WORD_COUNT_JSON_CURRENTS_PATH = word_count_jsons
    CONTENT_LIST_TXT_FILES_PATH = content_list_txt_files
    QUERY_WORD_COUNTS_PATH = query_word_counts
    
    """
    
    for path in PATHS_LIST:
        if folder_path in path:
            THE_PATH = path
            pass
    return THE_PATH

def give_date_and_time(hours=False):
    now = datetime.now()
    if hours == True:
        formatted_date = now.strftime("%m_%d_%Y_%H_%M")
    else:
        formatted_date = now.strftime("%m_%d_%Y")
    return formatted_date

class gosh_darn_match_date():
    """
    this is for grabbing specific "word_count_current" json files by a given match_date
    """
    def __init__(self):
        self.latest_scrape_specific_match_date = ""

class MyHTMLParser(HTMLParser):
    """
    Got the original code from here, before modifications:  
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.parsed_list = []
        self.tag = "a"
        self.content = ""
        self.content_search = False
        self.thread_search = True
    def handle_starttag(self, tag, attrs):
        
        if self.thread_search == True:
            if self.tag == "":
                # print("Start tag:", tag)
                for attr in attrs:
                    if self.content_search == True:
                        if self.content in attr:
                            self.parsed_list.append(attr)
                        # print("     attr:", attr)
                    else:
                        self.parsed_list.append(attr)
            if self.tag == "a":
                if tag == self.tag:
                    # print("Start tag:", tag)
                    for attr in attrs:
                        if self.content_search == True:
                            if self.content in attr:
                                self.parsed_list.append(attr)
                            # print("     attr:", attr)
                        else:
                            self.parsed_list.append(attr)
        if self.thread_search == False:
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

def get_selenium_driver():
    """
    returns webdriver so selenium can be implemented more easily
    """
    webdriver_path = WEBDRIVER_PATH
    service = Service(executable_path=webdriver_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)    
    return driver

def parse_html(html_content,filename,thread_search=True): 
    """
    takes html_content from selenium page_source output
    takes a filename
    """
    file_name = PARSE_HTML_FILE_PATH + filename + '.html'

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(html_content)
    time.sleep(5)
    
    HTMLFile = open(file_name, "r",encoding="utf-8") 
    HTMLFile = HTMLFile.read() 
    parser = MyHTMLParser()
    if thread_search == False:
        parser.thread_search = False
    parser.feed(HTMLFile)

    parsed_list = parser.parsed_list  
    return parsed_list

class scrape_pol_class():
    
    def __init__(self):
        self.thread_list = []
        self.replies_left = 0
        self.urls_left = 0
        
    def give_number_left(self, num_urls, num_replies, url_ct, reply_ct):
        url_left = num_urls - url_ct
        reply_left = num_replies - reply_ct
        if reply_ct == 1:
            print(f"||||| {url_left} URLS left to scrape |||||")
        print("REPLIES left:", reply_left)

    def grab_info_from_threads(self, thread_list, return_dataframe = False):
        
        """
        grabs replies, number of images, number of posters, and any identifiable posters (and all posters in general), 
        and cross-checking other threads to see if they post there too
        
        search 4chan by poster ID, then get counts of all slurs, topics, terms, etc. by poster
        """
        
        
        XPTHS = ["/html/body/div[10]/div/span[1]","/html/body/div[10]/div/span[3]"] 
        thread_dict_list = []
        url_ct = 0
        thread_list_len = len(thread_list)
        shortend_threads = []
        for url in thread_list:
            thread_dict = {}
            url_ct += 1
            driver = get_selenium_driver()
            driver.get(url)
            driver.implicitly_wait(3) # wait a few seconds for driver to catch up to the request
            
            pattern = r"\b\d{9}\b"
            match = re.search(pattern, url)
            thread_dict['thread_number'] = match.group()
            # print("url:",url)
            # print("match.group():", match.group())
            shortend_threads.append(match.group())

            try:
                elem = driver.find_elements(By.XPATH, XPTHS[0]) # grab thread reply count by xpath # right-click the element in the browser and copy the xpath

                for el in elem:
                    thread_dict["num_replies"] = int(el.text)
            except:
                thread_dict["num_replies"] = 0

            try: 
                elem = driver.find_elements(By.XPATH, XPTHS[1]) # grab thread reply count by xpath # right-click the element in the browser and copy the xpath
                for el in elem:
                    thread_dict["num_posters"] = int(el.text)
            except:
                thread_dict["num_posters"] = 0
            urls_left = thread_list_len - url_ct
            # print("urls left:", urls_left)
            thread_dict_list.append(thread_dict)
        if return_dataframe == True:
            thread_dict = pd.DataFrame(thread_dict_list)
        else:
            thread_dict = merge_dicts(thread_dict_list)
        return [thread_dict, shortend_threads]

    def grab_all_replies(self, thread_dict, shortend_threads):
        
        thread_reply_dict_list = []

        thread_nums = thread_dict['thread_number']
        num_replies = thread_dict['num_replies']
        pairs = zip(thread_nums, num_replies)
        url_ct = 0
        for thread_number, num_reply in pairs:
            URL_ = f"https://boards.4chan.org/pol/thread/{thread_number}"
            reply_ct = 0
            thread_reply_dict = {
                "thread":thread_number,
            }
            REPLY_CT = num_reply
            replies_list = []
            if REPLY_CT > 0: # break death loop on threads with no replies
                url_ct += 1
                try:
                    while reply_ct <= REPLY_CT:
                        reply_ct += 1
                        scrape = scrape_pol_class()
                        scrape.give_number_left(num_urls=len(thread_nums),num_replies=REPLY_CT,url_ct=url_ct,reply_ct=reply_ct)
                        driver = get_selenium_driver()
                        driver.get(URL_)
                        # driver.implicitly_wait() # wait a few seconds for driver to catch up to the request
                        try:
                            elem = driver.find_elements(By.XPATH, f"/html/body/form[2]/div[1]/div[1]/div[{reply_ct}]/div[2]/blockquote") # grab thread reply count by xpath # right-click the element in the browser and copy the xpath
                            for el in elem:
                                # print("el.text::",el.text)
                                print("reply_ct:",reply_ct)
                                replies_list.append(el.text) 
                        except Exception as error:
                            print('error:', Exception)
                            replies_list.append(f"ERROR: {Exception}") 
                    thread_reply_dict['post_replies'] = replies_list
                    thread_reply_dict_list.append(thread_reply_dict)
                except:
                    replies_list.append("")
                    thread_reply_dict['post_replies'] = replies_list
                    thread_reply_dict_list.append(thread_reply_dict)
            if REPLY_CT == 0:
                url_ct += 1
            
        write_json(dictionary_list = thread_reply_dict_list,file_name="test")
        return thread_reply_dict_list

    def grab_thread_urls_from_catalog(self,self_list = False):
        """
        grabs thread URLs from catalog page of 4chan /pol/
        
        https://boards.4chan.org/pol/catalog
        """
        pol_cat_url = "https://boards.4chan.org/pol/catalog"
        
        driver = get_selenium_driver()
        driver.get(pol_cat_url)
        time.sleep(5)
        
        html_content = driver.page_source

        the_list = parse_html(html_content=html_content,filename="4chan_catalog_pol")
        thred_list = []
        for item in the_list:
            # print(item)
            if item[0] == 'href':
                if "/pol/thread/" in item[1]:
                    if item[1] not in thred_list:
                        thread_url = "https:" + item[1]
                        thred_list.append(thread_url)

        if self_list == True:
            self.thread_list = thred_list
        return thred_list

def write_json(dictionary={},file_name = "oops_nofilename", dictionary_list = []):
    
    if dictionary_list != []:
        dictionary = merge_dicts(dictionary_list)
        formatted_date = give_date_and_time(hours=True)
        path = f"replies_dictionary/{file_name}_{formatted_date}.json"
        with open(path, "w") as json_file:
            json.dump(dictionary, json_file, indent=4) 
    if dictionary_list == []:
        formatted_date = give_date_and_time(hours=True)
        path = f"replies_dictionary/{file_name}_{formatted_date}.json"
        with open(path, "w") as json_file:
            json.dump(dictionary, json_file, indent=4) 

def write_line_by_line_txt(content_list,filename,direct_address="", directory_name="defalt",html=False):
    """
    filename: takes a filename for a txt file. Do not include '.txt' in filename.
    directory_name: either default, which is the default directory, or
    it takes whatever directory you give it, with a forward slash on the end
    """
    
    formatted_date = give_date_and_time(hours=True)
    
    directory_dict = {
        "default":DEFAULT_TXT_FILES_PATH,
        f"{directory_name}":f"{direct_address}"
    }
    if directory_name == "defalt":
        ct = 0
        for key, value in directory_dict.items():
            ct += 1
            if ct == 1:
                direct_address = value
    else:
        ct = -1
        for key, value in directory_dict.items():
            ct += 1
            if ct == 1:
                direct_address = value
    if html == False:
        with open(f"{direct_address}{filename}_{formatted_date}.txt", "w") as file:
            for line in content_list:
                file.write(line)
                file.write('\n')
            file.close()
    if html == True:
        with open(f"{direct_address}{filename}_{formatted_date}.txt", "w",encoding="utf-8") as file:
            for line in content_list:
                file.write(line)
                file.write('\n')
            file.close()
            
    print("Txt file written. Number of lines:",len(content_list))

def split_into_sentences(content_list):
    """
    
    GRABBED THIS FUNCTION FROM HERE: https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences
    I MODIFIED IT SOMEWHAT.
    
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    all_sentences = []
    # -*- coding: utf-8 -*-
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'
    
    for text in content_list:
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
        text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = [s.strip() for s in sentences]
        if sentences and not sentences[-1]: sentences = sentences[:-1]
        for sentence in sentences:
            all_sentences.append(sentence)
    return all_sentences

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
    
    formatted_date = give_date_and_time(hours=True)
    
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
    file_name = f"{WORD_COUNT_JSON_CURRENTS_PATH}word_counts_{formatted_date}.json"
    file_name_forscript = f"{WORD_COUNT_JSON_CURRENTS_PATH}word_counts_current_{formatted_date}.json"
    gosh_darn = gosh_darn_match_date()
    gosh_darn.latest_scrape_specific_match_date = formatted_date
    sorted_dict = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

    # upload word counts and post content to Mysql database
    # upload_data_mySQL(sorted_dict,content_list) 
    
    with open(file_name, "w") as json_file:
        json.dump(sorted_dict, json_file,indent=4) 

    with open(file_name_forscript, "w") as json_file:
        json.dump(sorted_dict, json_file,indent=4) 
    
    with open(f'{CONTENT_LIST_TXT_FILES_PATH}content_list_{formatted_date}.txt', 'w',encoding='utf-8') as f:
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
    merge_dict = {}
    for d in dicts_list:
        for key, value in d.items():
            # Create an entry in the merged dictionary for each key
            if key not in merge_dict:
                merge_dict[key] = []
            merge_dict[key].append(value)
    return merge_dict

def get_counts_for_queries(query_tuple_list,word_counts_dict,filename):

    query_words = {}
    for q in query_tuple_list:
        word = q[0]
        score = q[1]
        if score >= 80:
            query_words[word] = score
    
    new_count_dict = {}
    for q_word in query_words:
        for wordd, count in word_counts_dict.items():
            if wordd == q_word:
                new_count_dict[wordd] = count
    
    count = 0
    for word, ct in new_count_dict.items():
        count += ct

    blur_words = {
        "nigger":"n-word",
        "jew":"jew",
        "hitler":"hitler",
        "kike":"k-word",
        "poo":"poo (anti-Indian slur)",
        "white":"white",
        "jesus":"jesus",
        "christian":"christian",
        "muslim":"muslim",
        "troon":"troon",
        "tranny":"tranny",
        "genocide":"genocide",
        "kill":"kill",
        "goy":"goy",
        "globohomo":"globohomo", # aka, colonial imperialism as it defined by russian-style fascists; or perhaps some NWO-style plan by the globalists (jews) as defined by conservatives
        "globalist":"globalist",
        "fren":"fren",
        "comfy":"comfy",
        "pogrom":"pogrom",
        "society":"society",
        "collapse":"collapse",
        "kosher":"kosher",
        "blood":"blood",
        "vermin":"vermin",
        "shitskin":"shitskin"
    }
    formatted_date = give_date_and_time(hours=True)
    # readable_formatted_date = now.strftime("%m_%d_%Y") 
    
    simple_count_dict = {filename:count}
    
    print(f"Query:{blur_words[filename]}. Number of occurances: {count}.")
    query_file_name = f"{QUERY_WORD_COUNTS_PATH}query_word_count_query_{filename}_{formatted_date}.json"
    with open(query_file_name, "w") as json_file:
        json.dump(simple_count_dict, json_file, indent=4) 

def find_similar_matches(query_list, words_dictionary, threshold=80):

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
        for word, score in words_dictionary.items():
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
            # for word, similarity_score in matches:
            #     # print(f"QUERY:{query}. {word}: {similarity_score}")
            #     pass
            match_dict_list.append(matches)
        else:
            print("no matches for query:",query)
        
        get_counts_for_queries(matches,words_dictionary,filename=query)
    # return merge_dicts(match_dict_list)
     
def search_content(search_word, search_date="",query_dict={}):   
    """
    takes an optional search date in the format: 01-01-1999
    """
    now = datetime.now()
    if search_date != "":
        search_date = search_date
    else:
        search_date = now.strftime("%m_%d_%Y")
    folder_path = CONTENT_LIST_TXT_FILES_PATH
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if f"{search_date}" in file:
                this_one = file
                print(file)
                break
    this_one = folder_path + "/" + this_one
    
    searched_content = []
    with open(this_one,"r",encoding="utf-8") as file:
        for f in file:
            if search_word in f:
                if f not in searched_content:
                    searched_content.append(f)
    
    print(len(searched_content))
    search_date = now.strftime("%m_%d_%Y_%H_%M")
    file_path = f"{CONTENT_LIST_TXT_FILES_PATH}searched_{search_word}_{search_date}.txt"
    with open(file_path,"w",encoding="utf-8") as file:
        for s in searched_content:
            file.write(s)
            file.write('\n')
    
    
def grab_latest_json():
    """
    grab latest json file to build dictionary for matching function
    """
    gosh_darn = gosh_darn_match_date()
    directory = f"{WORD_COUNT_JSON_CURRENTS_PATH}word_counts_current_{gosh_darn.latest_scrape_specific_match_date}.json"
    f = open(directory)
    data = json.load(f)
    f.close()
    return data


            