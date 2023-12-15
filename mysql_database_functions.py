import mysql.connector
import mysql.connector
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
from pol_scrape_funcs import *
import re

def grab_latest_json():
    """
    grab latest json file to build dictionary for matching function
    """
    
    the_path = provide_save_path(folder_path="word_count_current")
    
    directory = f"{the_path}word_counts_current.json"
    f = open(directory)
    data = json.load(f)
    f.close()
    return data

def login_create_mysql_cursor(): 
    try:
        cnx = mysql.connector.connect(user='root', password='fakeTrick56%',
                                    host='127.0.0.1',
                                    database='4chan_pol_scrape')
    except:
        pass

    cursor = cnx.cursor()
    return [cursor, cnx]

def close_commit_mysql_connect(cnx,cursor):
    cnx.commit()
    cnx.close() 
    cursor.close()

def grab_query_word_count(query_word,temp_file_list):
    
    # base_length = "searched__00_00_0000_00_00.txt" # key to get the correct time stamp
    
    if len(temp_file_list) == 1:
        json_file = temp_file_list[0]
        print("json file name:",json_file)
        # directory = f"C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/word_count_current/query_word_counts/{json_file}"
        directory = json_file
        f = open(directory)
        data = json.load(f)
        f.close()
        word_ct = data[query_word]
        return word_ct
    
    if len(temp_file_list) > 1:
        temp_file_tuple_list = []
        for file in temp_file_list:
            print("max hour number:",int(file[-10:-8]))
            temp_file_tuple_list.append((file,int(file[-10:-8])))
    
        # using a loop to find the maximum element and sort based on it
        # sorted_list = []
        # max_val = 0
        # for tup in temp_file_tuple_list:
        #     print("tup here", tup)
        #     max_val = max(tup[1])
        #     sorted_list.append((tup, max_val))
        # sorted_list.sort(key=lambda x: x[1], reverse=True)
        # final_list = [tup[0] for tup in sorted_list]
        # json_file, _ = map(list,zip(*final_list))
        
        max_tuple = max(temp_file_tuple_list, key=lambda x: x[1])
        json_file = max_tuple[0]
        
        # directory = f"C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/word_count_current/query_word_counts/{json_file}"
        directory = json_file
        f = open(directory)
        data = json.load(f)
        f.close()
        word_ct = data[query_word]
        return word_ct
        
    
def insert_into_table(query_words_list=['nigger', 'kike', 'jew', 'jesus', 'hitler'], sql_table="pol_word_counts",thread_list = [], thread_dict={}):
    # insert_query = "INSERT INTO your_table_name (date, nigger, kike, jew, jesus, hitler) VALUES (%s, %s, %s, %s, %s, %s)"

    cursor, cnx = login_create_mysql_cursor()
    print("test 0.01")
    
    data_table = {
        "pol_word_counts": ['nigger', 'kike', 'jew', 'jesus', 'hitler'],
        "thread_stats_info":['num_replies','num_posters','thread_number']
    }
    now = datetime.now()
    search_date = now.strftime("%m_%d_%Y")
    if sql_table == "pol_word_counts":
        dataframe = {}
        path = "C:/Users/mattk/Documents/GitHub/4chan_pol_scrape/query_word_counts"
        print("test 2")
        for query in query_words_list:
            temp_list = []
            for file in glob.glob(os.path.join(path, '*.json')):
            # for file in files:
                if query in file:
                    if search_date in file:
                        temp_list.append(file)
            if len(temp_list) == 0:
                dataframe[query] = 0
            if len(temp_list) >= 1:
                dataframe[query] = grab_query_word_count(query_word=query,temp_file_list=temp_list)
                
        
        # words = data_table[sql_table]
        # dataframe = {}
        # for word in words:
        #     if word != 'date':
        #         for key, item in json_query_data.items():    
        #             if key == word:
        #                 dataframe[key] = item

        insert_query = f"INSERT INTO {sql_table} (nigger, kike, jew, jesus, hitler) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(insert_query,(dataframe['nigger'],dataframe['kike'],dataframe['jew'],dataframe['jesus'],dataframe['hitler']))
        print("test 3")
    if sql_table == "thread_stats_info":
        print("test 0.1")
        if thread_list != []:
            thread_dict, _ = scrape_pol_class.grab_info_from_threads(thread_list)
        if len(thread_list) == 0:
            thread_dict = thread_dict
        # columns = {row.column_name for row in cursor.columns(table='thread_stats_info')}
        # query = "INSERT INTO TABLEabc ({columns}) VALUES ({value_placeholders})".format(
        #     columns=", ".join(thread_dict.keys()),
        #     value_placeholders=", ".join(["?"] * len(thread_dict)),
        # )

        # cursor.execute(query, list(thread_dict.values()))
        print("test 1")
        for i in range(len(thread_dict['thread_number'])):
            print("test 0.0001")
            replies = thread_dict['num_replies'][i]
            posters = thread_dict['num_posters'][i]
            thread_num = thread_dict['thread_number'][i]
            
            sql = "INSERT INTO thread_stats_info (num_replies, num_posters, thread_number) VALUES (%s, %s, %s);"
            
            cursor.execute(sql, (replies, posters, thread_num))
            print("test 5")
        
    close_commit_mysql_connect(cnx,cursor)
