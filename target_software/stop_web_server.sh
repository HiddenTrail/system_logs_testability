#!/bin/sh
ps -fe | grep http-server | awk '{print $2}' | xargs kill -9 >> /dev/null 2>&1
