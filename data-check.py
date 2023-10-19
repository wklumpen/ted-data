from gtfslite.gtfs import GTFS
from ted.gtfs import get_all_stops, summarize_gtfs_data
import pandas as pd
import numpy as np
import zipfile
import datetime as dt
import os

gtfs_folder = "../region/WAS/gtfs/"
agencies_file = '../ted-data/agencies.csv'
agency_stops_masterlist = {
    "date": [],
    "total_stops": [],
    "total_unique_stops": [],
    "total_invalid_feeds": [],
}
#summary = summarize_gtfs_data(gtfs)

feed_check_list = pd.read_csv(agencies_file)

for date in os.listdir(gtfs_folder):
    print(f"\nNow parsing {date}...\n")
    date_file = os.path.join(gtfs_folder,date)
    stops = get_all_stops(date_file)

    #get a list of the unique stops in dated feed
    stop_id_list = (stops.loc[:,'stop_id'])
    unique_stop_id_list = pd.unique(stop_id_list)
    invalid_feed_id_list = []
    stop_id_list = stop_id_list.tolist()
    unique_stop_id_list = pd.unique(unique_stop_id_list)

    agencies = os.listdir(date_file)
    #make a list with invalid agencies
    for agency in agencies:
        if agency.startswith('._') and (agency.endswith('.zip') or agency.endswith('.csv')):
            invalid_feed_id_list.append(agency)
    
    #get total amount of stops and unique stops
    total_stops = len(stop_id_list)
    total_unique_stops = len(unique_stop_id_list)
    total_invalid_feeds = len(invalid_feed_id_list)

    #add data to masterlist
    agency_stops_masterlist['date'].append(date)
    agency_stops_masterlist['total_stops'].append(total_stops)
    agency_stops_masterlist['total_unique_stops'].append(total_unique_stops)
    agency_stops_masterlist['total_invalid_feeds'].append(total_invalid_feeds)

    print(f"\nDone parsing, {date} has...\nTotal stops: {total_stops}\nTotal unique stops: {total_unique_stops}\nTotal invalid feeds: {total_invalid_feeds}")

masterlist_df = pd.DataFrame(agency_stops_masterlist)
print(f"\nMaster List:\n{masterlist_df}")

#Pseudo:
#go into dated ntry and look through all feed 
# use get_all_stops to get all the stops
# look into what summarize gtfs data does using summarize_gtfs_data(gtfs)
# - add total # of stops per each agency
# - add total # of routes
# - List all unique route_type in routes.txt
# - make reccomendations?? or flag feeds that dont have all data

