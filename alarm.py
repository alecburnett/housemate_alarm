import os
import random
from playsound import playsound  # requires 'playsound' package

def play_random_mp3(directory):
    # Get a list of all the MP3 files in the directory
    mp3_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".mp3")]

    # Choose a random MP3 file from the list
    random_file = random.choice(mp3_files)

    # Use the 'playsound' package to play the MP3 file
    playsound(random_file)
