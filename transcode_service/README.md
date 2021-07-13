# The Transcode-service

This module uses NGINX with the RTMP module to implement the transcode-service.

The Dockerfile builds an image with NGINX compiled with the RTMP module and copies the configuration file nginx.conf for the server to operate on port 1937.

The docker-compose automates the creation of the container for the server to function as a microservice.

# Dependencies 

To build and run the server it is necessary to have Docker and docker-compose installed, see the links below to learn how to install them.

* Install Docker: https://docs.docker.com/engine/install/ubuntu/
* Install Docker-compose: https://docs.docker.com/compose/install/

# Building and Running the Transcode-service

To run the Transcode-service, in the root run:

$ ./deploy.sh -s transcode-service -b

# Stoping service

$ crtl + c

# Test transcode

To start a live stream, configure the client to stream for rtmp://$SERVER-IP:1937/transcode4/$key

Where $SERVER-IP is your server's IP and $key is a custem key defined in the transmission.


# Broadcasting a Live
As a client rtmp you can use the OBS-studio tool or some other application.

# Watching a Live by RTMP
You can watch the live using the VLC player to access the rtmp://$SERVER-IP:1937/transcode4/$key address