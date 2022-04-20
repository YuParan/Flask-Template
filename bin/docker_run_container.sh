#!/bin/bash

# Get AbPath
PROJECT_PATH=$(dirname $(cd $(dirname $0) && pwd -P))
SETTING_FILE=system/environments.yaml  # environments 파일 경로 매칭 필요

# include parse_yaml function
. $PROJECT_PATH/bin/yaml_reader.sh

# read yaml file
eval $(parse_yaml $PROJECT_PATH/$SETTING_FILE "")

docker run -d -p $server_port:$server_port \
    -v $PROJECT_PATH:/$server_name \
    --name $server_name $server_name:$server_version \
    /$server_name/bin/run_dev_server.sh
docker logs -ft --tail=50 $server_name
