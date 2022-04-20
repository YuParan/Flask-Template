#!/bin/bash

# Get AbPath
PROJECT_PATH=$(dirname $(cd $(dirname $0) && pwd -P))
echo $PROJECT_PATH
SETTING_FILE=system/environments.yaml  # environments 파일 경로 매칭 필요

# include parse_yaml function
. $PROJECT_PATH/bin/yaml_reader.sh

# read yaml file
eval $(parse_yaml $PROJECT_PATH/$SETTING_FILE "")

# Cross-platform CPU(M1 Mac) 대응을 위해 `--platform linux/amd64` 가 필요 합니다
docker build --platform linux/amd64 \
    --build-arg PROJECT_NAME=$server_name \
    --build-arg PROJECT_PORT=$server_port \
    -t $server_name:$server_version .
