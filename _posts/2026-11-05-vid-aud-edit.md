---
layout: post
title: "Some Multimedia (Audio/Video) Handling Resources"
date: 2026-11-05 01:00:00-0000
categories:
---

This post is just some personal notes about handling audio and video files.  
I will be dumping in here commands, links etc, now that I am experimenting with including audio and/or video in some of my posts.

## Remove last x seconds from a video

```bash
# Find the total duration of the video in seconds
ffprobe -i input.mp4 -show_entries format=duration -v quiet -of csv="p=0"

# Subtract 2 seconds from that total duration
dur=$(ffprobe -i input.mp4 -show_entries format=duration -v quiet -of csv="p=0")
new_end=$(awk "BEGIN {print $dur - 2}")
ffmpeg -i input.mp4 -t "$new_end" -c copy output.mp4
```

## Metadata

```bash
# View all metadata
exiftool video.mp4

# Remove all clearable metadata (leaves a backup copy)
exiftool -all= video.mp4

# Remove metadata directly without saving a backup
exiftool -overwrite_original -all= video.mp4

# ExifTool might leave some stuff. FFmpeg completely strips everything
ffmpeg -i input.mp4 -map_metadata -1 -c:v copy -c:a copy output.mp4
```

More tricks to come (if I ever need them) ...
