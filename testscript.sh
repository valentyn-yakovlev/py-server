#!/bin/bash
#test script for runserver.py

PathToServer="/home/jp/py-server/runserver.py"
address=127.0.0.1
port=8888


LISTEN_ADDRESS=$address LISTEN_PORT=$port $PathToServer &
PID=$!
sleep 2

third_step() {
result=`echo "myip" | nc $address $port`
[ "$result" == "$address" ] && return 0 || return 1
}

fourth_step() {
myip=`ip -o -4 a | awk '$2 !~/lo/{print $4}'| cut -d '/' -f 1 | head -1`
if echo help | nc $myip $port
then return 1
else return 0
fi
}

third_step && fourth_step && echo "Test passed" || echo "Test failed"


kill $PID
