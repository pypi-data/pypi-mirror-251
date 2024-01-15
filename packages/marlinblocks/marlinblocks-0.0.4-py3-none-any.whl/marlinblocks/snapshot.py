#!/usr/bin/env python3
# Imports
from marlinblocks.std_imports import *

#
#
# Copyright RS Aqua and Marlin 2023 www.rsaqua.co.uk r.tandon@rsaqua.co.uk
# -------------------------------------------------------------------------------------
# Written by Rahul Tandon, r.tandon@rsaqua.co.uk
#
#

"""_summary_


"""

from marlinblocks.acoustic_frame import *
from marlinblocks.geo_frame import *
from marlinblocks.model_frame import *
import requests
import random
import json
import base64

class snapshot_container(object):
    
    def __init__(self):
        
       
        self.cpa_vessel     = {}    #mmsi -> distance
        self.cpa_time       = {}    #mmsi -> time
        self.cpa_ids        = {}    #mmsi -> ss_ids
        self.snap_shots     = []  
        
    
    def update(self, snapshot):
        
        for vessel_hit in snapshot['geo_hit_data']:
            vessel_mmsi = vessel_hit['mmsi']
            vessel_distance = vessel_hit['cpa']
            vessel_cpa_time = vessel_hit['cpa_time']
            
            
            if vessel_mmsi in self.cpa_vessel:
                if vessel_distance < self.cpa_vessel[vessel_mmsi]:
                    self.cpa_vessel[vessel_mmsi] = vessel_distance
                    self.cpa_time[vessel_mmsi] = vessel_cpa_time
                    self.cpa_ids[vessel_mmsi] = snapshot['ss_id']
            else:
                self.cpa_vessel[vessel_mmsi] = vessel_distance
                self.cpa_time[vessel_mmsi] = vessel_cpa_time
                self.cpa_ids[vessel_mmsi] = snapshot['ss_id']
                               
            
        
    def send_to_db(self, run_id : str = "no_id"):
       
        data = {
                'cpa_distance'  : self.cpa_vessel,
                'cpa_time'      : self.cpa_time,
                'cpa_index'     : self.cpa_ids
                
        }
       
        send_data = {
            'snap_cpa_data' : json.dumps(data),
            'run_id' : run_id
        }
        
        # print (json.dumps(send_data))
        
        api_address = "https://vixen.hopto.org/rs/api/v1/data/snapshot/overview"
        print(api_address)
        try:
            r = requests.post(api_address, data=json.dumps(send_data))
        except:
            print("[update_run_progress http: fail]")
        # print (r)
         
        
    

    


class snapshot(object):
    """_summary_

    Args:
        object (_type_): _description_
    """    
    def __init__(self, batch_id : int = 0):
        self.location = ""
        self.model_data = None
        self.acoustic_data = None 
        self.geo_data = None
        self.batch_id = batch_id
        self.environment_acoustic_frame = None
        self.snap_id = random.randrange(0,1000000)
    
    def build(self, decision_acoustic_data : acoustic_frame = None, environment_acoustic_data : acoustic_frame = None, geo_data : geo_frame = None, model_data : model_frame = None ,location : str = ""):
        """_summary_

        Args:
            acoustic_data (acoustic_frame, optional): _description_. Defaults to None.
            geo_data (geo_frame, optional): _description_. Defaults to None.
            model_data (model_frame, optional): _description_. Defaults to None.
        """        
        self.acoustic_data = decision_acoustic_data
        self.environment_acoustic_frame = environment_acoustic_data
        self.geo_data = geo_data
        self.model_data = model_data
        self.location = location
    
    
    def hit(self, run_id : str = "no_id"):
        
        self.buildJson()
        self.save()
        self.send_to_db(run_id)
    
    def buildJson(self):
        
        self.out_json = {
        'hits'                          :   {

                                                'model_data'    : self.model_data.hit,
                                                'geo_data'      : self.geo_data.hit

                                            },
        'ss_id'                         : self.snap_id,
        'sample_rate'                   : self.acoustic_data.sample_rate,
        'data_frame_start'              : self.acoustic_data.start_time.strftime('%y%m%d_%H%M%S.%f'),
        'data_frame_end'                : self.acoustic_data.end_time.strftime('%y%m%d_%H%M%S.%f'),
        'data_frame_start_env'          : self.environment_acoustic_frame.start_time.strftime('%y%m%d_%H%M%S.%f'),
        'data_frame_end_env'            : self.environment_acoustic_frame.end_time.strftime('%y%m%d_%H%M%S.%f'),
        
        'data_receiver_location'        : self.acoustic_data.location,
        'data_receiver_location_name'   : self.acoustic_data.location_name,
        'data_live_sample_number'       : self.acoustic_data.sample_number,
        'data_delta_time'               : self.acoustic_data.frame_delta_t,
        'spec_images'                   : self.acoustic_data.spec_images,
        'spec_images_html'              : self.acoustic_data.spec_images_html,
        'geo_hit_number'                : self.geo_data.num_hit,
        'geo_hit_data'                  : self.geo_data.hit_data,
        'environment_images'            : self.environment_acoustic_frame.spec_images,
        'environment_spec_images_html'  : self.environment_acoustic_frame.spec_images_html,
        'frequency_images'              : self.acoustic_data.wave_images,
        'frequency_images_html'         : self.acoustic_data.wave_images_html
        
        
    }
    
    

    def __str__(self):
        self.out_json = {
            'hits'                          :   {

                                                    'model_data'    : self.model_data.hit,
                                                    'geo_data'      : self.geo_data.hit

                                                },
            'data_frame_start'              : self.acoustic_data.start_time.strftime('%y%m%d_%H%M%S.%f'),
            'data_frame_end'                : self.acoustic_data.end_time.strftime('%y%m%d_%H%M%S.%f'),
            'data_receiver_location'        : self.acoustic_data.location,
            'data_receiver_location_name'   : self.acoustic_data.location_name,
            'data_live_sample_number'       : self.acoustic_data.sample_number,
            'data_delta_time'               : self.acoustic_data.frame_delta_t,
            'spec_images'                   : self.acoustic_data.spec_images,
            'spec_images_html'              : self.acoustic_data.spec_images_html,
            'geo_hit_number'                : self.geo_data.num_hit
            # 'geo_distance'                  : self.geo_data.distance,
            # 'd_limit'                       : self.geo_data.d_limit,
            # 'src_time'                      : self.geo_data.src_time
            
            
        }
        
        
    
    def save(self):
        
        
        start_time = self.acoustic_data.start_time.strftime('%y%m%d_%H%M%S.%f')
        location = self.acoustic_data.location_name
        delta_t = self.acoustic_data.frame_delta_t
        
        filename = f"snapshot_{start_time}_{location}_{delta_t}.json"
        location = f"/home/vixen/html/rs/snapshots/{self.batch_id}/json/"
        with open(location+filename, 'w') as fp:
            json.dump(self.out_json,fp )
        
    
    def send_to_db(self, run_id : str = "no_id"):
        ss_send_data = json.dumps(self.out_json)
        send_data = {
            'sample_rate' : self.acoustic_data.sample_rate,
            'snapshot_id' :  self.snap_id,
            'location' : self.acoustic_data.location_name,
            'timeframe_start': self.acoustic_data.start_time.strftime('%y-%m-%d %H:%M:%S.%f'),
            'timeframe_end': self.acoustic_data.end_time.strftime('%y-%m-%d %H:%M:%S.%f'),
            'run_id' : run_id,
            'snapshot_data' : ss_send_data
        }
        
        # print (json.dumps(send_data))
        
        api_address = "https://vixen.hopto.org/rs/api/v1/data/snapshot/new"
        try:
            r = requests.post(api_address, data=json.dumps(send_data))
        except:
            print("[sending new snapshot http: fail]")
        
        #serialise corresponding acoustic raw data
        # acoustic_serial_data = self.acoustic_data.Save()
        # acoustic_serial_data['snapshot_id'] = self.snap_id
        # data_shape = len(acoustic_serial_data['raw_data'])
        # print (f' shape of raw data  : {data_shape}')
        # # acoustic_serial_data['raw_data'] = []
        # # print (json.dumps(acoustic_serial_data))
        # print ("Sending snapshot data")
        # acoustic_serial_data['raw_data'] = np.array([1,2,3,4]).tobytes()
        # # print (json.dumps(acoustic_serial_data))
        
        save_location = f"/home/vixen/html/rs/snapshots/data/{self.snap_id}"
        cmd = f'mkdir {save_location}'
        
        os.system(cmd)
        
        raw_data_fn = f"{save_location}/raw_.data"
        self.acoustic_data.frame_raw_data.tofile(raw_data_fn)
        
        save_location_url = f"https://vixen.hopto.org/rs/snapshots/data/{self.snap_id}"
        raw_data_fn_url = f"{save_location_url}/raw_.data"
        
        acoustic_serial_data = {
            'raw_data' : raw_data_fn,
            'raw_data_url' : raw_data_fn_url,
            'frequencies'   : [],
            'amplitude_data': [],
            'time_bins'     : [],
            'frequency_bins': []
        }
        
        api_address = f"https://vixen.hopto.org/rs/api/v1/data/snapshot/data/{self.snap_id}"
        # print (api_address)
        
        # # data_str = base64.b64encode(acoustic_serial_data['raw_data'])
        # # acoustic_serial_data['raw_data'] = data_str
        # print ((acoustic_serial_data['raw_data']))
        
        try:
            r = requests.post(api_address, data=json.dumps(acoustic_serial_data))
            print (f'status : {r.status_code}')
            print (r.text)
        except:
            print("send snapshot data http: fail]")
        
        #send binary data to data storage
        
            
        
            
        
        
        
        
        
        
        