#!/usr/bin/env python3
# Imports
from std_imports import *
import argparse
import requests
import os, psutil

#
#
# Copyright RS Aqua and Marlin 2023 www.rsaqua.co.uk r.tandon@rsaqua.co.uk
# -------------------------------------------------------------------------------------
# Written by Rahul Tandon, r.tandon@rsaqua.co.uk
#
#

"""_summary_


"""

# Design args parser
parser = argparse.ArgumentParser(description = "RS Aqua acoustics descriminator MARLIN project.")
parser.add_argument('filename',metavar='filename', type=str, help='Filename of acoustic data to run.', nargs=1)
parser.add_argument('frame_size',metavar='framesize', type=int, help='Integer value of data size in individual acoustic frames.', nargs=1)
parser.add_argument('frequency_frame_size', metavar='frequency_frame_size', type=int, help='Integer value of frequency bucket size. e.g. 200Hz will resample frequency data into 200Hz buckets for signal and stat analysis.', nargs=1)
parser.add_argument('frequency_target_min',  metavar='frequency_target_min', type=int, help='Integer value of lower bound of frequency range of interest', nargs=1)
parser.add_argument('frequency_target_max', metavar='frequency_target_max', type=int, help='Integer value of upper bound of frequency range of interest', nargs=1)
parser.add_argument('min_memory', metavar='min_memory', type=int, help='Integer value of bots minimum memory range.', nargs=1)
parser.add_argument('max_memory', metavar='max_memory', type=int, help='Integer value of bots maximium memory range.', nargs=1)
parser.add_argument('run_id',  metavar='run_id', type=str, help='Unique ID of run.', nargs=1)
parser.add_argument('location',  metavar='location', type=str, help='Location of source of run.', nargs=1)

# Read args
# args = parser.parse_args()
# print(args)
# filename = args.filename
# sample_size = args.frame_size
# freq_frame_size = args.frequency_frame_size
# freq_target_max = args.frequency_target_max
# freq_target_min = args.frequency_target_min
# min_memory = args.min_memory
# max_memory = args.max_memory 

filename = sys.argv[2]
sample_size = int(sys.argv[4]) * 22050
freq_frame_size = int(sys.argv[6])
freq_target_max = int(sys.argv[8])
freq_target_min = int(sys.argv[10])
min_memory = int(sys.argv[12])
max_memory =int(sys.argv[14])
run_id =(sys.argv[16])
location = (sys.argv[18])

run_data = {
    'filename' : filename,
    'sample_size' : sample_size,
    'freq_frame_size' : freq_frame_size,
    'freq_target_max' : freq_target_max,
    'freq_target_min' : freq_target_min,
    'min_memory' : min_memory,
    'max_memory' : max_memory,
    'run_id'    : run_id,
    'location'  : location
}


#get start time of file
rprint (run_data)




def send_run_data(run_data : {} = None) -> None:
    ss_send_data = json.dumps(run_data)
    send_data = {
        'run_id' : run_id,
        'run_data' : ss_send_data
    }
        
        
    print(json.dumps(send_data))   
    api_address = "https://vixen.hopto.org/rs/api/v1/data/newrun"
    
    try:
        r = requests.post(api_address, data=json.dumps(send_data))
    except:
        rprint("[update_run_progress http: fail]")
    
def update_run_progress(current_index : int = 0, total_index : int = 0, run_id : str = ""):
    
    send_data = {
        'run_id' : run_id,
        'current_index' : current_index,
        'total_index' : total_index
    }    
    
    api_address = "https://vixen.hopto.org/rs/api/v1/data/runupdate"
    #rprint(json.dumps(send_data))
    try:
        r = requests.post(api_address, data=json.dumps(send_data))
    except:
        rprint("[update_run_progress http: fail]")
        

def get_start_date_time(filename : str = ""):
    """_summary_

    Args:
        filename (str, optional): _description_. Defaults to "".

    Returns:
        _type_: _description_
    """    
    start_time = None
    start_date = None
    
    #../../data/acoustic/_20230712_015341_310.wav
    if filename == "":
        rprint("no filename given")
        split_file_name = audio_files[0].split('_')
    else:
        rprint(filename)
        split_file_name = filename.split('_')
        rprint(split_file_name)
    
    
    date_string = split_file_name[1]
    time_string = split_file_name[2]
    ms_string = split_file_name[3]
    ms_str_split = ms_string.split('.')
    ms_str_time = ms_str_split[0]


    # date_string_arr = date_string.split('')
    date_string_arr = list(date_string)
    # rprint (date_string_arr)
    yr_str = ''.join(date_string_arr[:4])
    # rprint(yr_str)
    month_str = ''.join(date_string_arr[4:6])
    # rprint(month_str)
    day_str = ''.join(date_string_arr[6:8])
    # rprint(day_str)

    # time_string_arr = time_string.split('')
    time_string_arr = list(time_string)
    #hr
    # rprint(time_string_arr)
    hr_str = ''.join(time_string_arr[:2])
    # rprint(hr_str)
    #min
    min_str = ''.join(time_string_arr[2:4])
    # rprint(min_str)
    #second
    sec_str = ''.join(time_string_arr[4:6])
    # rprint(sec_str)
    #ms
    ms_str = ms_str_time
    # rprint(ms_str)
    start_dt = datetime.datetime(int(yr_str), int(month_str), int(day_str), int(hr_str), int(min_str), int(sec_str), int(ms_str))
    # rprint(start_dt)

    return start_dt

def get_Dt_from_time(time):
    pass

def getIndexesFromTime(target_time : int = 2, sr : float = 0) -> int:
    num_seconds = target_time * 60
    number_indx = num_seconds*sr
    return number_indx
     


def analyse_audio_file():
    """_summary_

    Args:
        filename (string, optional): _description_. Defaults to "".

    Returns:
        int: _description_
    """    
    result = 1
    # rprint ("Loading acoustic data.")
    if filename == "":
        with console.status("[bold green] Fetching acoustic data...") as status:
            raw_data, sample_rate = librosa.load(audio_files[0])
    
    else:
        with console.status("[bold green] Fetching acoustic data...") as status:
            file_path =f"/home/vixen/rs/data/acoustic/{filename}"
            raw_data, sample_rate = librosa.load(file_path)
    
            
    
    #input frame size in seconds from command line
    # data_frame_size = data_frame_size * sample_rate        
    # data_frame_size_tmp = data_frame_size * sample_rate
    # data_frame_size = data_frame_size_tmp
    
    # print(raw_data.shape)
    raw_dimension = raw_data.shape[0]
    print (raw_data.shape)
    
    
    
    
    print(f'sample rate: {sample_rate}')
    rec_time_s = raw_dimension / sample_rate
    data_frame_time_s = data_frame_size / sample_rate
    
    
    
    rprint(f'Total Recorded Time(m)= {rec_time_s/60}') 
    rprint(f'Total Sample Time(m)= {data_frame_time_s/60}') 
    
    ref_loc = {}
    ref_loc['latitude'] = 50.719344
    ref_loc['longitude'] = -0.548028
    
    start_dt = get_start_date_time(filename)
    print (f'start time : {start_dt}')
    
    
    environemt_memory = AcousticEnvironmentMemory()
    # tut_bot = bot()
    # tutbot.build(min_vector=4, max_vector=15)
    
    
    model = model_frame()
    model.build_population(size=1, freq_bucket_size = freq_frame_size, target_frequency_min=freq_target_min, target_frequency_max=freq_target_max, min_vector = min_memory, max_vector=max_memory) #needs updating for ML mode.
    
    #------------SNAPSHOT CONTAINER --------------
    ss_container = snapshot_container()
   
    with Progress() as progress:
        process = psutil.Process(os.getpid())
        
        task1 = progress.add_task(f"[green] Building & analysing data frames [size={data_frame_size}]", total = 100)
        start_index  = 0
        end_index = 0
        sample_number = 0
        current_sim_time = start_dt
        
        
        
        while end_index < raw_dimension:
            
            #physical timeframe
            time_delta = timedelta(seconds = data_frame_time_s)
            # rprint(time_delta)
            
            # rprint(f'Sample number [{sample_number}] Index {end_index} of {raw_dimension}')
            
            sample_number+=1
            end_index = start_index + data_frame_size
            update_run_progress(current_index=end_index, total_index=raw_dimension, run_id=run_id)
            rprint(f'Frame start time [{current_sim_time}] delta t {time_delta}  Sample number [{sample_number}] Index {end_index} of {raw_dimension}') #end='\r'
           
            # rprint(f'sr{sample_rate}')
            #-----------Build Dataframe-------------------
            data_frame = acoustic_frame(location_name= run_data["location"], location = ref_loc, start_index=start_index, end_index=end_index, sample_number=sample_number, 
                                        start_time=current_sim_time, end_time=current_sim_time + time_delta, sample_rate=sample_rate , sample_size = data_frame_size, batch_id = batch_id)
            #with console.status("[bold green] Analysing data...") as status:
            data_frame.analyse(raw_data)
            environemt_memory.add_acoustic_experience(data_frame)
            #---------------------------------------------
            
            #------------Snapshot detection---------------
            # Run Model 
            #---------------------------------------------
            
            model_hit = False
            model_hit = model.run(environemt_memory)
    
            #---------------------------------------------
            
            
            #------------Snapshot detection---------------
            # Run XR
            #---------------------------------------------
            
            geo_hit = False
            geo_model = geo_frame(acoustic_data = data_frame)
            geo_hit = geo_model.run()
            
            #---------------------------------------------
            
            
            
            
            
            snap = True
            if model_hit == True or geo_hit == True or snap == True:
                # print(f'model: {model_hit} geo: {geo_hit}')
                num_indx = getIndexesFromTime(sr = sample_rate)
               
                env_start_index = max(0, start_index-num_indx)
                env_end_index = min(len(raw_data), end_index + num_indx)
                env_acoustic_frame = acoustic_frame(location_name= run_data["location"], location = ref_loc, start_index=env_start_index, end_index=env_end_index, sample_number=sample_number, 
                                        start_time=current_sim_time, end_time=current_sim_time + time_delta, sample_rate=sample_rate , sample_size = data_frame_size, batch_id = batch_id)
                
                env_acoustic_frame.set_data(raw_data)
                env_acoustic_frame.create_spectogram()
                
                tf_snapshot = snapshot(batch_id=batch_id)
                tf_snapshot.build(decision_acoustic_data = data_frame, environment_acoustic_data = env_acoustic_frame, geo_data = geo_model, model_data = model)
                tf_snapshot.hit(run_id = run_id)
                
                ss_container.update(tf_snapshot.out_json)

            start_index = end_index
            adv = ((data_frame_size)/raw_dimension) * 100
            # print (end_index, raw_dimension, adv)
            progress.update(task1, advance=adv)
            current_sim_time = current_sim_time + time_delta
            # time.sleep(0.1)
        
        # rprint("Data frames built.")
        ss_container.send_to_db(run_id=run_id)
    
    return raw_data, sample_rate, result, start_dt, current_sim_time


'''

    ...Run Algorith...

'''
send_run_data(run_data)


audio_files = glob('/home/vixen/rs/data/acoustic/*.wav')

#attach fn. link to arg parser

filenames = ["_20230616_115756_779.wav","_20230616_130005_321.wav","_20230617_130453_825.wav"]
filenames = []
filenames.append(filename)



console = Console()
data_frame_size = 0
batch_id = 0


#have a look at sample size vs output
samples = range(1000000, 10000000, 100000)




#one sample
# samples = range(3500, 3500, 0)

samples = []
samples.append(sample_size)
import random





for fn in filenames:

    filename = fn
    # tag_id = random.randint(0,9999999)
    batch_id = f"{run_data['run_id']}"
    # batch_id = run_data['run_id']
    print (f' Running batch number: {batch_id}')
    #send run data
    
    for sample_size in samples:
        
        #build folder structure
        cmd = f'mkdir /home/vixen/html/rs/batch/{batch_id}'
        os.system(cmd)
        
        cmd = f'mkdir /home/vixen/html/rs/batch/{batch_id}/{sample_size}'
        os.system(cmd)
        
        #/home/vixen/html/rs/snapshots/{self.batch_id}/json/
        cmd = f'mkdir /home/vixen/html/rs/snapshots/{batch_id}'
        os.system(cmd)
        
        cmd = f'mkdir /home/vixen/html/rs/snapshots/{batch_id}/json'
        os.system(cmd)
        
        cmd = f'mkdir /home/vixen/html/rs/video/batch/{batch_id}'
        os.system(cmd)
        
        
        
        data_frame_size = sample_size
        load_thread = Thread(target = analyse_audio_file)
        load_thread.start()
        load_thread.join()
        
        
        
        #----build mpg of spec and all snapshots
        # rprint('Building mpg4')
        cmd = f'ffmpeg -y -r 5 -s 1080x1620 -i /home/vixen/html/rs/batch/{batch_id}/{data_frame_size}/spec_%05d.png -vcodec h264 -crf 25 ~/html/rs/video/batch/{batch_id}/video_{data_frame_size}.mp4'
        os.system(cmd)

        #----delete images of spec
        cmd = 'rm /home/vixen/html/rs/batch/*.png'
        # os.system(cmd)
        
        
    

sys.exit(1)


