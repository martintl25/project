FROM ubuntu:18.04

RUN apt-get install unzip
RUN unzip platform-tools-latest-linux.zip -d ~
RUN echo -e "\n\nif [ -d \"$HOME/platform-tools\" ] ; then\n  PATH=\"$HOME/platform-tools:\$PATH\"\nfi"
RUN source ~/.profile
RUN apt-get install -y bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf
RUN apt-get install -y imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5
RUN apt-get install -y libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync
RUN apt-get install -y schedtool squashfs-tools xsltproc zip zlib1g-dev libwxgtk3.0-dev
RUN apt-get install -y openjdk-8-jdk