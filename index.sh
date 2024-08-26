#!/bin/bash
#./index.sh TARGET_HOST="somehost.com" FALLBACK_HOST="localhost" FALLBACK_PORT=3000

# Iterate over the command-line arguments
for ARG in "$@"
do
  # Use eval to set the environment variables from the arguments
  eval "export $ARG"
done

# Run mitmproxy with the Python script
mitmproxy -s index.py --listen-port 8888
