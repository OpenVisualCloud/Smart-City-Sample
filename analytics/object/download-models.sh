#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

download()
{
	MODEL_NAME=$1
	MODEL_PRICISION=$2
	MODEL_PATH=$3
	
	DATA_IMAGE="openvino/ubuntu20_data_dev:2021.4.2"
	TOOLS_PATH="/opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader"

	if test -f "${MODEL_PATH}/${MODEL_PRICISION}/${MODEL_NAME}.xml"; then
		echo "model exist at ${MODEL_PATH}/${MODEL_PRICISION}"
		return
	fi

	echo "will download model : ${MODEL_NAME}"
	sleep 1

	#set -x

	EX_FILE="${MODEL_PATH}/_download.sh"
	echo "#!/bin/bash -ex" > $EX_FILE
	echo "python3 ${TOOLS_PATH}/downloader.py --name ${MODEL_NAME} --precisions ${MODEL_PRICISION} -o /mnt" >> $EX_FILE
	echo "python3 ${TOOLS_PATH}/converter.py --name ${MODEL_NAME} --precisions ${MODEL_PRICISION} --download_dir /mnt -o /mnt" >> $EX_FILE

	docker run --rm -u $(id -u):$(id -g) -v "${MODEL_PATH}:/mnt:rw" -it ${DATA_IMAGE} bash /mnt/_download.sh

	mv "${MODEL_PATH}/public/${MODEL_NAME}/${MODEL_PRICISION}" "${MODEL_PATH}"
	rm -rf "${MODEL_PATH}/public"
	rm $EX_FILE
}

download yolo-v4-tiny-tf FP32 "${DIR}/models/yolo-v4-tiny-tf/1"
