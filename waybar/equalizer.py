#!/usr/bin/env python3
import subprocess


""" 
Not too sure about this, pretty sure though that this executes cava since python is technically
the first thing we really open in this entire data pipeline. The whole subprocess thing just makes
cava technically the CHILD of the python program, like such: 

Forgive me my internet overlords, this is my first time dealing with anything subprocess pipeline
related
   waybar       
      equalizer.py  <-^ (averages data to send back to waybar)
         cava > > >---| (sends data back to the script)
         
         
         For future reference: 
         - subprocess.Popen is process open, the line that actually opens the command
         - ["cava"] is the command that's opening, basically like typing "cava" in terminal
         - stdout is the output cava is sending here instead of sending to the terminal, it makes the pipe
            - In other words, you change the path the data flows to from cava to terminal to cava to script
         - text = true tells python not to interpret the piped data as bytes and lets you change it
         - buffering lets python get a line from cava one at a time
            - So instead of playing a song and finishing and python not getting the data until it's done
              cava sends it one at a time, important for the equalizer very much so
         
    
"""
cava = subprocess.Popen(
    ["cava"],
    stdout = subprocess.PIPE,
    text = True,
    bufsize = 1
)

# Note that strip just removes outside stuff, split removes inside afterwords

#This is basically saying for every line of output cava sends, do allat
for line in cava.stdout:
    values = line.strip().strip(";").split(";")

    #Just checking to make sure everything in the original string was split up correctly
    if len(values) != 8:
        continue

    #This forms the array of integers from the split string array made earlier
    values = [int(value) for value in values]

    #THIS forms the array of averaged values, moving from an 8 element array to a 4 element array
    four_bands = [
        max(values[0] + values[1]),
        max(values[2] + values[3]),
        max(values[4] + values[5]),
        max(values[6] + values[7])
    ]
    smoothed_bands =[]
    previous_bands = [0.0, 0.0, 0.0, 0.0]
    for old, new in zip(previous_bands, four_bands):
        if new > old:
            smoothed = old * 0.3 + new * 0.7
        else:
            smoothed = old * 0.8 + new * 0.2
        smoothed_bands.append(smoothed)


    bars = "▁▂▃▄▅▆▇█"
    visualizer = " ".join(
        bars[min(int(value/100 * len(bars)), len(bars) - 1)]
        for value in smoothed_bands
    )

    #Flush just prevents python from accidentally chunking data together
    print(visualizer, flush=True)
