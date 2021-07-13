# The Ingest Server Live Stream

This module uses NGINX with the RTMP module to implement the live video ingest server.

The Dockerfile builds an image with NGINX compiled with the RTMP module and copies the configuration file nginx.conf for the server to operate on port 1935.

The docker-compose automates the creation of the container for the server to function as a microservice.

# Dependencies 

To build and run the server it is necessary to have Docker and docker-compose installed, see the links below to learn how to install them.

* Install Docker: https://docs.docker.com/engine/install/ubuntu/
* Install Docker-compose: https://docs.docker.com/compose/install/

# Config IP

Open the file ingest_server/nginx.conf and configure the transcode ip.
    Ex.: push 192.168.100.20:1937/transcode4;

# Building and Running the Ingest Server

To run the ingest server, enter into ingest_server folder and run:

$ ./deploy.sh -s ingest-server -b

# Stoping service

$ ctrl + c

# Live Broadcast Address

To start a live stream, configure the client to stream for rtmp://$SERVER-IP:1936/live/$key

Where $SERVER-IP is your server's IP and $key is a custem key defined in the transmission.

As a client rtmp you can use the OBS-studio tool or some other application.

# Watching a Live

You can watch the live using the VLC player to access the rtmp://$SERVER-IP:1936/live/$key address