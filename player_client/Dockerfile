FROM ubuntu:latest
LABEL Description="Ingest client for live stream" Vendor="Joao da Mata" Version="1.0"
ARG DEBIAN_FRONTEND=noninteractive

# Install Dependencies
RUN apt-get update 
RUN apt-get install -qy mahimahi \
    sudo netcat ffmpeg python3-pip build-essential wget \
    libssl-dev libffi-dev python3-dev \
    xvfb xserver-xephyr tigervnc-standalone-server xfonts-base \
    fonts-liberation xdg-utils  
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
&& dpkg -i google-chrome-stable_current_amd64.deb && apt-get install -f 

WORKDIR /scripts


COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Create a user 'client' for use Mahimahi
RUN useradd -ms /bin/bash client
RUN usermod -aG sudo client
# Chown all the files to the app user.
RUN chown -R client:client /scripts
# No password to run scripts in the container
RUN echo "client ALL=(ALL)NOPASSWD:ALL" >> /etc/sudoers
# Switch to 'client'
#USER client

