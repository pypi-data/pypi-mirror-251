#!/usr/bin/env
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


from marlinblocks.bot import *
 

class model_frame(object):
    def __init__(self):
        self.hit = False
        self.population = []
    
    def build_population(self, size = 1, freq_bucket_size = 100, target_frequency_min = 0, target_frequency_max = 500, min_vector : int = 10, max_vector : int = 10):
        self.population_size = size
        for i in range(0, self.population_size):
            _bot = bot()
            _bot.build(min_vector = min_vector, max_vector=max_vector, frequency_bucket=freq_bucket_size, freq_target_min=target_frequency_min, freq_target_max=target_frequency_max ) #max_v currently obsolete
            self.population.append(_bot)
            
    
    def run(self,  acoustic_data : acoustic_frame = None) -> bool:
        hit = False;

        hit_vector = []

        for bot in self.population:
            hit = bot.run(acoustic_data)
            hit_vector.append(hit)
       
        hit_ratio = (sum(hit_vector) / len(hit_vector)) * 100
        if hit_ratio > 0.8:
            hit = True
            self.hit = True
        

        return hit