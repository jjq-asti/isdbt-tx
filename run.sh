#!/bin/bash

if [ $# -lt 2 ]

then
  /bin/echo "Usage:"
  /bin/echo "./run.sh channel_program.ts layer_a.ts"

  exit 65

fi

docker run --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --privileged -v /dev:/dev -v /proc:/proc -v persistent-37:/home/gnuradio/persistent -v $1:/home/gnuradio/c.ts -v $2:/home/gnuradio/a.ts --group-add=audio -it isdbt-tx sh -c "sudo python2 tx_demo.py"
