#!/usr/bin/env

from marlinblocks.acoustic_frame import *
from marlinblocks.std_imports import *


class bot(object):
    """

    Args:
        object (_type_): _description_
    """    
    
    def __init__(self):
        self.name = "tut_EnergyBot"
        self.initialised = False
        
    def build(self, min_vector : int = 1, max_vector : int = 5, frequency_bucket : int = 100, freq_target_min : int = 0, freq_target_max : int = 500):
         self.struct = {'min_vector' : min_vector, 'max_vector' : max_vector, 'frequency_bucket' : frequency_bucket, 'target_frequency_min' : freq_target_min, 'target_frequency_max' : freq_target_max}
         
    def run(self, acoustic_memory : AcousticEnvironmentMemory = None) -> bool:
        hit = False
        
        '''
            Mode to read data and make decision. Memory question.
        '''
        
        current_memory_length = acoustic_memory.get_memory_length()
        if current_memory_length > self.struct['min_vector'] + 5: #safety arithmetic
            self.initialised = True
        
        
        
        if self.initialised:
            
            # get data
            energy_metric_vector = []
            end_epoch = current_memory_length
            
            for i in range(end_epoch-self.struct['min_vector'],end_epoch):
                # Get acoustic frame from memory
                # note : sample number = index + 1
                acoustic_frame = acoustic_memory.get_memory_experience(i)
                
                # Run signal analysis on bot's choice of f bucket
                resolved_data = acoustic_frame.run_resolved_analysis(self.struct['frequency_bucket'])
                # rprint (resolved_data)
                
                #get stats for interval of choice
                target_data = acoustic_frame.freq_framer.resolved_freq_frames.get_energy_data(frequency_start = 0, frequency_end = self.struct['target_frequency_max'])
                # rprint(target_data)
                energy_metric_vector.append(target_data['avg_amplitude'])
                
                
            #logic
            sorted_energy_vector = sorted(energy_metric_vector, reverse=False)
            if sorted_energy_vector == energy_metric_vector:
                hit = True
            
            
            
            
        
        
                

        
        
        
        # rprint(f'bot : {self.name} : init: {self.initialised} : hit {hit}')
        
        return hit