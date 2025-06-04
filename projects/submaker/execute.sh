#! /bin/bash

for file in s1/*.mp4; do
    echo "Processing $file"
    ffmpeg -i "$file" -q:a 0 -map a "output.mp3"
    echo "Transcribing audio $file"
    python3 main.py
    echo "Moving subtitle file $file"
    mv output.srt "s1/${file}.srt"
    echo "Cleaning up $file"
    rm output*
done