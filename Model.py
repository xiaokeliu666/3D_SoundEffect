# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:40:19 2019

@author: Scott
"""
import numpy as np
from scipy import io, signal
from scipy.fftpack import ifft
from scipy.io.wavfile import write

def modeling_transfer_function(n, fn = 500): 
    angle_set =[]
    angle_set.extend(np.linspace(0, -0.5*np.pi, n))
    angle_set.extend(np.linspace(-0.5*np.pi, 0.5*np.pi, 2*n))
    angle_set.extend(np.linspace(0.5*np.pi, 0, n))


    omega_set = np.linspace(-np.pi, np.pi, fn)
    temp = 10 / (np.pi*2) 

    HR = np.complex64(np.zeros((len(angle_set),fn)))
    HL = np.complex64(np.zeros((len(angle_set), fn)))

    j = 0
    for each in angle_set:
        k = 0
        for omega in omega_set:
            alpha = (1 + np.sin(each))/2
            delta = temp/2
            Tr = (1 - alpha)*delta
            Tl = alpha * delta

            Hr = (complex(1, 2*alpha*omega*delta)/complex(1, omega*delta)) * np.exp(complex(0,-omega*Tr))
            Hl = (complex(1, 2 * (1-alpha) * omega * delta) / complex(1, omega * delta)) * np.exp(complex(0, -omega * Tl))

            HR[j, k] = Hr
            HL[j, k] = Hl

            k +=1
        j+=1


    HR = np.hstack((HR[:, int(fn / 2):], HR[:,:int(fn / 2)]))
    HL = np.hstack((HL[:, :int(fn / 2)], HR[:, int(fn / 2):]))

    return HL,HR

def max_length(a):
    matr = a.shape
    maximum = max(list(matr))
    return maximum

def HRTF_synthetic_model(fn):
    fs, wave = io.wavfile.read(fn)
    wave = wave.reshape(1, -1)  # 1 * n
    time = max(list(wave.shape))

    HL, HR = modeling_transfer_function(n=20) # Calculate HL,HR from formula

    hL = np.real(ifft(np.array(HL), axis=1)) # HL ---> hL
    hR = np.real(ifft(np.array(HR), axis=1))

    # Swithing left and right

    hL = np.hstack((hL[:,int(hL.shape[1]/2):], hL[:,:int(hL.shape[1]/2)]))
    hR = np.hstack((hR[:,int(hR.shape[1]/2):], hR[:,:int(hR.shape[1]/2)]))

    points_number = int(hL.shape[0])
    r = time % points_number

    if (r > 0):
        padding_zero = int(points_number - r)
        wave = np.concatenate((wave, np.zeros((1, padding_zero))), axis=1)

    step = int(max(list(wave.shape)) / points_number)


    for i in range(1, points_number + 1):  

        AL = hL[i-1,:]
        AR = hR[i-1,:]

        B = 1
        inputL = wave[0, step * (i - 1): step * i]
        inputR = wave[0, step * (i - 1): step * i]

        zi = signal.lfilter_zi(AL, B)
        L, _ = signal.lfilter(AL, B, inputL, axis=-1, zi=zi)

        zi = signal.lfilter_zi(AR, B)
        R, _ = signal.lfilter(AR, B, inputR, axis=-1, zi=zi)

        L = L.reshape(1,-1)
        R = R.reshape(1, -1)

        if (i ==1):
            left = np.array(L)
            right = np.array(R)
        else:
            left = np.hstack((left, L))
            right = np.hstack((right, R))

    max_value = np.max(np.abs(np.concatenate((left, right), axis=1)))

    left = left / max_value
    left = left[0, :]
    right = right / max_value
    right = right[0, :]



    out = np.concatenate((left.reshape(-1, 1), right.reshape(-1, 1)), axis=1)

    max_value = np.max(np.abs(out))
    out = out / max_value  # 2 * n
    out = out[:, :]

    return out
    

fs = 44100
fn = 'Original.wav'

n = 20
modeling_transfer_function(n, fn = 500)

out = HRTF_synthetic_model(fn)    
outs=np.shape(out)

output_wave = 'Model.wav'                   
scaled = np.int16(out/np.max(np.max(np.abs(out)))*32767)
write(output_wave,fs,scaled)
