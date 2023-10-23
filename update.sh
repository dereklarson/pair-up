#!/bin/bash
# Run this script as  `./update.sh pair_up` to force a rebuild of image

docker-compose -f docker/$1/docker-compose.yaml build
