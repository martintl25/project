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
RUN apt-get install -y openjdk-8-jdk vim
RUN mkdir -p ~/bin
RUN mkdir -p ~/android/lineage
RUN curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
RUN chmod a+x ~/bin/repo
RUN echo -e "# set PATH so it includes user's private bin if it exists\nif [ -d \"$HOME/bin\" ] ; then\n    PATH=\"$HOME/bin:$PATH\"\nfi" >> ~/.profile
RUN /bin/bash -c "source ~/.profile"
RUN git config --global user.email "martin.tl.cs08@nycu.edu.tw"
RUN git config --global user.name "martintl25"
RUN echo "export USE_CCACHE=1" >> ~/.bashrc
RUN echo "export CCACHE_EXEC=/usr/bin/ccache" >> ~/.bashrc