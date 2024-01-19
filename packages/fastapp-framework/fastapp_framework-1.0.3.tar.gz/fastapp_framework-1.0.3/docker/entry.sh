#!/bin/sh

if [ "$ENV" = "dev" ]; then
    cd /live
    /app/scripts/run-dev
    exit 0
else
    cd /mnt
    /app/scripts/run
    exit 0
fi