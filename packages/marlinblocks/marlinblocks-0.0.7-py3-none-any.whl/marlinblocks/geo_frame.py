#!/usr/bin/env
# Imports
from marlinblocks.std_imports import *
import requests, json
import datetime

#
#
# Copyright RS Aqua and Marlin 2023 www.rsaqua.co.uk r.tandon@rsaqua.co.uk
# -------------------------------------------------------------------------------------
# Written by Rahul Tandon, r.tandon@rsaqua.co.uk
#
#

"""_summary_


"""


def rs_api_t_convert(c_time : datetime = None):
    t_string = c_time.strftime('%Y%m%d_%H%M%S.%f')
    # print (f'converted time : {t_string}')
    return t_string


from marlinblocks.acoustic_frame import *

class geo_frame(object):
    def __init__(self, acoustic_data : acoustic_frame = None):
        self.hit = False
        self.acoustic_frame_data = acoustic_data
        self.num_hit = 0
        self.distance = 0
        self.d_limit = 0
        self.src_time = 0
        self.hit_data = []
        
        
    def run(self):
        
        print ( self.acoustic_frame_data.start_time,  self.acoustic_frame_data.end_time)
        hit = False
        num_hit = 0
        # We have t and location. Look for an AIS hit.
        # Use Marlin AIS Data API. Look at documentation for info.
        
        print (f'1 : {self.acoustic_frame_data.start_time}')
        
        src_time = rs_api_t_convert(self.acoustic_frame_data.start_time)
        print (f'2 : {src_time}')
        
        
        send_data = {
            "dlimit" : 3,
            "src_lat" : self.acoustic_frame_data.location['latitude'],
            "src_long" : self.acoustic_frame_data.location['longitude'],
            "src_time" : src_time,
            "tlimit" : 15,
            "start_time" : self.acoustic_frame_data.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time" : self.acoustic_frame_data.end_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        
        api_address = "https://vixen.hopto.org/rs/api/v1/data/ais/"
       
        #send request & evaluate hit
        rprint (json.dumps(send_data))
        try:
            r = requests.post(api_address, data=json.dumps(send_data))
            # rprint (r)
            # rprint(json.loads(r.content))
            results = json.loads(r.content)
            
            num_hit = results['num_unique']
            # distance = results['distance']
            # d_limit = results['d_limit']
            # src_time = results['src_time']
            
            # rprint (f'number of hits : {num_hit}')
            self.number_hits = num_hit
        # self.distance = distance
        except:
            print("[geo_frame run()] http: fail]")
           
       
        
        hit_data = {}
        if num_hit > 0:
            # print (f"Min time : {results['min_delta_t']} of {send_data['tlimit']}")
        
            # print (results['data'])
            hit = True
            self.hit = True
            
            
         
            
            
            for hits in results['data']:
                hit_data = {}
                hit_data['mmsi'] = hits['mmsi']
                hit_data['name'] = hits['vessel_name']
                hit_data['t_lat'] = hits['t_lat']
                hit_data['t_long'] = hits['t_long']
                new_mmsi = str(hit_data['mmsi'])
                hit_data['cpa'] = results['mmsi_distance_tracker'][new_mmsi]
                hit_data['cpa_time'] = results['mmsi_time_tracker'][new_mmsi]
                hit_data['distance'] = hits['distance']
                hit_data['vessel_type'] = hits['vessel_type']
                hit_data['d_limit'] = hits['d_limit']
                hit_data['delta_t'] = hits['delta_t']
                
                self.hit_data.append(hit_data)
                
            self.num_hit = num_hit
            
        
        # print (self.hit_data)
        
        self.hit = hit
        self.num_hit = num_hit
        # self.hit_data = hit_data
        
        return hit
    
    
        