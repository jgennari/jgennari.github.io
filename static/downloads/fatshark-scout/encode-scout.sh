#!/usr/bin/env bash
# Encode and normalize timing. Run one_sample_chunks.py afterward.
# Requires ffmpeg with libx264; HDR10 mode also requires zscale and tonemap.
set -euo pipefail

if [[ $# != 3 || ( "$3" != hdr10 && "$3" != sdr ) ]]; then
  echo 'Usage: bash encode-scout.sh INPUT NEW_OUTPUT_DIRECTORY hdr10|sdr' >&2
  exit 2
fi

source=$1
work=$2
mode=$3
ffmpeg_bin=${FFMPEG:-ffmpeg}
mkdir "$work" # Refuse to overwrite a previous conversion.

vf='scale=w=720:h=480:force_original_aspect_ratio=decrease:force_divisible_by=2'
if [[ "$mode" == hdr10 ]]; then
  vf+=',zscale=t=linear:npl=100,format=gbrpf32le,tonemap=tonemap=hable:desat=0'
  vf+=',zscale=t=bt709:m=bt709:p=bt709,format=yuv420p'
else
  # SDR mode expects BT.709 input and skips HDR tone mapping.
  vf+=',format=yuv420p'
fi
vf+=',pad=720:480:(ow-iw)/2:(oh-ih)/2,setsar=1'
vf+=',sidedata=mode=delete:type=MASTERING_DISPLAY_METADATA'
vf+=',sidedata=mode=delete:type=CONTENT_LIGHT_LEVEL,fps=60000/1001'

"$ffmpeg_bin" -hide_banner -nostdin -n -i "$source" \
  -map 0:v:0 -map 0:a:0 -map_metadata -1 -map_chapters -1 \
  -vf "$vf" \
  -c:v libx264 -preset veryfast -crf 18 -profile:v main -level:v 3.0 \
  -x264-params 'bframes=0:ref=1:keyint=15:min-keyint=15:scenecut=0:weightp=0' \
  -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a aac -ar 32000 -ac 2 -b:a 128k -metadata:s:a:0 title= \
  -movie_timescale 60000 -video_track_timescale 60000 \
  -use_editlist 0 -write_btrt 0 -brand 3gp4 -f 3gp "$work/encoded.MOV"

"$ffmpeg_bin" -hide_banner -nostdin -n -i "$work/encoded.MOV" \
  -map 0:v:0 -map 0:a:0 -c copy \
  -bsf:v 'filter_units=remove_types=6,setts=pts=N*1001:dts=N*1001:duration=1001:time_base=1/60000' \
  -bsf:a 'setts=pts=N*1024:dts=N*1024:duration=1024:time_base=1/32000' \
  -map_metadata -1 -map_chapters -1 \
  -movie_timescale 60000 -video_track_timescale 60000 \
  -use_editlist 0 -brand 3gp4 -f 3gp "$work/timed.MOV"

printf '\nNext: python3 one_sample_chunks.py "%s/timed.MOV" "%s/MOV180101-000000-000001F.MOV"\n' "$work" "$work"
