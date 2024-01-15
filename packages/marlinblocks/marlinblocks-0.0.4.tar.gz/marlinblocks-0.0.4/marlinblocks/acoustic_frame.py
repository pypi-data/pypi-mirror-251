#!/usr/bin/env

#
#
# Copyright RS Aqua and Marlin 2023 www.rsaqua.co.uk r.tandon@rsaqua.co.uk
# -------------------------------------------------------------------------------------
# Written by Rahul Tandon, r.tandon@rsaqua.co.uk
#
#

#
# todo Dec 2023 -> allow for multiple acoustic frames. More encapsulation and output to snapshot. More than one acoustic frame per bot.
# video for each acoustic frame when a hit. Encapsulate. Make available on web app. Video list to play and images to view. Data signal 
# visualisation.
# 


import marlinblocks.std_imports
import os, sys
import logging
import numpy as np
import librosa
import librosa.display
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import datetime
import random
import scipy
import json
logging.basicConfig(level=logging.ERROR)


    

class resolved_frequency_frame(object):
    """

    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """    
    
    
    def __init__(self, resolved_data : dict = {}):
        self.resolved_freq_data = resolved_data
        self.resolved_freq_stats_data = {}
    
    
    def run_stats(self):
        for f, f_bucket in self.resolved_freq_data.items():
            bucket_stats = self.build_bucket_stats(f_bucket, f)
            self.resolved_freq_stats_data[f] = bucket_stats
            
            
        return self.resolved_freq_stats_data
    
    
    def get_energy_data(self, frequency_start : float = 0, frequency_end : float = 100):
        """

        Args:
            frequency_start (float, optional): _description_. Defaults to 0.
            frequency_end (float, optional): _description_. Defaults to 100.
        """    
        amplitude = 0
        number = 0
        for freq, stats in self.resolved_freq_stats_data.items():
           if freq <= frequency_end:
               amplitude += stats['avg_amplitude']
               number += 1
        
        
        average_amplitude = amplitude/number
        
        return { 'avg_amplitude' : average_amplitude, 'frequency_end'  : frequency_end}
            
    
    # def combine_data(self, data_one : {}, data_two : {}):
        
    
    
    def build_bucket_stats(self, bucket, assoc_f) -> {}:
        
        stats = {}
        avg_a = 0
        freq = -1
        a = []
        for frame in bucket:
            # freq = frame.freq 
            freq = assoc_f
            frame_max_a = frame.get_max_amplitude()
            a.append(frame_max_a)
            
        
        avg_amplitude = abs(sum(a)/len(a))
        stats = {
            'avg_amplitude' : avg_amplitude,
            'bucket_f' : freq
        }
        
        return stats
    
    def output(self):
        for k,v in self.resolved_freq_stats_data.items():
            bucket_f = v['bucket_f']
            avg_amp = v['avg_amplitude']
            print (f'frequency bucket {bucket_f} : average energy {avg_amp}' )
            
            
    
class frequency_frame(object):
    
    """

    Args:
        object (_type_): _description_
    """    
    
    def __init__(self, start_time = None, end_time=None, frequency=0):
        self.start_time = start_time,
        self.end_time = end_time,
        # self.amplitude = amplitude,
        self.freq = frequency
        self.amplitude = []
        self.time = []
        self.min_a = 0
        self.max_a = 0
        

    # data
    def add_data(self,time, amplitude):
        self.time.append(time)
        self.amplitude.append(amplitude)
        
    #work
    def get_average_amplitude(self):
        pass
    
    def get_max_amplitude(self):
        return self.max_a
    
    
class frequency_framer(object):
    """_summary_

    Args:
        object (_type_): _description_
    """    

    def __init__(self, frame_data : [frequency_frame] = []):
        self.frame_data = frame_data
        self.f_bucket_size = 100 #Hz
        self.resolved_frame_data = {}


    def debug(self):
        for frame in self.frame_data:
            print (f'f:{frame.freq}')

    def summary(self):
        self.freq_list = []
        
        a_max = -1000000
        a_min = 10000000
        for f_frame in self.frame_data:
            self.freq_list.append(f_frame.freq)
            a_max_f = max(f_frame.amplitude)
            a_min_f = min(f_frame.amplitude)
            f_frame.max_a = a_max_f
            f_frame.min_a = a_min_f
            if a_max_f > a_max:
                a_max = a_max_f
            if a_min_f < a_min:
                a_min = a_min_f
    
        self.a_max = a_max
        self.a_min = a_min
        
        self.min_f = min(self.freq_list)
        self.max_f = max(self.freq_list)

        # print (self.freq_list)


    #visualiser
    def plot_profiles(self):
        pass

    def print_summary(self):
        print (f'max a {self.a_max} : min a {self.a_min} : ')
        print (f'max f {self.max_f} : min f {self.min_f} : ')
        print (f'number of data frames: {len(self.frame_data)}')
        
    
    # work
    def set_freq_bucket_size(self, freq_bucket_size : int = 100):
        self.f_bucket_size = freq_bucket_size
        
        
    def resolve_buckets(self) -> {}:
        """_summary_

        Returns:
            _type_: _description_
        """        
        #build buckets
        stat_bucket_bounds = []
        resolved_freq_frames = {}
        resolved_freq_data = {}
        start_f = 0
        end_f = 0
        
        while end_f < self.max_f:
            end_f = start_f + self.f_bucket_size
            resolved_freq_frames[end_f] = []
            for frame in self.frame_data:
                if frame.freq <= start_f and frame.freq < end_f:
                    resolved_freq_frames[end_f].append(frame)
                
            start_f = end_f
        

        self.resolved_freq_frames = resolved_frequency_frame(resolved_freq_frames)
        return_data = self.resolved_freq_frames.run_stats()
        
        return return_data
        # self.resolved_freq_frames.output()
        
            
    def build_plot_data(self):
        pass
            
    def Serialise(self):
        '''
            Serialise the frequency framer
        '''
        s_frame_data_amplitude = {}
        s_frame_data_time = {}
        s_frame_f = []
        for fframe in self.frame_data:
            s_frame_f.append(fframe.freq)
            s_frame_data_amplitude[fframe.freq] = (fframe.amplitude)
            s_frame_data_time[fframe.freq] = (fframe.time)
        
        
        return_data = {
           'f_list' : s_frame_f,
           'f_amplitude_list' : s_frame_data_amplitude,
           'f_time_list' : s_frame_data_time
        }
        
        return return_data
        
        
        
            
                    

class acoustic_frame(object):
    
    """
    acoustic_frame holds the raw data from a wav file and an analysis of
    that data for a defined period of time or timeframe.

    Args:
        object (_type_): Root Python object
    """
    
    def __init__(self, location_name : str = None, location : any = None, start_index:int = 0, end_index:int = 0, sample_number:int = 0, start_time:datetime = None, end_time: datetime = None, sample_rate: int = 0, sample_size = 0, batch_id : int = 0) -> None:
        ''' Constructor for acoustic_frame class.
        Args:
            start_index (int, optional): Index of raw data file where window/frame starts. Defaults to 0.
            end_index (int, optional):Index of raw data file where window/frame starts. Defaults to 0.

        Returns:
            int: Success or failure [1 or 0]
        '''

        exit_result = 1

        #set frame values
        self.frame_raw_data = None
        self.start_index = start_index   #start index of dataframe in raw data
        self.end_index = end_index       #end indew of dataframe in raw data
        self.sample_number = sample_number #sample number
        self.start_time = start_time    #start time of frame
        self.end_time = end_time
        self.location = location
        self.location_name = location_name
        self.sample_rate = sample_rate
        self.frame_delta_t = (self.end_index - self.start_index) / self.sample_rate
        self.frame_index = sample_size
        self.batch_id = batch_id
        logging.info(f"acoustic_frame created between index {start_index} and {end_index}. Exiting with {exit_result}")
        
        self.spec_images = []
        self.spec_images_html = []
        
        self.wave_images = []
        self.wave_images_html = []

        
        self.freq_framer = None
        

    def set_data(self, data : np.array = None):
        self.raw_data = data
            
    def create_spectogram(self):
        
        n_fft = 2048
        transformed_data = librosa.stft(self.raw_data[self.start_index : self.end_index], n_fft=n_fft, hop_length=n_fft//2)
        S_db = librosa.amplitude_to_db(np.abs(transformed_data), ref=np.max)
        S_db = np.abs(S_db)
        
        # print(self.start_index, self.end_index)
        
        # Plot transformed data
        fig, ax = plt.subplots(figsize=(10, 5))
        
        img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', ax=ax)
        ax.set(title='Time EnvironmentLog-frequency power spectogram')
        ax.label_outer()
        fig.colorbar(img, ax=ax, format=f'%0.f')
        # fig.savefig(f"output/{self.sample_number:03d}")
        #save to batch
        img_id = random.randint(0,90000000)
        fig.savefig(f"/home/vixen/html/rs/batch/{self.batch_id}/{self.frame_index}/custom_spec_{img_id}.png")
        self.spec_images.append(f"/home/vixen/html/rs/batch/{self.batch_id}/{self.frame_index}/custom_spec_{img_id}.png")
        self.spec_images_html.append(f"https://vixen.hopto.org/rs/batch/{self.batch_id}/{self.frame_index}/custom_spec_{img_id}.png")
        plt.close(fig)
        
    def load(self, raw_data:np.array = None, analysis = False) -> int:
        """_summary_

        Args:
            raw_data (_type_, optional): Numpy array of raw acoustic data.  Defaults to None.
            analysis (bool, optional): Run analysis on data. Defaults to False.

        Returns:
            int: Success or failure [1 or 0]
        """
        pass

    def f_analyse(self, D : np.ndarray = None):
        
        
        
        f, t, Zxx = scipy.signal.stft(D, fs=self.sample_rate, nperseg=1024)
        frequency_bins = f
        scipy_time_bins = t
        n_fft = 2048

        #convert frame counts to time (s)
        librosa_time_bins = librosa.frames_to_time(range(0, D.shape[1]), sr=self.sample_rate, hop_length=(n_fft//2), n_fft=n_fft)
        self.time_bins = librosa_time_bins
        #build frequency bins
        librosa_f_bins = librosa.core.fft_frequencies(n_fft=n_fft)
        self.f_bins = librosa_f_bins
        # print(f'amplitude: {D[14,450]} at f : {librosa_f_bins[14]} and t: {librosa_time_bins[450]}')
        # print(f'amplitude: {D[10,450]} at f : {librosa_f_bins[10]} and t: {librosa_time_bins[450]}')
        # print(f'amplitude: {D[9,450]} at f : {librosa_f_bins[9]} and t: {librosa_time_bins[450]}')
        # print(f'amplitude: {D[2,450]} at f : {librosa_f_bins[2]} and t: {librosa_time_bins[450]}')
        # print(f'amplitude: {D[140,450]} at f : {librosa_f_bins[140]} and t: {librosa_time_bins[450]}')
        
        # print(f'bin type : {type(librosa_time_bins)}')
        # print(librosa_time_bins)
        
        # print('Building frequency snapshots')
        # print (f'fbin length : {len(librosa_f_bins)}')
        # print (f'tbin length : {len(librosa_time_bins)}')
        list_of_freq_frames = []
        for freq_idx in range(0,len(librosa_f_bins)-1):
            
            f = librosa_f_bins[freq_idx]
            f_ss = frequency_frame(start_time=t, frequency = f)
            for tim_idx in range(0,len(librosa_time_bins)-1):                
                t = librosa_time_bins[tim_idx]
                a = D[freq_idx,tim_idx]
                f_ss.add_data(t,a)
            
            list_of_freq_frames.append(f_ss)
            
        # print (f'number of frames built {len(list_of_freq_frames)}')
        self.freq_framer = frequency_framer(list_of_freq_frames)
        self.freq_framer.summary()
        # self.freq_framer.print_summary()
        
        
        #---function below uncommented
        # fig, ax = plt.subplots(figsize=(10, 5))
        # img = librosa.display.waveshow(D, ax=ax)
        # ax.set(title='Waveshow')
        # ax.label_outer()
        # # fig.colorbar(img, ax=ax, format=f'%0.f')
        # # fig.savefig(f"output/{self.sample_number:03d}")
        # #save to batch
        # fig.savefig(f"/home/vixen/html/rs/batch/{self.batch_id}/{self.frame_index}/wave_{self.sample_number:05d}.png")
        
        # self.wave_images.append(f"/home/vixen/html/rs/batch/{self.batch_id}/{self.frame_index}/wave_{self.sample_number:05d}.png")
        # self.wave_images_html.append(f"https://vixen.hopto.org/rs/batch/{self.batch_id}/{self.frame_index}/wave_{self.sample_number:05d}.png")
        # plt.close(fig)
        
    def analyse(self, raw_data) -> str:
        
        
        self.frame_raw_data = raw_data[self.start_index : self.end_index]
        #spectogram
        
        n_fft = 2048
        hop_length = n_fft // 2
        # print (f'hop length: {hop_length}')
        transformed_data = librosa.stft(raw_data[self.start_index : self.end_index], n_fft=n_fft, hop_length=hop_length)
        S_db = librosa.amplitude_to_db(np.abs(transformed_data), ref=np.max)
        S_db = np.abs(S_db)
        # self.frame_raw_data = S_db
        
        
       
        # Plot transformed data
        
        #----default linear
        
        # fig, ax = plt.subplots(figsize=(10, 5))
        
        # img = librosa.display.specshow(S_db, x_axis='time', y_axis='linear', ax=ax)
        # ax.set(title='Linear-frequency power spectogram')
        # ax.label_outer()
        # fig.colorbar(img, ax=ax, format=f'%0.f')
        # fig.savefig(f"/home/vixen/html/rs/batch/{self.batch_id}/{self.frame_index}/spec_{self.sample_number:05d}_linear.png")
        # self.spec_images.append(f"/home/vixen/html/rs/batch/{self.batch_id}/{self.frame_index}/spec_{self.sample_number:05d}_linear.png")
        # self.spec_images_html.append(f"https://vixen.hopto.org/rs/batch/{self.batch_id}/{self.frame_index}/spec_{self.sample_number:05d}_linear.png")
        # plt.close(fig)
        
        #--- log frequency
        # fig, ax = plt.subplots(figsize=(10, 5))
        
        # img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', ax=ax)
        # ax.set(title='Log-frequency power spectogram')
        # ax.label_outer()
        # fig.colorbar(img, ax=ax, format=f'%0.f')
        # fig.savefig(f"/home/vixen/html/rs/batch/{self.batch_id}/{self.frame_index}/spec_{self.sample_number:05d}_log.png")
        # self.spec_images.append(f"/home/vixen/html/rs/batch/{self.batch_id}/{self.frame_index}/spec_{self.sample_number:05d}_log.png")
        # self.spec_images_html.append(f"https://vixen.hopto.org/rs/batch/{self.batch_id}/{self.frame_index}/spec_{self.sample_number:05d}_log.png")
        # plt.close(fig)
        
        
        
        
        
        #signal processing
        
    
        
        #time domain
        # fig, ax = plt.subplots(figsize=(10, 5))
        # img = librosa.display.waveshow(S_db)
        # plt.show(img)
        # plt.close(fig)
        
        # average over file
        D_AVG = np.mean(S_db, axis=1)


        # plt.bar(np.arange(D_AVG.shape[0]), D_AVG)
        # x_ticks_positions = [n for n in range(0, n_fft // 2, n_fft // 16)]
        # x_ticks_labels = [str(self.sample_rate / 2048 * n) + 'Hz' for n in x_ticks_positions]
        # plt.xticks(x_ticks_positions, x_ticks_labels)
        # plt.xlabel('Frequency')
        # plt.ylabel('dB')
        # plt.show(block=True)
        # plt.close()

        
        # print ('Running signal processing')
        self.f_analyse(S_db)
        
        # resolved_data_stats = self.run_resolved_analysis(100)
        # return resolved_data_stats
    
        # plt.show(block=True)
        # return f"output/{self.sample_number}"

    def run_resolved_analysis(self, resolve_size : int) -> {}:
        
        self.freq_framer.set_freq_bucket_size(resolve_size)
        resolved_data = self.freq_framer.resolve_buckets()
        return resolved_data #stats for data buckets
        
    def output(self):
        """_summary_
        """
        pass

    def Save(self):
        '''
            Serialise acoustic frame to db. 
        '''
        
        framer_data = self.freq_framer.Serialise()
        raw_data = self.frame_raw_data.tolist()
        time_bins = self.time_bins
        freq_bins = self.f_bins
    
        serialise_data = {
            
            'raw_data'      : self.frame_raw_data,
            'frequencies'   : [],
            'amplitude_data': [],
            'time_bins'     : [],
            'frequency_bins': []
        }
        
        
        # with open('data.json', 'w') as f:
        #     json.dump(serialise_data, f)
        
        return serialise_data
        


class AcousticEnvironmentMemory(object):
    """

    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """    

    def __init__(self):
        self.acoustic_memory = []
        
    def add_acoustic_experience(self, acoustic_experience : acoustic_frame = None):
        if acoustic_experience is not None:
            self.acoustic_memory.append(acoustic_experience)
            
    #sample number is one more than index
    def get_memory_experience(self, sample_id : int = 1) -> acoustic_frame:
        for frame in self.acoustic_memory:
            if frame.sample_number == sample_id:
                return frame
        
        
    def get_memory_length(self) -> int :
        return len(self.acoustic_memory)
    
    
        
                
