#!/bin/sh

JOIN_AS_MODERATOR="";
if [ "${BBB_AS_MODERATOR}" = "true" ]
then
   JOIN_AS_MODERATOR="-m";
fi    

xvfb-run -n 122 --server-args="-screen 0 1360x768x24" python3 stream.py -s ${BBB_URL} -p ${BBB_SECRET} -i ${BBB_MEETING_ID} -t ${BBB_STREAM_URL} -u ${BBB_USER_NAME} $JOIN_AS_MODERATOR;
