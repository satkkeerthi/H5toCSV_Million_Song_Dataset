"""
Satkkeerthi Sriram
University of West Florida
March 12th 2023

This code converts the HDF5 files of the Million Song Dataset to a CSV.

This file also requires the use of "hdf5_getters.py", written by
Thierry Bertin-Mahieux (2010) at Columbia University

Credit:
This HDF5 to CSV code makes use of the following example code provided
at the Million Song Dataset website 
(Home>Tutorial/Iterate Over All Songs, 
http://labrosa.ee.columbia.edu/millionsong/pages/iterate-over-all-songs)


Based on the code by Alexis Greenstreet here:
https://github.com/AGeoCoder/Million-Song-Dataset-HDF5-to-CSV/blob/master/msdHDF5toCSV.py
"""

import os
import hdf5_getters
import re
import math

def get_vector_dets(vector):
    n = len(vector)
    if n == 0:
        start = 0
    else:
        start = vector[0]
    exp_int = 0
    sd = 0
    
    if(n<=1):
        return start, exp_int, sd
    for i in range(1,n):
        exp_int+=vector[i] - vector[i-1]
    exp_int/=(n-1)
    for i in range(1,n):
        sd+=((vector[i]-vector[i-1]) - exp_int) * ((vector[i]-vector[i-1]) - exp_int)
    sd/=(n-1)
    sd = math.sqrt(sd)
    return start, exp_int, sd
    
def main():
    outputFile1 = open('SongCSV.csv', 'w')
    csvRowString = ""
    csvRowString = ("Title,AlbumName,Year,ArtistName,ArtistLocation,ArtistLatitude,"+
        "ArtistLongitude,ArtistFamiliarity,ArtistHotttnesss,Danceability,BarsStartFirst,BarsStartIntervalMean,BarsStartIntervalSD,BeatsStartFirst"+
        ",BeatsStartIntervalMean,BeatsStartIntervalSD,Duration,Energy,EndOfFadeIn,KeySignature,"+
        "Loudness,Mode,SongHotttnesss,StartOfFadeOut,SectionsStartFirst,SectionsStartIntervalMean,SectionsStartIntervalSD,"+
        "SegmentsStartFirst,SegmentsStartIntervalMean,SegmentsStartIntervalSD,TatumsStartFirst,TatumsStartIntervalMean,TatumsStartIntervalSD,Tempo,TimeSignature")
    
    csvAttributeList = re.split('\W+', csvRowString)
    for i, v in enumerate(csvAttributeList):
        csvAttributeList[i] = csvAttributeList[i].lower()
        
    outputFile1.write(csvRowString + "\n")
    csvRowString = ""  

    basedir = "." # Directory
    for f in os.listdir(basedir):
        print(f)
        if(f[-3:]!=".h5"):
            continue
        songH5File = hdf5_getters.open_h5_file_read(f)
        
        barsStart = hdf5_getters.get_bars_start(songH5File)
        barsStartVec = get_vector_dets(barsStart)
        beatsStartVec = get_vector_dets(hdf5_getters.get_beats_start(songH5File))
        tatumsStartVec = get_vector_dets(hdf5_getters.get_tatums_start(songH5File))
        sectionsStartVec = get_vector_dets(hdf5_getters.get_sections_start(songH5File))
        segmentsStartVec = get_vector_dets(hdf5_getters.get_segments_start(songH5File))
        
        for attribute in csvAttributeList:
            
            # Note that the strings are prefixed by b' and suffixed by ', thus the string[2:-1] is appended
            if attribute == 'AlbumName'.lower():
                albumName = str(hdf5_getters.get_release(songH5File))
                albumName = albumName.replace(",","")
                albumName = albumName.replace(";"," ")
                albumName = albumName.replace(';',' ')
                csvRowString += albumName[2:-1]
            elif attribute == 'ArtistLatitude'.lower():
                latitude = str(hdf5_getters.get_artist_latitude(songH5File))
                if latitude == 'nan':
                    latitude = ''
                csvRowString += latitude
            elif attribute == 'ArtistLocation'.lower():
                location = str(hdf5_getters.get_artist_location(songH5File))
                location = location.replace(',','')
                location = location.replace(";"," ")
                location = location.replace(';',' ')
                csvRowString += location[2:-1]
            elif attribute == 'ArtistLongitude'.lower():
                longitude = str(hdf5_getters.get_artist_longitude(songH5File))
                if longitude == 'nan':
                    longitude = ''
                csvRowString += longitude                
            elif attribute == 'ArtistName'.lower():
                artistName = str(hdf5_getters.get_artist_name(songH5File))
                artistName = artistName.replace(',','')
                artistName = artistName.replace(';',' ')
                artistName = artistName.replace(';',' ')
                csvRowString +=  artistName[2:-1]     
            elif attribute == 'ArtistFamiliarity'.lower():
                csvRowString += str(hdf5_getters.get_artist_familiarity(songH5File))        
            elif attribute == 'ArtistHotttnesss'.lower():
                artistHottnesss = str(hdf5_getters.get_artist_hotttnesss(songH5File))
                if artistHottnesss == 'nan':
                    artistHottnesss = ''
                csvRowString +=  artistHottnesss
            elif attribute == 'Danceability'.lower():
                csvRowString += str(hdf5_getters.get_danceability(songH5File))
            elif attribute == 'Duration'.lower():
                csvRowString += str(hdf5_getters.get_duration(songH5File))
            elif attribute == 'BarsStartFirst'.lower():
                csvRowString += str(barsStartVec[0])
            elif attribute == 'BarsStartIntervalMean'.lower():
                csvRowString += str(barsStartVec[1])
            elif attribute == 'BarsStartIntervalSD'.lower():
                csvRowString += str(barsStartVec[2])
            elif attribute == 'BeatsStartFirst'.lower():
                csvRowString += str(beatsStartVec[0])
            elif attribute == 'BeatsStartIntervalMean'.lower():
                csvRowString += str(beatsStartVec[1])
            elif attribute == 'BeatsStartIntervalSD'.lower():
                csvRowString += str(beatsStartVec[2])
            elif attribute == 'EndOfFadeIn'.lower():
                csvRowString += str(hdf5_getters.get_end_of_fade_in(songH5File))
            elif attribute == 'Energy'.lower():
                energy = str(hdf5_getters.get_energy(songH5File))
                csvRowString += energy
            elif attribute == 'KeySignature'.lower():
                csvRowString += str(hdf5_getters.get_key(songH5File))
            elif attribute == 'Loudness'.lower():
                csvRowString += str(hdf5_getters.get_loudness(songH5File))
            elif attribute == 'Mode'.lower():
                csvRowString += str(hdf5_getters.get_mode(songH5File))
            elif attribute == 'SongHotttnesss'.lower():
                songHotttnesss = str(hdf5_getters.get_song_hotttnesss(songH5File))
                if songHotttnesss == 'nan':
                    songHotttnesss = ''
                csvRowString += songHotttnesss
            elif attribute == 'StartOfFadeOut'.lower():
                csvRowString += str(hdf5_getters.get_start_of_fade_out(songH5File))
                
            elif attribute == 'SegmentsStartFirst'.lower():
                csvRowString += str(segmentsStartVec[0])
            elif attribute == 'SegmentsStartIntervalMean'.lower():
                csvRowString += str(segmentsStartVec[1])
            elif attribute == 'SegmentsStartIntervalSD'.lower():
                csvRowString += str(segmentsStartVec[2])
                
            elif attribute == 'TatumsStartFirst'.lower():
                csvRowString += str(tatumsStartVec[0])
            elif attribute == 'TatumsStartIntervalMean'.lower():
                csvRowString += str(tatumsStartVec[1])
            elif attribute == 'TatumsStartIntervalSD'.lower():
                csvRowString += str(tatumsStartVec[2])
            elif attribute == 'Tempo'.lower():
                csvRowString += str(hdf5_getters.get_tempo(songH5File))
            elif attribute == 'TimeSignature'.lower():
                csvRowString += str(hdf5_getters.get_time_signature(songH5File))
            elif attribute =='SectionsStartFirst'.lower():
                csvRowString+=str(sectionsStartVec[0])
            elif attribute =='SectionsStartIntervalMean'.lower():
                csvRowString+=str(sectionsStartVec[1])
            elif attribute =='SectionsStartIntervalSD'.lower():
                csvRowString+=str(sectionsStartVec[2])
            elif attribute == 'Title'.lower():
                title = str(hdf5_getters.get_title(songH5File))
                title = title.replace(',', '')
                title = title.replace(';',' ')
                title = title.replace(';',' ')
                csvRowString += title[2:-1]
            elif attribute == 'Year'.lower():
                csvRowString += str(hdf5_getters.get_year(songH5File))

            csvRowString += ","

        #Remove the final comma from each row in the csv
        lastIndex = len(csvRowString)
        csvRowString = csvRowString[0:lastIndex-1]
        csvRowString += "\n"
        outputFile1.write(csvRowString)
        csvRowString = ""

        songH5File.close()

    outputFile1.close()
	
main()
