# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:40:19 2019

@author: Scott
"""
import numpy as np
from scipy import io
from scipy.io.wavfile import write

def length(a):
    matr = a.shape
    maximum = max(list(matr))
    return maximum

def audio_with_hrir(left,right,wave1,hrir):
    wave=wave1
    wave=wave.reshape(-1,1)
    time = length(wave)
    points_number = num.shape[1]/2

    remainder = time % points_number
    if remainder > 0 :
       padding_zero = int(points_number - remainder)
       zero = np.zeros((padding_zero,1))
       wave = np.vstack((wave,zero))
       step = int(length(wave) / points_number)
      
    #infit part piece
       step = int(step)
       points_number = int(points_number)

       nz = length(left)
       left = np.zeros(nz)
       right = np.zeros(nz);

       for i in range(1 ,(points_number +1)):
    #flatting    
           wave = wave.reshape(1,-1)
           hrir1=hrir[:,2*i+1]
           lhrir1=length(hrir1)
           
           hrir2=hrir[:,2*i+2]
           lhrir2=length(hrir2)

           wav1=wave[0,step*(i-1):step*i]
           len_wav1=length(wav1)
           wav2=wave[0,step*(i-1):step*i]
           len_lwav2=length(wav2)

           A1=len_wav1+ lhrir1
           A2=len_lwav2+ lhrir2
           wave_l_fft = np.fft.fft(wav1,A1)
           wave_r_fft = np.fft.fft(wav2, len_lwav2+ lhrir2)

           A = np.fft.fft(hrir1,A1)
           B = np.fft.fft(hrir2,A2)
           
           #store the real part
           L = np.real(np.fft.ifft(wave_l_fft * A)); 
           R = np.real(np.fft.ifft(wave_r_fft * B)); 

           left = np.hstack((left,L))
           right = np.hstack((right,R))    

    # find max value
    mv = np.vstack((left,right))
    max_value = np.max(np.abs(mv))

# normalization 
# todo
# compare the result of max_value and 32767
    left = left / max_value;
    right = right / max_value;
   
    out = np.vstack((left,right))

    return out
fn,wave1 = io.wavfile.read('Original.wav')

fs = 44100
hrir_fn= io.loadmat('large_pinna_final.mat')

left=hrir_fn['left']
right=hrir_fn['right']
front = 8
back = 40


# get the  HRIR for each ear
hrir_l = np.hstack((left,left))
hrir_r = np.hstack((right,right))
numl=np.array(left)
n = numl.shape[1]

n = n*8

# get the total HRIR

hrir = np.zeros((200,n))

num=np.array(hrir_l)
hang=num.shape[0]
lie=num.shape[1]


for i in range(1,lie+1):
    hrir[:,i*2-2] = hrir_l[:,i-1]
    hrir[:,i*2-1] =  hrir_r[:,i-1]


out = audio_with_hrir(left,right,wave1,hrir)

out=np.transpose(out)
outs=np.shape(out)

# Use another dataset to get the vertical audio
output_wave = 'FFT_Horizontal.wav'                   
scaled = np.int16(out/np.max(np.max(np.abs(out)))*32767)
write(output_wave,fs,scaled)



