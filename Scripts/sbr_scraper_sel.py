"""
This program will scrape all NBA betting data from
www.sportsbookreview.com using Selenium.
The files are saved as CSV in a folder for each individual
month.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from multiprocessing import Pool
import time
import os
import datetime as dt
import numpy as np
import calendar

# global variable
BASE_URL = 'https://www.sportsbookreview.com/betting-odds/nba-basketball/'


def get_dates():
    """
    Function that gets a pandas series of all the dates to be
    searched.
    :return: numpy array with dates of games in format 'YYYYMMDD'
    """
    loc = './../Data/bask_ref_csvs/'
    file_list = [file for file in os.listdir(loc) if file.startswith('game')]
    all_csv = []
    for file in file_list:
        all_csv.append(pd.read_csv(loc + file, index_col='Index', header=0))
    df = pd.concat(all_csv, ignore_index=True, sort=False)
    df.date = df.date.apply(lambda x: dt.datetime.strptime(x, "%I:%M %p, %B %d, %Y"))
    dates = df.date.apply(lambda x: str(x.year) + (str(x.month) if x.month > 9 else '0' + str(x.month)) + (str(x.day) if x.day > 9 else '0' + str(x.day)))
    dates = dates.loc[dates.astype(int) > 20061000]
    return dates.unique()


def update(df, date, lists):
    """
    Updates the data frame storing all the data after each day.
    :param df:
    :param date:
    :param lists: list of lists attained by day_loop()
    :return: updated data frame
    """
    for bet_type in ['p', 'm', 't']:
        for length_type in ['full', 'first', 'sec']:
            lst = lists.pop(0)
            for game in range(int(len(lst) / 24)):
                df.loc[len(df)] = [date, bet_type, length_type, game] + lst[(game * 24):((game + 1) * 24)]
    return df


def day_loop(driver, date, sleep, run):
    """
    For a give day, will return a list of lists, where each individual list
    contains data for a bet type + length type combination on given date.
    :param driver: chromedriver
    :param date: in format 'YYYYMMDD'
    :param sleep: to ensure page loads, needs a sleep
    :param run: a counter to limit number of re-attempts for a failing page
    :return: list of lists
    """
    # list that will hold the entry count for bet type/length type combination;
    # should equal (10 (# books) + 2 (wager + opener)) * n_games * 2 (teams per game)
    game_check = []

    full_list = []
    for bet_type in ['pointspread/', 'money-line/', 'totals/']:
        for length_type in ['', '1st-half/', '2nd-half/']:      # blank length is for full game
            driver.get(BASE_URL + bet_type + length_type + '?date=' + date)

            time.sleep(sleep)

            test = driver.find_elements_by_class_name('_1QEDd')
            singles = [t.text for t in test]
            game_check.append(len(singles))
            full_list.append(singles)

    # checks that everything was scraped correctly
    uniques = len(set(game_check))  # = 1 if all pages give same number of data entries
    if uniques != 1:
        if uniques > 1:  # unequal number of entries for different pages,
            if run < 3:    # need to re-run with a longer sleep interval.
                text_file = open("drive/My Drive/scraping/Output.txt", "a")
                print('\nGoing round {}'.format(run + 2), file=text_file)
                text_file.close()
                full_list = day_loop(driver, date, sleep + 0.15, run + 1)
            else:
                text_file = open("drive/My Drive/scraping/Output.txt", "a")
                print('\nCould not get match entries for {}'.format(date),
                      file=text_file)
                text_file.close()
                return None
        elif 0 in set(game_check):
            text_file = open("drive/My Drive/scraping/Output.txt", "a")
            print('\nNo games on date: {}'.format(date), file=text_file)
            text_file.close()
            return None
    return full_list


def day_caller(month_list):
    """
    Will initialize a data frame to store data, initialize a
    webdriver to scrape data, call dates for given month linearly.
    :param month_list: list with all game dates for a given month
    :return:
    """
    column_names = ['date', 'bet', 'length', 'game_num', 'aw', 'hw', 'ao', 'ho',
                    'ab1', 'hb1', 'ab2', 'hb2', 'ab3', 'hb3', 'ab4', 'hb4',
                    'ab5', 'hb5', 'ab6', 'hb6', 'ab7', 'hb7', 'ab8', 'hb8',
                    'ab9', 'hb9', 'ab10', 'hb10']
    df = pd.DataFrame(columns=column_names)

    # configure the driver
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome('./../Misc/chromedriver', options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(1500, 950)

    # loop every day for the month
    for date in month_list:
        list_of_lists = day_loop(driver, date, 0.15, 0)
        if list_of_lists is not None:
            df = update(df, date, list_of_lists)

    # push monthly data frame to a csv
    year = str(month_list[0][:4])
    month = calendar.month_abbr[int(month_list[0][4:6])]
    df.to_csv('./../Data/sbr_csvs/' + month + year + '.csv', index_label='Index')


def main():
    """
    - Gets all dates to scrape on SBR (format: YYYYMMDD)
    - Moves through years sequentially
    - For given year, will scrape each month in parallel
    :return:
    """
    dates = get_dates()
    dates.sort()
    completed = os.listdir('./../Data/sbr_csvs/')

    for year in np.arange(2006, 2019):
        year_list = []

        for mon in np.arange(1, 13):

            # if not already done
            if calendar.month_abbr[mon] + str(year) + '.csv' not in completed:
                month = '0' + str(mon) if mon < 10 else mon

                # get every game day for the month and append if non-empty
                month_dates = [date for date in dates if str(year) + str(month) == date[:6]]
                if len(month_dates) != 0:
                    year_list.append(month_dates)

        # process each individual month for a given year in parallel
        if len(year_list) > 0:
            print('Starting {}'.format(year))
            pool = Pool(processes=len(year_list))
            pool.map(day_caller, year_list)


if __name__ == '__main__':
    if 'README.md' in os.listdir('.'):
        os.chdir('Scripts/')
    main()






