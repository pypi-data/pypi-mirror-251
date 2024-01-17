#!/usr/bin/env

#
#
# Copyright RS Aqua and Marlin 2023 www.rsaqua.co.uk r.tandon@rsaqua.co.uk
# -------------------------------------------------------------------------------------
# Written by Rahul Tandon, r.tandon@rsaqua.co.uk
#
#

"""_summary_
"""
from rich import pretty
from rich.console import Console
pretty.install()
from rich import print as rprint
from rich.progress import Progress


from geopy import distance

def BuildDistanceProfile(track: {} = None, center_point:{} = None):
    """_summary_

    Args:
        track (None, optional): _description_. Defaults to None.
        center_point (None, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """    
    distance_profile = {}
    point_of_closest_approach = {}

    ref_loc = (center_point['latitude'], center_point['longitude'])
    print(f'Number of track points: {len(track)}')
    min_d = 10000000000000
    for pt in track:
        
        t_loc = (pt['latitude'], pt['longitude'])
        d = distance.distance(ref_loc, t_loc).km
        distance_profile[pt['timestamp']] = d
        if d < min_d:
            min_d = d
            point_of_closest_approach['nearest'] = {'pt' : pt, 'distance' : d}
        
    
        
    return distance_profile, point_of_closest_approach
    