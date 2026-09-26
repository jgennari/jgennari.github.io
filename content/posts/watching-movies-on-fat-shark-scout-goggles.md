---
title: "Watching Movies on Fat Shark Scout Goggles"
date: 2026-09-25T17:22:37-04:00
draft: false
tags: ["fpv", "ffmpeg", "maker", "troubleshooting"]
author: "Me"
categories: ["Tech"]
description: "A working SD-card movie conversion recipe for Fat Shark Scout FSV1132 goggles, including the MOV chunk-table fix that made playback work."
---

I wanted to watch a movie on my Fat Shark Scout goggles. They have an SD card slot and can play their own recordings, so I figured this would be a quick ffmpeg command. Several hours, red X thumbnails, green video, and one headset crash later, my AI assistant and I finally had a working file. The useful clue came from comparing a recording made by the goggles with the same recording repackaged by ffmpeg. The video hadn't changed, but playback stopped after a frame or two. Eventually, we got a complete 103-minute movie playing, with audio, as one file. Apparently I needed to learn about MOV chunk tables to watch a movie on my face.

## What worked

This is for the **Fat Shark Scout FSV1132**. The native recordings I inspected contained H.264 video and AAC audio in a `3gp4`-branded MOV file.

The working recipe uses:

- **Video:** 720×480, letterboxed, square pixels, BT.709 SDR, H.264 Main, 60000/1001 fps. One reference frame, no B-frames, a keyframe every 15 frames.
- **Audio:** AAC-LC, stereo, 32 kHz, 128 kbit/s.
- **Timing:** video samples of 1001 ticks at a 60000 timescale; audio samples of 1024 ticks at 32000.
- **Packaging:** remove H.264 SEI data, disable edit lists, and use **one sample per chunk for both tracks**.

That last item was the breakthrough. The goggles' recordings used one sample per chunk. Our ffmpeg files grouped samples into chunks. Rewriting the `stsc` (sample-to-chunk) and `stco` (chunk-offset) tables fixed playback without changing the encoded video or audio. That points to a limitation in the goggles' container parser.

I later disassembled [released PowerPlay firmware](https://orqafpv.freshdesk.com/support/solutions/articles/48001281127-powerplay) and found that its MOV writer explicitly creates one `stsc` entry with one sample per chunk. The [Scout manual](https://myosuploads3.banggood.com/products/20190613/20190613044907ScoutManualRevD.pdf) calls its recorder a PowerPlay DVR, although I can't confirm it runs the same firmware build. The native recordings also contain a large `skip` box, but the working movie plays without one.

Matched tests finally isolated the MOV quirk. Two files had the same video and audio packets, timestamps, and chunk offsets. With video `stsc` entries `(1,1,1), (3,2,1), (5,1,1)`, playback stopped after a frame or two. Adding a redundant `(4,2,1)` entry made the otherwise identical file play through. So the Scout can play two-sample chunks, but this firmware mishandles a two-sample `stsc` entry that spans consecutive chunks. I still don't have the Scout's own firmware to identify the faulty instruction.

**September 26 update:** I checked the released PowerPlay v2.0032.01 reader as well. One path tracks samples within chunks and waits for the next `stsc` entry boundary; another sample-stepping path remains ambiguous. My Scout reports version `1.0032.0058`, so I can't confirm that the released image contains the same bug. The matched playback tests establish what fails on the Scout, not which firmware instruction causes it.

Removing SEI data had already fixed the thumbnails, but wasn't enough for sustained playback. This is the combined recipe that worked, not a claim that every encoder setting is mandatory.

## Make a file

Download [encode-scout.sh](/downloads/fatshark-scout/encode-scout.sh) and [one_sample_chunks.py](/downloads/fatshark-scout/one_sample_chunks.py) into the same directory. You'll need Python 3 and ffmpeg with `libx264`; HDR10 conversion also needs `zscale` and `tonemap`.

```bash
# For an HDR10 source. Use "sdr" for BT.709 SDR input.
bash encode-scout.sh input.mkv scout hdr10

# Fix the container after encoding. Don't remux the result afterward.
python3 one_sample_chunks.py scout/timed.MOV \
  scout/MOV180101-000000-000001F.MOV

# Check that the whole file decodes without errors.
ffmpeg -v error -i scout/MOV180101-000000-000001F.MOV -f null -
```

The shell script uses the first video and audio tracks, tone-maps HDR10 when requested, and applies ffmpeg's [`filter_units` and `setts` bitstream filters](https://www.ffmpeg.org/ffmpeg-bitstream-filters.html) to remove SEI and normalize timestamps. The Python script changes only the chunk tables and their enclosing box sizes. It requires a nonfragmented file with `moov` at the end and 32-bit offsets, which is what the shell script produces for files under 4 GB.

Copy the final MOV into the card's `DCIM` directory, using an unused filename in that format. Keep it under FAT32's 4 GB per-file limit, preserve your recordings, and safely eject the card. On a Mac, remove any `._` sidecar created for the copied movie. My full movie was about **1.03 GB**, so splitting it into ten-minute files turned out to be unnecessary.
