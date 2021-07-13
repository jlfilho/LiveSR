ARG REPO=vistart
ARG VERSION_CUDA=10.0-cudnn7
ARG VERSION_UBUNTU=20.04
FROM ${REPO}/cuda:${VERSION_CUDA}-devel-ubuntu${VERSION_UBUNTU} as build

ARG VERSION_FFMPEG=4.3.1
ARG VERSION_LIBTENSORFLOW=1.15.0

ARG DEPENDENCIES="\
  autoconf \
  automake \
  build-essential \
  cmake \
  curl \
  git \
  git-core \
  libass-dev \
  libfdk-aac-dev \
  libfreetype6-dev \
  libgnutls28-dev \
  libgomp1 \
  libmp3lame-dev \
  libnuma-dev \
  libopus-dev \
  libsdl2-dev \
  libtool \
  libunistring-dev \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libvpx-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  libxcb1-dev \
  libx264-dev \
  libx265-dev \
  nasm \
  pkg-config \
  python3 \
  python3-pip \
  python3.6 \
  texinfo \
  yasm \
  sudo \
  nano \
  iputils-ping \
  libssl-dev \
  zlib1g-dev \
   mahimahi \
"

ENV DEBIAN_FRONTEND=noninteractive \
  TERM=xterm

COPY script/ /usr/local/sbin/


RUN set -o errexit \
 && set -o xtrace \
 && bootstrap-prepare \
 && bootstrap-upgrade \
 && bootstrap-install ${DEPENDENCIES} \ 
 && build ${VERSION_LIBTENSORFLOW} ${VERSION_FFMPEG} \ 
 && produce-sr-models ${VERSION_LIBTENSORFLOW} 



FROM ${REPO}/cuda:${VERSION_CUDA}-devel-ubuntu${VERSION_UBUNTU}


ENV DEBIAN_FRONTEND=noninteractive \
  TERM=xterm

RUN apt-get update && apt-get install -qy mahimahi \
  python3 \
  python3-pip

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt  

COPY --from=build /deps /
COPY --from=build /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=build /usr/local/bin/ffprobe /usr/local/bin/ffprobe
COPY --from=build /usr/local/share/ffmpeg-tensorflow-models/ /usr/local/share/ffmpeg-tensorflow-models/

RUN ln -s /usr/local/share/ffmpeg-tensorflow-models/ /models 

# Create a user 'client' for use Mahimahi
RUN useradd -ms /bin/bash client
RUN usermod -aG sudo client

# No password to run scripts in the container
RUN echo "client ALL=(ALL)NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /scripts
