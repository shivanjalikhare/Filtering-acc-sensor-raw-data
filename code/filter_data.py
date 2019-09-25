# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:28:52 2019

@author: Shivanjali Khare
"""



import math
from scipy.fftpack import fft
from scipy import signal
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from data_util import *
import csv
import pandas as pd

def read_data(file_path, columns):
    mode = 'r'
    with open (file_path, mode) as f:
        lines = f.readlines()
        #print(len(lines))
        num_rows = len(lines)
        print(str(num_rows), 'rows')
        num_cols=len(columns)
        print(str(num_cols), 'cols')
        data=np.zeros([num_rows,num_cols])
        for indice, line in enumerate(lines[:]):
            row=line.rstrip().split(',')
            #print(row)
            for ii,i in enumerate(columns):
                data[indice, ii] = row[i]
    print('done')
    f.close()
    return data


def plot_lines(data,fs,title):
    num_rows, num_cols=data.shape
    if num_cols != 3:
        raise ValueError('Not 3D data')
    fig, ax=plt.subplots()
    labels=['x','y','z']
    color_map=['r','g','b']
   
    index=np.arange(num_rows)/fs
    print(index.shape)
    for i in range(num_cols):
        ax.plot(index, data[:,i], color_map[i], label=labels[i])
    ax.set_xlim([0,num_rows/fs])
    ax.set_xlabel('Time')
    ax.set_xlabel('Time [sec]')
    ax.set_title('Time domain ' +title )
    ax.legend


    
def median_filter(data, f_size):
    lgth, num_signal=data.shape
    f_data=np.zeros([lgth,num_signal])
    for i in range(num_signal):
        f_data[:,i]=signal.medfilt(data[:,i], f_size)
    return f_data



def freq_filter(data, f_size, cutoff):
    lgth, num_signal=data.shape
    f_data=np.zeros([lgth, num_signal])
    lpf=signal.firwin(f_size,cutoff,window='hamming')
    for i in range(num_signal):
        f_data[:,i] = signal.convolve(data[:,i], lpf, mode='same')
    return f_data

def plot3D(data,title):
    fig=plt.figure()
    ax=fig.add_subplot(111, projection='3d')
    ax.plot(xs=data[:,0], ys=data[:,1], zs=data[:,2], zdir='z')
    ax.set_title(title)

def test_data(file_name):
    
    cur_dir=os.getcwd()
    fs=512
    cutoff=10
    file_path=os.path.join(cur_dir, 'data', file_name)
    data=read_data(file_path, [0,1,2])
    plot_lines(data, fs, 'Raw data')
    #fft_plot(data, fs, 'Raw data')
    median_data=median_filter(data, 155)
    lpf_data=freq_filter(data, 155, cutoff/fs)
    comb_data=freq_filter(median_data, 155, cutoff/fs)
    
    print(median_data.shape) 
    plot_lines(median_data, fs, 'median filter')
    plot_lines(lpf_data,fs,'low pass filter')
    plot_lines(comb_data, fs, 'median_low pass filter')
    plot3D(data, 'raw data')
    plot3D(median_data,'median filter')
    plot3D(lpf_data, 'low pass filter')
    plot3D(comb_data, 'median + lpf')
	
    plt.show()
    
    
	
	
	
	
	

	

if __name__ == '__main__':  
    input_id = input("filename")
    test_data(input_id)
       

    
