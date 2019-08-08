#!/bin/bash -e

REPO="https://github.com/OpenVisualCloud/Ad-Insertion-Sample/archive/v1.1.tar.gz"
DIR=$(dirname $(readlink -f "$0"))

cd "$DIR"

test -d app && git rm -rf app
test -d platforms && git rm -rf platforms
mkdir tmp
cd tmp
wget -O repo.tar.gz "$REPO"
tar xvfz repo.tar.gz --strip-components=3 --wildcards '*/ad-insertion/video-analytics-service'
rm -rf platforms/VCAC*
rm -rf platforms/Xeon/Dockerfile*ffmpeg*
rm -rf platforms/Xeon/pipelines/ffmpeg
cp -r app ..
cp -r platforms ..
cd ..
rm -rf tmp

# workarounds
dockerfile="platforms/Xeon/Dockerfile.1.va.gst.xeon"
sed -i -E 's/video_analytics_service_gstreamer/smtc_analytics_common/' $dockerfile
sed -i -E 's/COPY +\.\/samples.*//' $dockerfile
sed -i -E 's/COPY +\.\/models.*//' $dockerfile
sed -i -E 's/COPY +\.\/feeder.*//' $dockerfile
sed -i -E 's/.*docker-entrypoint\.sh.*//' $dockerfile
sed -i -E 's/WORKDIR +.*//' $dockerfile
sed -i -E 's/USER +.*//' $dockerfile
sed -i -E 's/## +.*$//' $dockerfile
sed -i -E 's/RUN +groupadd .*//' $dockerfile

git add app platforms

