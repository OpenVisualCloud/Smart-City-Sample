#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
IFS="," read -r -a SCENARIOS <<< "${2:-traffic}"

FFMPEG_IMAGE="openvisualcloud/xeon-centos76-media-ffmpeg:20.1"
CLIPS_traffic=($(grep _traffic "$DIR"/streamlist.txt))
CLIPS_stadium=($(grep -v _traffic "$DIR"/streamlist.txt))

mkdir -p "${DIR}/archive"
for scenario in ${SCENARIOS[@]}; do
    clipz="CLIPS_$scenario[@]"
    for clip in "${!clipz}"; do
        url=$(echo "$clip" | cut -f1 -d',')
        clip_name=$(echo "$clip" | cut -f2 -d',')
        clip_mp4="${clip_name/\.*/}.mp4"
        license=$(echo "$clip" | cut -f3 -d',')

        if test ! -f "$DIR/archive/$clip_mp4"; then
            if test "$reply" = ""; then
                printf "\n\n\nThe Smart City sample requires you to have a dataset to simulate camera, please accept downloading dataset for camera simulation:\n\nDataset: $url\nLicense: $license\n\nThe terms and conditions of the data set license apply. Intel does not grant any rights to the data files.\n\n\nPlease type \"accept\" or anything else to skip the download.\n"
                read reply
            fi
            if test "$reply" = "accept"; then
                echo "Downloading..."
                tmp="tmp_$clip_name"
                wget -q -U "XXX YYY" -O "$DIR/archive/$tmp" "$url"
                docker run --rm -u $(id -u):$(id -g) -v "$DIR/archive:/mnt:rw" -it ${FFMPEG_IMAGE} ffmpeg -i /mnt/$tmp -vf scale=1280:720 -pix_fmt yuv420p -c:v libx264 -profile:v baseline -x264-params keyint=30:bframes=0 -c:a aac -f mp4 /mnt/$clip_mp4
                rm -f "$DIR/archive/$tmp"
            else
                echo "Skipping..."
            fi
        fi
    done
done

if test $(find "$DIR/archive" -name '*.mp4' -print | wc -l) -eq 0; then
    printf "\n\nNo clip is detected for camera simulation.\n\nYou can use your own video dataset. The database must be stored under sensor/simulation and must contain MP4 files encoded with H.264 (baseline, closed-GOP and no-B-frames) and AAC.\n\nIf unsure, it is recommended that you transcode your dataset with FFmpeg:\n\nffmpeg -i <source>.mp4 -c:v libx264 -profile:v baseline -x264-params keyint=30:bframes=0 -c:a aac -ss 0 <target>.mp4.\n\n"
    exit -1
fi
