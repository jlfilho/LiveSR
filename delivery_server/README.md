# The Delivery Live Stream Server

This module uses NGINX with the RTMP module (dash enhanced version) to implement the live video delivery server.

The Dockerfile builds an image with NGINX compiled with the RTMP module (dash enhanced version) and copies the configuration file nginx.conf for the rtmp to operate on port 1935 and http on port 8080.

The docker-compose automates the creation of the container for the server to function as a microservice.


# Dependencies 

To build and run the server it is necessary to have Docker and docker-compose installed, see the links below to learn how to install them.

* Install Docker: https://docs.docker.com/engine/install/ubuntu/
* Install Docker-compose: https://docs.docker.com/compose/install/

# Configure the nginx.conf file:

Configure the ip.
```bash
dash_clock_helper_uri http://192.168.100.20:8080/time;
```
Configure the bitrates to dash,
```bash
dash_variant _low  bandwidth="700000"  width="640"  height="360";
dash_variant _med  bandwidth="1600000"  width="960"  height="540";
dash_variant _high  bandwidth="2800000"  width="1280"  height="720";
dash_variant _uhigh  bandwidth="4300000" width="1920"  height="1080" max;
```
Confgigure the biterate to hls,
```bash
hls_variant _low   BANDWIDTH=700000;
hls_variant _med   BANDWIDTH=1600000;
hls_variant _high BANDWIDTH=2800000;
hls_variant _uhigh BANDWIDTH=4300000;
```
# Building and Running the Delivery Server

To run the delivery server, enter into delivery_server folder and run:
```bash
$ ./deploy.sh -s delivery-server -b
```
# Stoping service
```bash
$ ctrl + c
```

# Test end-to-end flow

To test this module you need Ingest-server and transcode-service.

Run
```bash
./deploy.sh -s transcode-service,ingest-server,delivery-server -b
```

Use OBS-studio to send a streaming to rtmp://$ingest-server-ip:1936/live/$key

# Watching a Live

Once Ingest-server and transcode-service is sending the stream it will be available over DASH and HLS. For DASH the URL will be http://<your_domain>:8080/dash/<key>.mpd. For HLS, the URL will be http://<your_domain>/hls/<key>.m3u8.

Open a browser and access the url:
http://<delivery-server-ip>:8080/live

Choose a ABR algorithm link and inform the mpd url
http://<delivery-server-ip>:8080/dash/<key>.mpd