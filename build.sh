#! /bin/bash

source build/envsetup.sh
export USE_CCACHE=1
ccache -M 50G
export CCACHE_COMPRESS=1
export ANDROID_JACK_VM_ARGS="-Dfile.encoding=UTF-8 -XX:+TieredCompilation -Xmx4G"
export LC_ALL=C
export WITH_SU=true
export JACK_SERVER_VM_ARGUMENTS="-Dfile.encoding=UTF-8 -XX:+TieredCompilation -Xmx4G"
breakfast shamu
croot
brunch shamu 1>~/stdout 2>~/stderr
