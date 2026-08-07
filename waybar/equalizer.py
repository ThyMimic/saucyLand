#!/usr/bin/env python3
import subprocess

cava = subprocess.Popen(
    ["cava"],
    stdout = subprocess.PIPE,
    text = True,
    bufsize = 1
)

for line in cava.stdout:
    print(line.rstrip())
