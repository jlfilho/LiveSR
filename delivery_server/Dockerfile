
FROM ubuntu:latest
LABEL Description="Delivery server for adaptive live stream" Vendor="Joao da Mata" Version="1.0"
ARG DEBIAN_FRONTEND=noninteractive

# Install Dependencies
RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install -y build-essential 
RUN apt-get install -y libpcre3-dev 
RUN apt-get install -y zlib1g-dev 
RUN apt-get install -y libssl-dev
RUN apt-get install -y ffmpeg


# Cloning into nginx-rtmp-module
RUN git clone https://github.com/chetandhembre/nginx-rtmp-module.git
# Cloning into nginx
RUN git clone https://github.com/nginx/nginx.git

# Compiling nginx
RUN cd nginx \
    && ./auto/configure --add-module=../nginx-rtmp-module --with-cc-opt="-Wimplicit-fallthrough=0" \
    && make \
    && make install

RUN rm -r nginx
RUN rm -r nginx-rtmp-module
RUN apt-get remove -y git
RUN apt-get remove -y build-essential


ENV PATH /usr/local/nginx/sbin:$PATH

EXPOSE ${DELIVERY_SERVER_RTMP_PORT} ${DELIVERY_SERVER_HTTP_PORT}

CMD ["nginx", "-g", "daemon off;"]