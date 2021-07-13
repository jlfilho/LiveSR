# Player-client 

Player Client implements the clients that are attending the Live streaming. To automate this process, we implemented a module in python using the Selenium library that generates the video sessions using the Chrome browser (91.0). This module also has the behavior of the network link (bandwidth and delay) emulated using the Mahimahi tool.

# Dependencies 

To build and run the server it is necessary to have Docker and docker-compose installed, see the links below to learn how to install them.

* Install Docker: https://docs.docker.com/engine/install/ubuntu/
* Install Docker-compose: https://docs.docker.com/compose/install/

## Configuration:

Configure the parameters in share/conf/config.yml

``` bash
player_client:
  session:
    url: 'http://192.168.100.20:8080' # ip and http port of delivery server
    run_time: 405 # runtime of session
    default_chrome_user_dir: '/browser/chrome_data_dir' # path to default chrome user dir 
    chrome_driver: '/browser/chromedriver_linux64/chromedriver' # path to chrome drive used by Selenium 
    visible_virtual_display: False # Only set True if you run outside a container
    abr_algo: ['abrBola','abrL2A','abrLoLP'] # List of abr algorithm 
  channel_to_delivery:
    mm_delay: "40" # network delay
    traces_downlink: "/traces/cooked_group1/1/" #You can choose another trace available in the tracer folder 
    uplink: "/traces/12Mbps" # trace upload link 
```

## Run the player-client:

To run the player client, make sure the server modules are running and there are some live streaming.

``` bash
./deploy.sh -s player-client -b
```

6. The logs will be write in dir share/results-collector