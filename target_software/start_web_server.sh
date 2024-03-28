#!/bin/sh
http-server logs -p 8000 >> logs/httpserver.log 2>&1 &
