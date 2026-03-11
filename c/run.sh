#!/usr/bin/env bash
#
# Start an instance of the jetson-inference docker container.
# This script will resume an existing container if one exists,
# or create a new one if it doesn't.
#
# Usage:
#   1. Build the image first:
#        docker build -t jetson-inference-firebase .
#
#   2. Run this script from the root of the jetson-inference project:
#        ./docker/run.sh
#

CONTAINER_NAME="jetson-inference-persistent"
CONTAINER_IMAGE="jetson-inference-firebase"

# paths to some project directories
CLASSIFY_DIR="python/training/classification"
DETECTION_DIR="python/training/detection/ssd"
RECOGNIZER_DIR="python/www/recognizer"

DOCKER_ROOT="/jetson-inference"

# generate mount commands
DATA_VOLUME=" \
--volume $PWD/data:$DOCKER_ROOT/data \
--volume $PWD/$CLASSIFY_DIR/data:$DOCKER_ROOT/$CLASSIFY_DIR/data \
--volume $PWD/$CLASSIFY_DIR/models:$DOCKER_ROOT/$CLASSIFY_DIR/models \
--volume $PWD/$DETECTION_DIR/data:$DOCKER_ROOT/$DETECTION_DIR/data \
--volume $PWD/$DETECTION_DIR/models:$DOCKER_ROOT/$DETECTION_DIR/models \
--volume $PWD/$RECOGNIZER_DIR/data:$DOCKER_ROOT/$RECOGNIZER_DIR/data "

# check for V4L2 devices
V4L2_DEVICES=""

for i in {0..9}
do
    if [ -a "/dev/video$i" ]; then
        V4L2_DEVICES="$V4L2_DEVICES --device /dev/video$i "
    fi
done

# check for display
DISPLAY_DEVICE=""

if [ -n "$DISPLAY" ]; then
    sudo xhost +si:localuser:root
    DISPLAY_DEVICE=" -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix "
fi

# Check if container already exists
if [ "$(sudo docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
    echo "Found existing container '$CONTAINER_NAME'..."

    # If container is stopped, start it
    if [ "$(sudo docker ps -aq -f status=exited -f name=^${CONTAINER_NAME}$)" ]; then
        echo "Container is stopped - starting it..."
        sudo docker start $CONTAINER_NAME
    else
        echo "Container is already running..."
    fi

    # Attach to the container
    echo "Attaching to container..."
    sudo docker exec -it $CONTAINER_NAME bash

else
    echo "No existing container found - creating '$CONTAINER_NAME' for the first time..."

    cat /proc/device-tree/model > /tmp/nv_jetson_model

    # Create new persistent container (no --rm)
    sudo docker run --runtime nvidia -it \
        --name $CONTAINER_NAME \
        --network host \
        -v /tmp/argus_socket:/tmp/argus_socket \
        -v /etc/enctune.conf:/etc/enctune.conf \
        -v /etc/nv_tegra_release:/etc/nv_tegra_release \
        -v /tmp/nv_jetson_model:/tmp/nv_jetson_model \
        -v /var/run/dbus:/var/run/dbus \
        -v /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket \
        -w $DOCKER_ROOT \
        $DISPLAY_DEVICE $V4L2_DEVICES \
        $DATA_VOLUME \
        $CONTAINER_IMAGE bash
fi
