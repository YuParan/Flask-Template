#!/bin/bash

# Get AbPath
PROJECT_PATH=$(dirname $(cd $(dirname $0) && pwd -P))
SETTING_FILE=system/environments.yaml  # environments 파일 경로 매칭 필요

# include parse_yaml function
. $PROJECT_PATH/bin/yaml_reader.sh

# read yaml file
eval $(parse_yaml $PROJECT_PATH/$SETTING_FILE "")

docker container stop $server_name
docker container rm $server_name
