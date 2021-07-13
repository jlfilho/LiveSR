#!/bin/bash

export INGEST_IP='192.168.100.20' #$(hostname -I | cut -f1 -d' ')
export DELIVERY_IP='192.168.100.20'
export TRANSCODE_IP='192.168.100.20'

function PrintUsage() {
    echo -e "Usage:\n`basename $0` <-s> ARGS [-bf]\n"
    echo -e "Ex.: ./`basename $0` -s all -b"
    echo -e "Ex.: ./`basename $0` -s ingest-server,delivery-server -b"
    echo -e "Options: \n -s \n   all | delivery-server,ingest-server,transcoder-service,sr-service,colletor-srver \n"
    echo -e " -b \n   Build images before creating containers." 
    echo -e " -f \n   Recreate containers even if their configuration and image haven't changed."
    exit
}



function removeContainer() {
    nameContainer=$1
    red=`tput setaf 1`
    green=`tput setaf 2`
    reset=`tput sgr0`
    echo -e "Removing ${nameContainer} ... "
    docker ps -qa --filter "name=$nameContainer" | grep -q . && docker stop $nameContainer && docker rm -fv $nameContainer && echo -e "${green} done" || echo -e "${red} fail"
    echo ${reset}
}

while getopts s:bf flag
do
    case "${flag}" in
        s) set -f 
           IFS=',' 
           service=($OPTARG) ;;
        b) HAS_BUILD='--build';;
        f) HAS_FORCE='--force-recreate';;
        ?) PrintUsage;;
    esac
done


export PROJ_DIR=$(pwd)

export DELIVERY_SERVER_HTTP_PORT=8080
export DELIVERY_SERVER_RTMP_PORT=1935
export INGEST_SERVER_RTMP_PORT=1936
export INGEST_SERVER_HTTP_PORT=8181
export TRANSCODE_SERVICE_RTMP_PORT=1937
export TRANSCODE_SERVICE_HTTP_PORT=8282
export COLLECTOR_SERVER_HTTP_PORT=9191

export INGEST_SERVER_PATH=$PROJ_DIR/ingest_server
export TRANSCODER_SERVER_PATH=$PROJ_DIR/transcode_service
export DELIVERY_SERVER_PATH=$PROJ_DIR/delivery_server
export SR_SERVICE_PATH=$PROJ_DIR/sr_service
export COLLECTOR_SERVER_PATH=$PROJ_DIR/collector_server
export PLAYER_CLIENT_PATH=$PROJ_DIR/player_client


export TRACE_PATH=$PROJ_DIR/share/traces
export CONFIG_PATH=$PROJ_DIR/share/conf
export COLLECTOR_RESULTS_PATH=$PROJ_DIR/share/results-collector # can be share between containers
export DELIVERY_SERVER_PUBLIC_PATH=$PROJ_DIR/share/www/html
export BROWSER_DIR_PATH=$PROJ_DIR/share/abr_browser_dir


#export IS_SR=$(yq eval .enviroment.is_sr $CONFIG_PATH/config.yml)
#cp $CONFIG_PATH/config.yml $SR_SERVICE_PATH/src/

if [ -z "$service" ]; then
        echo 'Missing -s' >&2
        PrintUsage
        exit 1
fi

if [ ${service[@]} = "all" ]; then
    if [ -d "$DELIVERY_SERVER_PATH/tmp/" ]; then sudo rm -Rf $DELIVERY_SERVER_PATH/tmp/; fi
    removeContainer "delivery-server"
    removeContainer "ingest-server"
    removeContainer "transcoder-service"
    removeContainer "sr-service"
    removeContainer "collector-service"
    removeContainer "player-client"
    echo "Starting ${service[@]}"
    docker-compose up $HAS_BUILD $HAS_FORCE
else
    for i in "${service[@]}"; do
        removeContainer ${i} 
        echo ${i}
        if [ "${i}" = "delivery-server" ]; then
            if [ -d "$DELIVERY_SERVER_PATH/tmp/" ]; then 
                echo -n "Removing tmp folder... "
                sudo rm -Rf $DELIVERY_SERVER_PATH/tmp/ && echo "${green} done" || echo "${red} fail"; 
                echo ${reset}
            fi
        fi
        if [ "${i}" = "collector-server" ]; then
            if [ -d "$COLLECTOR_RESULTS_PATH" ]; then 
                echo -n "Removing collector logs... "
                sudo rm -fv ${COLLECTOR_RESULTS_PATH}/*.json && echo "${green} done" || echo "${red} fail"; 
                echo ${reset}
            fi
        fi
        
    done
    echo "Starting ${service[@]}"
    docker-compose up $HAS_BUILD $HAS_FORCE ${service[@]}
fi