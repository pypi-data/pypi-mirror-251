"""Build a marlin data run for simulation or ML.
"""
    
# import marlin_data adapter -> provides both acccess to: 
#   1. signature and simulation dataclass 
#   2. data feed iterable for iterating through feed data
#   3. build acoustic dat
#   4. run model
from marlin_data.marlin_data import *

# datetime import
from datetime import datetime

# numpy import
import numpy as np

# formatting
from rich import pretty
from rich.console import Console
pretty.install()
from rich import print as rprint
from rich.progress import Progress

def run_model():
    
    """ Main framework run routine. Demonstrate:
        1. Download simualtion and signature data
        2. Create a datafeed
        3. Run data through a model
    
    """
    # --------------------------------------------------------------
    # --- 1. Download data from RSA signature and simualtion db -  |
    # --------------------------------------------------------------
    rprint ("Building Adapter")
    # create the data adapter
    data_adapter = MarlinData()
    
    # download signature data
    rprint(f"[Downlaod Signature Snapshots]")
    data_adapter.download_signatures()
    
    # download simulation snapshots
    rprint(f"[Downlaod Simulation Snapshots]")
    data_adapter.download_simulation_snapshots()
    
    rprint (f"Data Download complete.")
    rprint (f"Number of signature samples downloaded: {data_adapter.number_signatures}")
    rprint (f"Number of marlin data acquisition runs: {data_adapter.number_runs}")
    
    # ---------------------------------------------------------------
    # --- 2. Build datafeed ---                                     |
    # ---------------------------------------------------------------
    rprint ("Building Datafeed")
    
    # create a MarlinDataStreamer
    data_feed = MalrinDataStreamer()
    # initilise the simulation datafeeder with downloaded data in data_adapter
    data_feed.init_data(data_adapter.simulation_data, data_adapter.simulation_index)
    
    for data_inst in data_feed:
        print (f"location {data_inst.meta_data['location_name']} between {data_inst.meta_data['data_frame_start']} and {{data_inst.meta_data['data_frame_end']}}")
        
        # build frame times
        frame_start_dt = datetime.strptime(data_inst.meta_data['data_frame_start'], '%y%m%d_%H%M%S.%f')
        frame_end_dt = datetime.strptime(data_inst.meta_data['data_frame_end'], '%y%m%d_%H%M%S.%f')
        time_delta = timedelta(seconds = data_inst.meta_data['frame_delta_t'])
        
        # get frequency data - numpy array
        freq_data = data_inst.frequency_ts_np
        freq_data_vec_length = len(freq_data)
        
        
        # ---------------------------------------------------------------
        # --- 3. Build Acoustic framedata---                             |
        # ---------------------------------------------------------------
    
        
        
        # ---------------------------------------------------------------
        # --- 4. Run Model ---                                          | 
        # ---------------------------------------------------------------
    
        
        
        
        
        
        
        
        
        
    
    
    
    
run_model()
    
    
