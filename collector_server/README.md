# The Metrics Collector API

This API collects metrics genereted by video client players.

The Dockerfile builds an image with python3 and flask on port 8300.

The docker-compose automates the creation of the container for the server to function as a microservice.

## Dependencies 

To build and run the server it is necessary to have Docker and docker-compose installed, see the links below to learn how to install them.

* Install Docker: https://docs.docker.com/engine/install/ubuntu/
* Install Docker-compose: https://docs.docker.com/compose/install/

## Building and Running the Colletor

To run the Collector, enter into metrics-collector-api folder and run:

First time:
```sh
$ ./start.sh --build
```
## Stoping service
```sh
$ sudo docker-compose stop
```
## Parameters

### Header
Content-Type: Type of application content. Ex: application/json

sessionId: UniqueId of session - This parameter is used to build the name of cvs. file
Ex.: 7a19c7ed-9984-4a19-9dd4-5590e49d4aad (uuid) or 1615852124 (unix time epoch)  

abr: Algorithm name - This parameter is used to build the name of cvs. file 
Ex.: BB 

### Body POST

	- throughput: bandwith of channel estimated of client-side - bits/s,
    - bitrate: bitrate used to encoding video, can be calculed by: segmentSize/segmentDuration - bits/s,
    - qualityLevel: number of quality selected,
    - segmentSize: size of the segment downloaded - bytes,
    - segmentDuration: duration of the segment downloaded - seconds,
    - segmentDelay: a period of time between requisition time and the start of the download of a segment - seconds,
    - bufferLevel: level of buffer ocupation - seconds,
    - rebufferingTime: period time in each buffer get empty - seconds,
    - downloadStartTime: initial time of a segment download, 
	- downloadFinishTime: final time of a segment download

#### Ex.: 
```json
{	
	"throughput": 1000.0,
    "bitrate": 900.0,
    "qualityLevel": 2,
    "segmentSize": 400,
    "segmentDuration": 2000,
    "segmentDelay": 1000,
    "bufferLevel": 10000,
    "rebufferingTime": 444,
    "downloadStartTime": 20392039239, 
	"downloadFinishTime": 20392039239
}
```