#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from datetime import timedelta
from time import sleep


START_DATE = datetime.strptime("2020-10-24", "%Y-%m-%d")
URL_BASE = "https://masslandlords.net/policy/eviction-data/filings-week-ending-"
RESULTS_DICT = {} ##key: date, value: evictions

def create_weeks_list(start_date, end_date = False):
    """
    Create a list of week starts between a start and end date.
    """
    if not end_date:
        end_date = datetime.today()
    date_list = []
    weekly = start_date
    while weekly <= end_date:
        date_list.append(weekly.strftime("%Y-%m-%d"))
        weekly += timedelta(days=7)
    return date_list

def parse_page(page_request):
    """
    Parses requested page.
    """
    results = {
        "W": 0,
        "E": 0,
        "C": 0,
        "SE": 0,
        "NE": 0,
        "MS": 0
    }
    page = page_request.text.split()
    for i in range(len(page)): 
        if page[i] == "metro_south":
            results["MS"] = page[i+1] 
        if page[i] == "eastern" and page[i+1] != "hampshire":
            results["E"] = page[i+1] 
        if page[i] == "western":
            results["W"] = page[i+1]
        if page[i] == "southeast":
            results["SE"] = page[i+1]
        if page[i] == "northeast":
            results["NE"] = page[i+1]
        if page[i] == "central" and page [i-1] != "bmc":
            results["MS"] = page[i+1]
    return results

for date in create_weeks_list(START_DATE):
    request = requests.get(URL_BASE + date)
    if request.status_code == 404:
        print(f"No data available for {date}.")
        continue
    else:
        RESULTS_DICT[date] = parse_page(request)
    sleep(1.5)
    

