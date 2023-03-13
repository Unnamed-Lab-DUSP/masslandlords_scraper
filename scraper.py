#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests import get
from csv import DictWriter
from datetime import datetime
from datetime import timedelta
from time import sleep
from os import path

START_DATE = datetime.strptime("2020-10-24", "%Y-%m-%d")
URL_BASE = "https://masslandlords.net/policy/eviction-data/filings-week-ending-"
RESULTS = []
OUT_FILE = path.join("results", "weekly-filings.csv")

def create_weeks_list(start_date, end_date = False):
    """
    Create a list of week starts between a start and end date.
    """
    if not end_date:
        end_date = datetime.today()
    date_list = []
    weekly = start_date
    while weekly <= end_date:
        print("he")
        date_list.append(weekly.strftime("%Y-%m-%d"))
        weekly += timedelta(days=7)
    return date_list

def parse_page(page_request):
    """
    Parses requested page.
    """
    results = {
        "E": 0,
        "C": 0,
        "MS": 0,
        "NE": 0,
        "SE": 0,
        "W": 0
    }
    page = page_request.text.split()
    for i in range(len(page)): 
        if page[i] == "central" and page [i-1] != "bmc":
            results["C"] = page[i+1]
        if page[i] == "eastern" and page[i+1] != "hampshire":
            results["E"] = page[i+1]
        if page[i] == "metro_south":
            results["MS"] = page[i+1]
        if page[i] == "northeast":
            results["NE"] = page[i+1]
        if page[i] == "southeast":
            results["SE"] = page[i+1]
        if page[i] == "western":
            results["W"] = page[i+1]
    return results

def run():
    print(create_weeks_list(START_DATE))
    for date in create_weeks_list(START_DATE):
        request = get(URL_BASE + date)
        print(f"Attempting to download {date}.")
        if request.status_code == 404:
            print(f"😞 No data available for {date}. 😞")
            continue
        else:
            results = parse_page(request)
            results['date'] = date
            RESULTS.append(results)
        # Be courteous.
        sleep(1.5)

    with open(OUT_FILE, "w") as csvfile:
        # creating a csv writer object
        writer = DictWriter(
            csvfile, 
            fieldnames = ["date", "E", "C", "MS", "NE", "SE", "W"]
            ) 
        # Write the header.
        writer.writeheader()
        # writing the data rows 
        writer.writerows(RESULTS)

if __name__ == "__main__":
    run()