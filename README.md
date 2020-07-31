# 3D_SoundEffect
This project generates 3D sound effect(including vertical and horizontal) from an audio file.
## Dataset
**The CIPIC HRTF Database**

The CIPIC HRTF Database is a public-domain database of high-spatial-resolution HRTF measurements for 45 different subjects, including the KEMAR mannequin with both small and large pinnae.

The database includes 2,500 measurements of head-related impulse responses for each subject. These “standard” measurements were recorded at 25 different interaural-polar azimuths and 50 different interaural-polar elevations. Additional “special” measurements of the KEMAR manikin were made for the frontal and horizontal planes. In addition, the database includes anthropometric measurements for use in HRTF scaling studies, technical documentation, and a utility program for displaying and inspecting the data. 

## HRTF
In order to generate 3-D sound effect, voice that internalized in or near the center of the head needs to be filtered by a pair of filters that simulate human auditory system. A head-related transfer function (HRTF) is such a filter that characterizes how an ear receives a sound from a point in space. In other words, HRTF provides a sound source localization model that has the spectrum structure characteristics of both IID and ITD.

## Guidance
By loading the different datasets in source code, audio files of vertical and horizontal can be generated. Using a headphone to test the results.
