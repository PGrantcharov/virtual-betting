from bs4 import BeautifulSoup, Comment
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import pandas as pd

"""
Beautiful Soup Tools
"""


def get_page(link):
    """
    Gets the page content from a given link; gives it a second try
    in case internet connection is lost for a moment to result in
    timeout error.
    :param link:
    :return: page content, or None if the link doesn't work
    """
    try:
        page = requests.get(link)
    except TimeoutError:
        page = requests.get(link)
    if page.status_code != 200:
        return None
    return BeautifulSoup(page.content, 'html.parser')


"""
Selenium Tools
"""


def get_driver(driver_loc, headless):
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(driver_loc, options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(1500, 950)
    return driver


"""
Other Tools
"""


def get_last_date(loc):
    """
    Finds last month where basketball-reference has been scraped.
    :return: integer of format YYYYMM
    """
    files = os.listdir(loc)
    max_date = 200000

    for file in files:
        if not file.startswith('.'):
            year = file[-8:-4]
            month = time.strptime(file[-11:-8], '%b').tm_mon
            month = '0' + str(month) if month < 10 else str(month)
            combo = int(year + month)

            # if it's the most recent month
            if combo > max_date:
                max_date = combo

    return str(max_date)


def arg_parse(args):
    if len(args) == 1:
        print("Must supply argument of either:")
        print('      1) "full"; downloads all data from 2006 season to present')
        print('      2) "update"; downloads data that is not yet archived')
    elif args[1] not in ['full', 'update']:
        print('Argument must be either "full" or "update"')
    else:
        return args[1]


def merge(loc, prefix):
    """
    Creates a single data frame that merges all the individual CSVs.
    :param loc: the directory of the CSV files to be merged.
    :param prefix: prefix of collection of CSVs that need to be merged
    :return: single master file as a pandas data frame
    """
    file_list = [file for file in os.listdir(loc) if not file.startswith('.') and file.startswith(prefix)]
    all_csv = []
    for file in file_list:
        all_csv.append(pd.read_csv(loc + file, index_col='Index', header=0))
    return pd.concat(all_csv, ignore_index=True, sort=False)
