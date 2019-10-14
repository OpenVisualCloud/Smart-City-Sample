#!/bin/bash -e

REPO="https://github.com/OpenVisualCloud/Ad-Insertion-Sample/archive/v19.10.tar.gz"
DIR=$(dirname $(readlink -f "$0"))

cd "$DIR"

test -d app && git rm -rf app
test -d platforms && git rm -rf platforms
mkdir tmp
cd tmp
wget -O repo.tar.gz "$REPO"
tar xvfz repo.tar.gz --strip-components=3 --wildcards '*/ad-insertion/video-analytics-service'
cp -r app ..
cp -r platforms ..
cd ..
rm -rf tmp

# workarounds
PLATFORM_LIST=("Xeon" "VCAC-A")
FRAMEWORK_LIST=("gst" "ffmpeg")
typeset -l platform

for PLATFORM in "${PLATFORM_LIST[@]}"; do
    platform=${PLATFORM}
    for FRAMEWORK in "${FRAMEWORK_LIST[@]}"; do
        framework=${FRAMEWORK}
        number=""
        internal_framework=""

        if test ${framework} == "gst"; then
            number="1"
            internal_framework="gstreamer" 
        elif test ${framework} == "ffmpeg"; then
            number="3"
            internal_framework="ffmpeg"
        fi
 
        dockerfile="platforms/${PLATFORM}/Dockerfile.${number}.va.${framework}.${platform}"
 
        if test ${PLATFORM} == "Xeon"; then
            sed -i -E "s/video_analytics_service_${internal_framework}/smtc_analytics_common_${platform}_${framework}/" $dockerfile
        elif test ${PLATFORM} == "VCAC-A"; then
            sed -i -E "s/video_analytics_service_${internal_framework}_vcac_a/smtc_analytics_common_${platform}_${framework}/" $dockerfile
        fi
        sed -i -E 's/COPY +\.\/samples.*//' $dockerfile
        sed -i -E 's/COPY +\.\/models.*//' $dockerfile
        sed -i -E 's/COPY +\.\/feeder.*//' $dockerfile
        sed -i -E 's/COPY +\.\/gallery.*//' $dockerfile
        sed -i -E 's/.*docker-entrypoint\.sh.*//' $dockerfile
        sed -i -E 's/WORKDIR +.*//' $dockerfile
        sed -i -E 's/USER +.*//' $dockerfile
        sed -i -E 's/## +.*$//' $dockerfile
        sed -i -E 's/RUN +groupadd .*//' $dockerfile
    done
done

rm -rf platforms/VCAC-A/Dockerfile*ffmpeg*
rm -rf platforms/VCAC-A/pipelines/ffmpeg

git add app platforms

