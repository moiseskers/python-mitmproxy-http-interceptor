#!/bin/bash
export TARGET_HOST="workingapi.com"
export FALLBACK_HOST="localhost"
export FALLBACK_PORT=3000

mitmproxy -s index.py --listen-port 8888
