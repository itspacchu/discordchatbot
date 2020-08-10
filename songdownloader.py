import subprocess as sp
import os
import subprocess

#Made for another Git project

def download_song(query:str):
    currentpath = os.getcwd()
    spotdlcommand = ' '
    if('youtube' in query):
        spotdlcommand = f'spotdl -s {query} -f ' + currentpath
    else:
        spotdlcommand = f'spotdl -s "{query}" -f '+ currentpath

    print("Running command " + spotdlcommand)
    #output = subprocess.check_output(spotdlcommand, shell=True)
    os.system(spotdlcommand)
