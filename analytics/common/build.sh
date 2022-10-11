#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

download_image(){
	URL=https://raw.githubusercontent.com/OpenVisualCloud/Dockerfiles/v22.3/Xeon/ubuntu-20.04/analytics/gst/Dockerfile
	TARGET="${DIR}/Xeon/gst/Dockerfile.1.gst"

	if test -f $TARGET; then
		return
	fi

	wget $URL -O $TARGET
	sed -i '1i # smtc_analytics_base ' $TARGET
	sed -i 's/v1.5.3/v1.4.1/g' $TARGET  #downgrade dlstreamer
	sed -i '636d' $TARGET
}


download_image
. "${DIR}/../../script/build.sh"
