#!/usr/bin/python
import json
from utils import *
from glob import glob
import csv
import sys
import os
from xr import *

from rich import pretty
from rich.console import Console
pretty.install()
from rich import print as rprint
# ---------------------
# header
# ---------------------
print("AIS Plotter. RS AQUA")

# ---------------------
# Load AIS data into json structure
# ---------------------
ais_filenames = glob('../../data/ais/*.csv')


header_data = {}
csv_data = []

# load AIS json/CSV data
# with open(ais_filename, 'r') as j:
#     ais_json = json.loads(j.read())
counter = 0
with open(ais_filenames[0], newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if counter == 0:
            hdr_indx = 0;
            for hdr in row:
                header_data[row[hdr_indx]] = hdr_indx
                hdr_indx += 1 
                
            #rprint (header_data)
            counter+=1
            continue
        csv_data.append(row)

# ---------------------
# Declare and define global vars for target data
# ---------------------

# vector vessel AIS ids
target_ids = []
timestamps = []
speeds = {}
numnber_track_points = {}
# target track data
track_data = {}

# define vars

# for page in ais_json['pages']:
#     for target in page['data']:
#         target_id = target['vessel_id']
#         if target_id not in target_ids:
#             target_ids.append(target_id)
#             track_data[target_id] = []
#         target_track_data = {}
#         target_track_data['time_stamp'] = target['timestamp']
#         target_track_data['geometry'] = target['geometry']
#         track_data[target_id].append(target_track_data)

for row in csv_data:
    target_name = row[header_data['name']]
    target_id = row[header_data['mmsi']]
    if target_id not in target_ids:
        target_ids.append(target_id)
        track_data[target_id] = []
    target_track_data = {}
    target_track_data['name'] = target_name
    target_track_data['timestamp'] = row[header_data['timestamp']]
    timestamps.append(row[header_data['timestamp']])
    target_track_data['latitude'] = float(row[header_data['latitude']])
    target_track_data['longitude'] = float(row[header_data['longitude']])
    target_track_data['mmsi'] = row[header_data['mmsi']]
    track_data[target_id].append(target_track_data)
    
    # rprint(target_track_data)
    

# sorted(timestamps, key=lambda d: map(int, d.split('-')))
timestamps.sort()

# --debug
rprint(f'{len(target_ids)} targets loaded from AIS between {timestamps[0]} and {timestamps[len(timestamps)-1]}')
# rprint(timestamps[0], timestamps[len(timestamps)-1])

# rprint(track_data['32001bbf-20d1-45b1-a639-2213b07dbd6e'])
# ---


ref_loc = {}
ref_loc['latitude'] = 50.719344
ref_loc['longitude'] = 0.548028

for target in target_ids:
    # BuildKMLFileCSV(track=track_data[target], id=target)
    # AnimateMapTrack(track=track_data[target], target_name=target)
    #RunTrack(track_data[target], target)
    print (len(track_data[target]))
    a, b = BuildDistanceProfile(track_data[target], ref_loc)
    
    print (b['nearest'])
    exit()
    