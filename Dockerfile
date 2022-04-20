# Base Image
FROM ubuntu:20.04
FROM python:3.8.12

# ARG PROJECT_NAME=server
ARG PROJECT_NAME=nameless_server
ARG PROJECT_PORT=5050

ENV PYTHONUNBUFFERED 1

# Set locale
ENV LC_ALL=C.UTF-8

# General Packages
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && apt-get install -y unixodbc-dev \
    && apt-get install -y build-essential \
    && apt-get install -y python-dev \
    && apt-get install -y python3-pip \
    && apt-get install -y default-libmysqlclient-dev

# Upgrading pip
RUN python -m pip install pip --upgrade
RUN apt-get update

# Setup Folders
RUN mkdir -p /${PROJECT_NAME}

# Move to working directory
WORKDIR /${PROJECT_NAME}

# Add working directory
COPY . /${PROJECT_NAME}

# Setup requirements
RUN mkdir -p ~/.pip \
    && cp /${PROJECT_NAME}/bin/pip.conf ~/.pip/pip.conf \
    && cd ~/.pip \
    && cd /${PROJECT_NAME} \
    && pip3 install -r requirements.txt

# Open Port for the Python App
EXPOSE ${PROJECT_PORT}

# Setting chmod bin/*.sh
CMD chmod -R 755 /${PROJECT_NAME}/bin

# CMD ["chmod", "+x", "/${PROJECT_NAME}/bin/run_uwsgi_sever.sh"]
# ENTRYPOINT ["/${PROJECT_NAME}/bin/run_uwsgi_sever.sh"]