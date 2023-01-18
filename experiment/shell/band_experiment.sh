#!/usr/bin/env bash

sh ./start.sh random
sleep 60

sh ./start.sh baseline
sleep 60

sh ./start.sh our
sleep 60

sleep 1000

sh ./start.sh random
sleep 60

sh ./start.sh baseline
sleep 60

sh ./start.sh our
sleep 60