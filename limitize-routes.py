from gtfslite.gtfs import GTFS
from ted.gtfs import remove_routes_from_gtfs
import pandas as pd
import zipfile
import numpy as np
import datetime as dt
import os

DEBUG_MODE = False

premium_route_id = pd.read_csv('premium_routes.csv')
premium_route_id_list = (premium_route_id.iloc[:,0]).tolist()

#TODO need to figure out how to make premium routes list into ID's

#converts fairfax-connector/295__393
def route_tag_to_id(tag: str):

    return id


#specifies the entry and output folders
entry_path = '../region/WAS/gtfs'
ct = str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
output_path = os.path.join(os.getcwd(),'run-' + ct)
os.mkdir(output_path)

dated_entries = os.listdir(entry_path)
index1 = 0

#Iterate through all dated entries
while index1 < len(dated_entries):
    curr_dated_entry = dated_entries[index1]

    #Make target output folder, this will look like: "../ted-data/runs/20XX-XX-XX-LIMITED"
    dated_output_path = os.path.join(output_path, curr_dated_entry + '-limited') 
    os.mkdir(dated_output_path)

    zip_entries = os.listdir(os.path.join(entry_path, curr_dated_entry))
    index2 = 0

    #Iterate through .zip entries
    while index2 < len(zip_entries):

        #Find entry zip folder
        curr_zip_entry = zip_entries[index2]
        curr_zip_dir = os.path.join(entry_path, curr_dated_entry, curr_zip_entry)

        if DEBUG_MODE: print('Currently parsing: ' + curr_dated_entry + ': ' + curr_zip_entry)

        try:
            remove_routes_from_gtfs(curr_zip_dir, dated_output_path, premium_route_id_list)
        except zipfile.BadZipFile:
            if DEBUG_MODE: print(curr_zip_entry, "is not a zipfile, skipping...")

        index2 += 1

    if DEBUG_MODE: print('\nFinished parsing: ' + curr_dated_entry + '\n')
    index1 += 1

if DEBUG_MODE: print('done!')


#1. Open the zipfile using the most recent version of GTFS-Lite
#2. Using the routes identified, use delete_routes() on the package and save as a modified file with a -LIMITED tag
#3. Upload the resulting limited GTFS files to the GDrive