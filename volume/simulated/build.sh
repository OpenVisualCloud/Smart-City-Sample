#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
IMAGE=openvisualcloud/xeon-centos76-media-ffmpeg
CLIPS=(https://www.pexels.com/video/1388383/download,1388383.mp4,10,https://www.pexels.com/photo-license)

declare -A ACCEPTS
printf "\n\n\n"
for clip in "${CLIPS[@]}"; do
    url=$(echo "$clip" | cut -f1 -d',')
    clip_name=$(echo "$clip" | cut -f2 -d',')
    duration=$(echo "$clip" | cut -f3 -d',')
    license=$(echo "$clip" | cut -f4 -d',')

    if test ! -f "$DIR/$clip_name"; then
        printf "Downloading $url for camera simulation...\n"
        if test -z "${ACCEPTS[$license]}"; then
            printf "\n\nData set subject to $license. The terms and conditions of the data set license apply. Intel does not grant any rights to the data files.\n\n\nPlease type \"accept\" or anything else to skip the download.\n"
            read reply
            if test $reply == "accept"; then
                ACCEPTS[$license]="accept"
            fi
        fi
        if test -n "${ACCEPTS[$license]}"; then
            echo "Downloading..."
            tmp="$clip_name.tmp.mp4"
            wget -q -O "$DIR/$tmp" "$url"
            sudo docker run -u $(id -u):$(id -g) -v "$DIR:/mnt:rw" -it $IMAGE ffmpeg -i /mnt/$tmp -c:v libx264 -profile:v baseline -x264-params keyint=30:bframes=0 -c:a aac -ss 0 -t $duration -f mp4 /mnt/$clip_name
            rm -f "$DIR/$tmp"
        else
            echo "Skipping..."
        fi
    fi
done

if test "$(find $DIR -name '*.mp4' -print | wc -l)" -eq 0; then
    printf "\n\nNo clip is detected for camera simulation.\n\n"
fi
