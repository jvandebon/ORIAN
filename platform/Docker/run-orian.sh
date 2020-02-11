#!/bin/bash

IMAGE=ckiddo74/oriancc-dev
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

OPT_EXEC_MODE="--rm -it"
OPT_PORT=""
OPT_CMD=""
OPT_NAME=""
OPT_IMAGE=""

while getopts dp:c:n:lbrsm option
do
case "${option}"
in
d) OPT_EXEC_MODE="-d";;
p) OPT_PORT="-p ${OPTARG}:${OPTARG}";;
c) OPT_CMD="${OPTARG}";;
n) OPT_NAME="--name ${OPTARG}";;
l) OPT_IMAGE="pull";;
b) OPT_IMAGE="build";;
s) OPT_IMAGE="push";;
r) OPT_IMAGE="remove";;
m) OPT_MAX="maxcompiler"
esac
done

echo $OPT_IMAGE

if [[ "$OPT_IMAGE" == "pull" ]]; then
   docker pull $IMAGE
   exit 0
elif [[ "$OPT_IMAGE" == "build" ]]; then
   docker build -t $IMAGE .
   exit 0
elif  [[ "$OPT_IMAGE" == "push" ]]; then
   docker login
   docker push $IMAGE
   exit 0
elif  [[ "$OPT_IMAGE" == "remove" ]]; then
   docker rmi $IMAGE
   exit 0
fi

MACADDR=""
if [[ "OPT_MAX" == "maxcompiler" ]]; then
   MACADDR="--mac-address 18:03:73:F7:74:2C"
fi   

DIRS="/vol/cc /opt/maxeler/ /opt/gcc-4.9.2"

VDIRS=""
for dir in $DIRS 
do
   if [ -d $dir ]; then
      VDIRS="$VDIRS -v $dir:$dir" 
   fi   
done

MAXDEVS=`ls -p /dev/maxeler* 2> /dev/null`
DDEVS=""
for maxd in $MAXDEVS; do
DDEVS="$DDEVS --device=$maxd "
done

if [ -d /dev/infiniband ]; then
VDIRS="$VDIRS -v /dev/infiniband:/dev/infiniband"
fi


docker run  $OPT_EXEC_MODE --privileged -v $ROOT/../..:/root/orian \
           $DDEVS \
           $OPT_NAME \
           $OPT_PORT \
           $VDIRS \
           $MAC_ADDR \
           $OPT_ARG \
           -v $ROOT/../..:/orian \
           -v $ROOT/../../../:/workspace \
           -w /orian \
           $IMAGE \
           /sbin/my_init --quiet -- /usr/local/bin/runtime-dev $USER `id -u $USER` $ROOT  


