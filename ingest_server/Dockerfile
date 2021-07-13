FROM ubuntu:latest
LABEL Description="Ingest server for live stream" Vendor="Joao da Mata" Version="1.0"
ARG DEBIAN_FRONTEND=noninteractive

# Install Dependencies
RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install -y build-essential 
RUN apt-get install -y libpcre3-dev 
RUN apt-get install -y zlib1g-dev 
RUN apt-get install -y libssl-dev
RUN apt-get install -y libfdk-aac-dev \
 libx264-dev \
 libx265-dev \
 ffmpeg  

# Cloning into nginx-rtmp-module
RUN git clone https://github.com/arut/nginx-rtmp-module.git
# Cloning into nginx
RUN git clone https://github.com/nginx/nginx.git

# Compiling nginx
RUN cd nginx \
    && ./auto/configure --add-module=../nginx-rtmp-module \
    && make \
    && make install

# Copy configuration
COPY nginx.conf /usr/local/nginx/conf/
COPY stat.xsl /usr/local/nginx/html/

ENV PATH /usr/local/nginx/sbin:$PATH

EXPOSE ${INGEST_SERVER_RTMP_PORT}

CMD ["nginx", "-g", "daemon off;"]