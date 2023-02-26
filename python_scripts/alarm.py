#!/usr/bin/env python3

import os
import random
from pydub import AudioSegment
from pydub.playback import play


directory = '/home/alexanderjmburnett1991/git/housemate_alarm/mp3_files'

def play_random_mp3(directory):
    # Get a list of all the MP3 files in the directory
    mp3_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".mp3")]

    # Choose a random MP3 file from the list
    random_file = random.choice(mp3_files)

    print(random_file)

    song = AudioSegment.from_mp3(random_file)

    # Use the 'playsound' package to play the MP3 file
    play(song)


play_random_mp3(directory)