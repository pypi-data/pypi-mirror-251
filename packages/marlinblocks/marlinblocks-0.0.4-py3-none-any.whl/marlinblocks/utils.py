import random
from gmplot import *
import sys, os


TRACK_SAMPLE_RATE = 1.0
GMAP_API_KEY = "AIzaSyAVxdJBQsf8vZd3XBR3pB8C3wAOTfQU8Vw"


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
        


def BuildKMLFileCSV(track:{}= None, id:any = None):
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
    tail = '</Document></kml>'
    placemarks = ""

    for placemark in track:
        if random.random() < TRACK_SAMPLE_RATE:
            i = 0
            placemarks += f" <gx:TimeStamp><when>{placemark['timestamp']}</when></gx:TimeStamp><Placemark><name></name><description></description><Point><coordinates>{placemark['longitude']},{placemark['latitude']},0</coordinates></Point> </Placemark>\n"
            i += 1

    kml_content = header + placemarks + tail

    #write kml data
    tag = placemark['mmsi']
    with open(f"/home/vixen/html/rs/kml/kml_{tag}.kml", 'w') as f:
        f.write(kml_content)
    
    with open(f"output/kml/kml_{tag}.kml", 'w') as g:
        g.write(kml_content)



def BuildKMLFile(track=None, id=None):

    header = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
    tail = '</Document></kml>'
    placemarks = ""

    for placemark in track:
        if random.random() < TRACK_SAMPLE_RATE:
            i = 0
            placemarks += f" <gx:TimeStamp><when>{placemark['time_stamp']}</when></gx:TimeStamp><Placemark><name></name><description></description><Point><coordinates>{placemark['geometry']['coordinates'][1]},{placemark['geometry']['coordinates'][0]},0</coordinates></Point> </Placemark>"
            i += 1

    kml_content = header + placemarks + tail

    with open(f"kml/kml_{id}.kml", 'w') as f:
        f.write(kml_content)



def AnimateMapTrack(track=None, target_name=""):
    """_summary_

    Args:
        track (_type_): _description_
        target_name (_type_): _description_
    """    
    # create html & img folder
    cmd = f"mkdir ~/html/rs/track_html/{target_name}"
    os.system(cmd)
    cmd = f"mkdir ~/html/rs/track_img/{target_name}"
    os.system(cmd)
    cmd = f"mkdir ~/rs/dev/src/output/track_html/{target_name}"
    os.system(cmd)
    cmd = f"mkdir ~/rs/dev/src/output/track_img/{target_name}"
    os.system(cmd)
    
    cmd = f"rm -r ~/rs/dev/src/output/track_html/{target_name}/*"
    os.system(cmd)
    cmd = f"rm -r ~/rs/dev/src/output/track_img/{target_name}/*"
    os.system(cmd)
    cmd = f"rm -r ~/html/rs/track_html/{target_name}/*"
    os.system(cmd)
    cmd = f"rm -r ~/html/rs/track_img/{target_name}/*"
    os.system(cmd)
    
    #build html & images
    counter=0
    gMap = None
    lat_v = []
    long_v = []
    # while len(lat_v) < counter+1:
    for point in track:
        if random.random() < TRACK_SAMPLE_RATE:
            
            lat_v.append(point['latitude'])
            long_v.append(point['longitude'])
            
            lat_v.append(point['latitude'])
            long_v.append(point['longitude'])
            # gMap = ShowOnMap(lat_v, long_v, gMap)
            print(len(lat_v), len(long_v))
            ShowOnMap(lat_v, long_v, gMap, target_name, counter)
            counter+=1

    exit()

    #create movie

import imgkit
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

def ShowOnMap(lat, long, myGmap, target_name:str="", counter:int = -1):

    myGmap = None

    if myGmap == None:
        myGmap = gmplot.GoogleMapPlotter(lat[0], long[0], 20)
    # print(lat[0], long[0])
    # print(f'lat size: {len(lat)}')
    # print(f'long size: {len(long)}')
    myGmap.scatter(lat, long, '#FF5100', size=10, marker=False)
    myGmap.plot(lat,long)
    
    myGmap.polygon(lat, long, color='cornflowerblue')
    myGmap.apikey = GMAP_API_KEY
    if counter == -1:    
        myGmap.draw(f"/home/vixen/html/rs/track_html/{target_name}/{target_name}_track_journey.html")
        
    else:
        myGmap.draw(f"/home/vixen/rs/dev/src/output/track_html/{target_name}/{target_name}_track_{counter}.html")
        # imgkit.from_file(f"/home/vixen/rs/dev/src/output/track_html/{target_name}/{target_name}_track_{counter}.html", f"/home/vixen/rs/dev/src/output/track_img/{target_name}/{target_name}_track_{counter}.jpg")
        myGmap.draw(f"/home/vixen/html/rs/track_html/{target_name}/{target_name}_track_{counter}.html")
        
        # options = Options()
        # options.headless = True
        # driver = webdriver.Firefox(options=options)
        
        # driver.set_window_position(0, 0)
        # driver.set_window_size(2000, 2000)
        # url = f"https://vixen.hopto.org/rs/html_track/{target_name}_track_{counter}.html"
        # driver.get(url)
        # img = driver.screenshot_as_png
        # with open(f"/html/rs/track_img/{target_name}/{target_name}_track_{counter}.png", "wb") as file:
        #     file.write(img)
        # time.sleep(2)

def RunTrack(track, target_name:str = ""):
    """_summary_

    Args:
        track (_type_): _description_
        target_name (str, optional): _description_. Defaults to "".
    """    
    gMap = None
    lat_v = []
    long_v = []
    for point in track:
        if random.random() < TRACK_SAMPLE_RATE:
            # print("adding")
            # print(point)
            lat_v.append(point['latitude'])
            long_v.append(point['longitude'])
            # gMap = ShowOnMap(lat_v, long_v, gMap)

    ShowOnMap(lat_v, long_v, gMap, target_name, -1)
