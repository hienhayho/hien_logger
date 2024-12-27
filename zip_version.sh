#!/bin/bash

FILE=$1

if [ -z "$FILE" ]; then
    echo "Usage: $0 <output-zip-file>"
    exit 1
fi

zip -r "$FILE" . \
    -x "build/*" \
    -x "dist/*" \
    -x "env/*" \
    -x ".pytest_cache/*" \
    -x "logs/*" \
    -x "hien_logger.egg-info/*" \
    -x ".git/*" \
    -x "**/__pycache__/*" \
    -x ".ruff_cache/*"
