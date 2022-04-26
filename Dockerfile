FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install wget -y
RUN wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
RUN apt-get install unzip -y
RUN unzip platform-tools-latest-linux.zip -d ~
RUN echo -e "if [ -d \"$HOME/platform-tools\" ] ; then\n  PATH=\"$HOME/platform-tools:\$PATH\"\nfi" >> ~/.profile
RUN /bin/bash -c "source ~/.profile"
RUN apt-get install -y bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf
RUN apt-get install -y imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5
RUN apt-get install -y libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync
RUN apt-get install -y schedtool squashfs-tools xsltproc zip zlib1g-dev libwxgtk3.0-dev
RUN apt-get install -y openjdk-8-jdk
