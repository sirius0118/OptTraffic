#!/usr/bin/env bash

sh ./start.sh random
sleep 60

sh ./start.sh baseline
sleep 60

sh ./start.sh our

