# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:40:19 2019

@author: Scott
"""

from scipy.io import loadmat
import numpy as np
from scipy.io import wavfile
from scipy import signal

def load_CIPIC_HRIP(left_or_right):

    m = loadmat("hrir_final.mat")
    hrir_l = m["hrir_l"]
    hrir_r = m["hrir_r"]

    if left_or_right == "left":
        out = np.vstack((np.squeeze(hrir_l[:, 8]), np.flip(np.squeeze(hrir_l[:, 40]), 0)))
    elif left_or_right =="right":
        out = np.vstack((np.squeeze(hrir_r[:, 8]), np.flip(np.squeeze(hrir_r[:, 40]), 0)))
    return out


def audio_with_brir(brir):

    # read audio file
    wavepath= "Original.wav"
    fs, audioIn = wavfile.read(wavepath)
    audioIn = np.array(audioIn)
    audioIn = audioIn / 32767

    # get the length of audio file
    duration = len(audioIn)

    #columns
    points_number = brir.shape[1]//2   

    #the number of padding zeros
    remainder = duration % points_number

    if remainder>0:
        padding_zero = points_number-remainder
        audioIn = np.hstack((audioIn , np.zeros(padding_zero)))

    # calcualte the new audio length and a step length for each segment
    step = len(audioIn)//points_number

# TODO
# Applying hanning window to fade in and out
    # length for window size
#    window_N = 512
#    window = np.hanning(window_N)

    # pass filter
#    lowpass = signal.firwin(1000,(20000/fs)*2,window='hamming')
#    highpass = signal.firwin(1001,(20/fs)*2,window='hamming',pass_zero=False)

    #init segment piece
    segment_L = np.zeros((points_number,step))
    segment_R = np.zeros((points_number,step))

    for i in range(points_number):
        L = signal.lfilter(brir[:,i*2],1,audioIn[step*i:step*(i+1)])
        R = signal.lfilter(brir[:,i*2+1],1,audioIn[step*i:step*(i+1)])

        segment_L[i,:] = L
        segment_R[i,:] = R

    out_L = segment_L.reshape(-1)
    out_R = segment_R.reshape(-1)
    out = np.vstack((out_L,out_R))
    out = out.T
    return out


if __name__ =='__main__':

    fs = 44100


    hrir_l = load_CIPIC_HRIP('left')
    hrir_r = load_CIPIC_HRIP('right')

    hrir = np.zeros((200, 100))

    for i in range(50):
        hrir[:, i * 2] = hrir_l[i]
        hrir[:, i * 2 + 1] = hrir_r[i]

    out =audio_with_brir(hrir)

    wavfile.write('HRTF_Horizontal.wav',44100,out)